from flask import jsonify
from models import mrts_model



def get_mrts() -> object:

    try:
        res_data = mrts_model.get_mrt_data()
        return jsonify({"data": res_data}), 200
    except:
        return jsonify({"error": True, "message": "Server error"}), 500
