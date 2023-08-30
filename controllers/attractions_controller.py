from flask import Blueprint, request, jsonify, blueprints


def get_attractions() -> object:
    return "get_attractions",200

def get_attraction_by_id(attractionId) -> object:
    return "get_attraction_by_id",200