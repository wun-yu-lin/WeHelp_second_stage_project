from flask import json, make_response
from werkzeug.exceptions import HTTPException
from app import app


## Error handling
@app.errorhandler(HTTPException)
def handle_error(e):
    #error handling
    response_arg ={
        "headers": {
            "content-Type": "application/json"
        },
        "data": {
            "code": e.code,
            "description": e.description,
            "error": e.error
        }
    }
    #error handling
    response = make_response(response_arg, e.code)
    return response