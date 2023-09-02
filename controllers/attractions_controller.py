from flask import Blueprint, request, jsonify, blueprints
import models.attractions_model as attractions_model
import sys
from errorhandling.errorhandling import handle_error



def get_attractions() -> object:
    #get query string
    try:
        page_parameter = request.args.get("page")
        keyword_parameter = request.args.get("keyword")

    except:
        return jsonify({"error": True, "message": "Invalid query string"}), 400
    
    ##get data 
    try:
        res_data =  attractions_model.get_attractions(keyword_parameter, page_parameter)
        return jsonify({"nextPage": int(page_parameter)+1, "data":res_data}),200
    except:
        return jsonify({"error": True, "message": "Server error"})
    

def get_attraction_by_id(attractionId) -> object:
    try:
        attractionId = int(attractionId)
        res_data = attractions_model.get_attraction_by_id(attractionId)
        if res_data==None:
            return jsonify({"error":True, "message":"Not attractoin data"}), 400
        return jsonify({"data":res_data}),200

    except:
        return jsonify({"error": True, "message": "Invalid query string"}), 400


