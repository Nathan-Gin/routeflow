// Create the map inside the map-area element.
const map = L.map("map-area").setView([51.9000, -8.4760], 14.5);


// Add OpenStreetMap tiles to the map.
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

let mapData = null;
let comparisonMode = false;

async function loadMapData() {
    const response = await fetch("api/map");
    mapData = await response.json();

    // Add a marker to the map for each node.
    for (const node of mapData.nodes) {
        L.marker([node.lat, node.lon])
            .addTo(map)
            .bindPopup(`Location: ${node.id}`);

        // Add location to dropdowns (within the )
        const startOption = document.createElement("option");
        startOption.value = node.id;
        startOption.textContent = node.id;

        const destinationOption = document.createElement("option");
        destinationOption.value = node.id;
        destinationOption.textContent = node.id;

        document.getElementById("start").appendChild(startOption);
        document.getElementById("destination").appendChild(destinationOption);
    }

    //zooms to map to the boundaires of the markers added
    const bounds = mapData.nodes.map(
        node => [node.lat, node.lon]
    );

    map.fitBounds(bounds)


    // Draw each graph edge on the map.
    for (const edge of mapData.edges) {

        const fromNode = mapData.nodes.find(
            node => node.id === edge.from
        );

        const toNode = mapData.nodes.find(
            node => node.id === edge.to
        );

        L.polyline(
            [
                [fromNode.lat, fromNode.lon],
                [toNode.lat, toNode.lon]
            ],
            {
                weight: 2
            }
        ).addTo(map);
    }

}

loadMapData();
let routeLine = [];
let dijkstraLine = [];
let astarLine = [];

//Calculate Route

const calculateButton = document.getElementById("calculate-button");
const singleModeButton = document.getElementById("single-mode");
const compareModeButton = document.getElementById("compare-mode");

calculateButton.addEventListener("click", handleCalculation);

singleModeButton.addEventListener("click", () => {
    compareMode = false;

    singleModeButton.classList.add("active");
    compareModeButton.classList.remove("active");

    document.getElementById("algorithm").style.display = "block";
    calculateButton.textContent = "Calculate Route";

    document.getElementById("single-route").style.display = "block";
    document.getElementById("comparison-results").style.display = "none";

    document.getElementById("algorithm-label").style.display = "block";
});

compareModeButton.addEventListener("click", () => {
    compareMode = true;

    compareModeButton.classList.add("active");
    singleModeButton.classList.remove("active");

    document.getElementById("algorithm").style.display = "none";
    calculateButton.textContent = "Compare Algorithms";

    document.getElementById("single-route").style.display = "none";
    document.getElementById("comparison-results").style.display = "block";

    document.getElementById("algorithm-label").style.display = "none";
});

// Sets single Mode as default
singleModeButton.click(); 

// Adding stops
const addStopButton = document.getElementById("add-stop");
addStopButton.addEventListener("click", addStop);

async function handleCalculation() {
    
    if (compareMode){
        await compareAlgorithms();
    }else{
        await calculateRoute();
    }
}

async function calculateRoute() {
    const stops = getStops()
    const algorithm = document.getElementById("algorithm").value;

    const data = await requestRoute(stops, algorithm);

    removeLines();

    routeLine = drawRoutes(data, "#ff8a3d", 5);

    const totals = calculateTotals(data);
    const fullPath = combinePaths(data);    

    document.getElementById("distance").textContent =
    `${totals.distance} m`;

    document.getElementById("nodes-explored").textContent =
    totals.nodes;

    //this combines array elements returned by flask with " → "
    document.getElementById("path").textContent =
        fullPath.join(" → ");
}

