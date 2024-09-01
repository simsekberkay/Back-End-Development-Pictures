from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
     # Find the picture with the given id
    picture = next((item for item in data if item["id"] == id), None)
    
    # If the picture is not found, return a 404 error
    if picture is None:
        return jsonify({"error": "Picture not found"}), 404
    
    # Return the picture URL
    return jsonify(picture)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["POST"])
def create_picture(id):
    picture = request.get_json()
    
    if any(item["id"] == picture["id"] for item in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
    
    data.append(picture)
    return jsonify(picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture_data = request.get_json()
    
    # Find the picture with the given id
    picture = next((item for item in data if item["id"] == id), None)
    
    # If the picture is not found, return a 404 error
    if picture is None:
        return jsonify({"message": "picture not found"}), 404
    
    # Update the picture with the new data
    picture.update(new_picture_data)
    
    # Return the updated picture
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    #picture = next((item for item in data if item["id"] == id), None)
    
    for item in data:
        if item["id"] == str(id):
            data.remove(item)
            return '', 204


    if picture is None:
        return jsonify({"message": "picture not found"}), 404
    
    
    

