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
        nextPage = int(page_parameter)+1
        #無第13筆資料，代表沒有下一頁
        if len(res_data) <13:
            nextPage = None
        ##修改資料數量為12筆
        if (len(res_data)==13):
            res_data.pop()

        return jsonify({"nextPage": nextPage, "data":res_data}),200
    except:
        return jsonify({"error": True, "message": "Server error"})
    

def get_attraction_by_id(attractionId) -> object:
    try:
        attractionId = int(attractionId)


    except:
        return jsonify({"error": True, "message": "Invalid query string"}), 400

    try:
        res_data = attractions_model.get_attraction_by_id(attractionId)
        if res_data==None:
            return jsonify({"error":True, "message":"Not attractoin data"}), 400
    except:
        return jsonify({"error": True, "message": "mysql server error"}), 500
    return jsonify({"data":res_data}),200
