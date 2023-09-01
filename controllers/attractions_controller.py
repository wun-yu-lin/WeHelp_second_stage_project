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
        return handle_error({"code": 400, "message": "Invalid query string"}), 400
    
    ##get data 
    try:
        res_data =  attractions_model.get_attractions(keyword_parameter, page_parameter)
        return jsonify(res_data),200
    except:
        return handle_error({"code": 400, "message": "Server error"})
    





    return "get_attractions",200

def get_attraction_by_id(attractionId) -> object:
    return "get_attraction_by_id",200