async function  compareAlgorithms() {
    const stops = getStops()

    const dijkstraData = await requestRoute(stops, "dijkstra");
    const astarData = await requestRoute(stops, "astar");

    removeLines();

    dijkstraLine = drawRoutes(dijkstraData, "#4b6bff" , 6)
    astarLine = drawRoutes(astarData, "#ff5c5c", 3);

    const dijkstraTotals = calculateTotals(dijkstraData);
    const astarTotals = calculateTotals(astarData);

    document.getElementById("dijkstra-distance").textContent =
    `${dijkstraTotals.distance} m`;

    document.getElementById("dijkstra-nodes").textContent =
    dijkstraTotals.nodes;

    document.getElementById("astar-distance").textContent =
    `${astarTotals.distance} m`;

    document.getElementById("astar-nodes").textContent =
    astarTotals.nodes;

}

async function requestRoute(stops, algorithm) {
    let route = [];

    for (let i = 0; i < stops.length - 1; i++) {
        const result = await _requestRoute(
            stops[i],
            stops[i + 1],
            algorithm
        );

        route.push(result);
    }

    return route;

}

async function _requestRoute(start, destination, algorithm) {
    const response = await fetch("/api/routes/calculate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        // Convert the JavaScript object into a JSON string.
        body: JSON.stringify({
            start: start,
            destination: destination,
            algorithm: algorithm
        })
    });

    const data = await response.json();

    return data;
}

// Convert the path IDs into coordinates.
// each node goes to the nodes above
// and converts to geographic coordinates
function pathToCoordinates(path){
    return path.map(
    nodeID => {
        const node = mapData.nodes.find(
            node => node.id ===nodeID
        );

        return [node.lat, node.lon]
    });
}

function addStop() {

    const stopContainer = document.createElement("div");
    stopContainer.classList.add("stop");

    const select = document.createElement("select")

    // Populate new select option with nodes
    for (const node of mapData.nodes) {

        // Add location to dropdowns (within the )
        const option = document.createElement("option");
        option.value = node.id;
        option.textContent = node.id;

        select.appendChild(option);
    } 

    const removeButton = document.createElement("button");
    removeButton.textContent = "Remove";

    removeButton.addEventListener("click", () => {
        stopContainer.remove();
    });

    stopContainer.appendChild(select);
    stopContainer.appendChild(removeButton);

    document.getElementById("stops-container").appendChild(stopContainer);
}

function getStops() {
    const start = document.getElementById("start").value;
    const destination = document.getElementById("destination").value;
    const stopElements = document.querySelectorAll("#stops-container select");
    
    // For each stop if it exists get its element (location)
    const stops = Array.from(stopElements).map(
        select => select.value
    );

    return [start, ...stops, destination];
}

function removeLines(){
    if (routeLine.length > 0) {
        _removeLines(routeLine);
        routeLine = [];
    }

    if (dijkstraLine.length > 0) {
        _removeLines(dijkstraLine);
        dijkstraLine = [];
    }

    if (astarLine.length > 0) {
        _removeLines(astarLine);
        astarLine = [];
    }
}

function _removeLines(lines) {
    for (let i = 0; i < lines.length; i++){
        map.removeLayer(lines[i]);
    }
}

function calculateTotals(data) {
    let totalDistance = 0;
    let totalNodes = 0;

    for (let i = 0; i < data.length; i++) {
        totalDistance += data[i].distance;
        totalNodes += data[i].nodes_explored;
    }

    return {
        distance: totalDistance,
        nodes: totalNodes
    };
}

function drawRoutes(data, colour, weight) {
    const lines = [];

    for (let i = 0; i < data.length; i++) {
        const routeCoordinates = pathToCoordinates(data[i].path);

        const currentLine = L.polyline(routeCoordinates, {
            weight: weight,
            color: colour
        }).addTo(map);

        lines.push(currentLine);
    }

    return lines;
}

function combinePaths(data) {
    let fullPath = [];

    for (let i = 0; i < data.length; i++) {
        if (i === 0) {
            fullPath.push(...data[i].path);
        } else {
            fullPath.push(...data[i].path.slice(1));
        }
    }

    return fullPath;
}