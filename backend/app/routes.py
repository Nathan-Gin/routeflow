from flask import Blueprint

"""
Learning for self - 
the Blueprint creates a container that groups the APIs
endpoints with similar characteristcs together
first parameter is the name the second is the 
python module it belongs to
"""
routes = Blueprint("routes", __name__)


@routes.get("/api/health")
def health():
    return {"status": "healthy"}


