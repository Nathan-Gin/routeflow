// Create the map inside the map-area element.
const map = L.map("map-area").setView([51.9000, -8.4760], 14.5);


// Add OpenStreetMap tiles to the map.
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

let map_data = null
let comparisonMode = false;

async function loadMapData() {
    const response = await fetch("api/map");
    map_data = await response.json();

    // Add a marker to the map for each node.
    for (const node of map_data.nodes) {
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
    const bounds = map_data.nodes.map(
        node => [node.lat, node.lon]
    );

    map.fitBounds(bounds)


    // Draw each graph edge on the map.
    for (const edge of map_data.edges) {

        const fromNode = map_data.nodes.find(
            node => node.id === edge.from
        );

        const toNode = map_data.nodes.find(
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
let routeLine = null;
let dijkstraLine = null;
let astarLine = null;

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

async function handleCalculation() {
    
    if (compareMode){
        await compareAlgorithms();
    }else{
        await calculateRoute();
    }
}

async function calculateRoute() {
    const start = document.getElementById("start").value;
    const destination = document.getElementById("destination").value;
    const algorithm = document.getElementById("algorithm").value;

    const data = await requestRoute(start, destination, algorithm);

    //Remove previous route if there is one
    if (routeLine){
        map.removeLayer(routeLine);
    }
    if (dijkstraLine) {
    map.removeLayer(dijkstraLine);
    }
    if (astarLine) {
        map.removeLayer(astarLine);
    }
    
    const routeCoordinates = pathToCoordinates(data.path)

    // Draw the calculated route.
    routeLine = L.polyline(routeCoordinates, {
        weight: 5,
        color: "#ff8a3d"
    }).addTo(map);

    document.getElementById("distance").textContent =
        `${data.distance} m`;

    document.getElementById("nodes-explored").textContent =
        data.nodes_explored;

    //this combines array elements returned by flask with " → "
    document.getElementById("path").textContent =
        data.path.join(" → ");
}

async function  compareAlgorithms(params) {
    const start = document.getElementById("start").value;
    const destination = document.getElementById("destination").value;

    const dijkstraData = await requestRoute(start, destination, "dijkstra");
    const astarData = await requestRoute(start, destination, "astar");

    //Remove previous route if there is one
    if (routeLine){
        map.removeLayer(routeLine);
    }
    if (dijkstraLine) {
    map.removeLayer(dijkstraLine);
    }
    if (astarLine) {
        map.removeLayer(astarLine);
    }

    const dijkstraCoordinates = pathToCoordinates(dijkstraData.path)
    const astarCoordinates = pathToCoordinates(astarData.path)

    dijkstraLine = L.polyline(dijkstraCoordinates, {
        weight: 6,
        color: "#4b6bff",
    }).addTo(map);

    astarLine = L.polyline(astarCoordinates, {
        weight: 3,
        color: "#ff5c5c"
    }).addTo(map);

    document.getElementById("dijkstra-distance").textContent =
    `${dijkstraData.distance} m`;

    document.getElementById("dijkstra-nodes").textContent =
    dijkstraData.nodes_explored;

    document.getElementById("astar-distance").textContent =
    `${astarData.distance} m`;

    document.getElementById("astar-nodes").textContent =
    astarData.nodes_explored;

}

async function requestRoute(start, destination, algorithm) {
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
        const node = map_data.nodes.find(
            node => node.id ===nodeID
        );

        return [node.lat, node.lon]
    });
}
