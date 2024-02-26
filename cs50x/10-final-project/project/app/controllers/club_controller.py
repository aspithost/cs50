from flask import request, jsonify
from app import app
from app.constants.clubs import CLUB_KEYS, COLORS_KEYS, DETAILS_KEYS
from app.constants.errors import DETAILS_400_INVALID, ERROR_400, ERROR_404_CLUBS, ERROR_500
from app.helpers.dict import validate_dict_keys
from app.helpers.is_true import is_true
from app.services.club_service import (
    create_club,
    get_club,
    update_club,
    delete_club,
    create_club_colors,
    update_club_colors,
    create_club_details,
    update_club_details
)


@app.route("/clubs", methods=["POST"])
def create_club_route():
    try:
        club = request.get_json()["club"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(club, CLUB_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        create_club(club)
    except Exception:
        return jsonify({"error": ERROR_500, "details": "Could not create club"}), 500
    else:
        return jsonify({ "message": "Club created successfully!"}), 201


@app.route("/clubs/<int:club_id>", methods=["GET"])
def get_club_route(club_id):
    options = {
        "colors": is_true(request.args.get("colors")),
        "details": is_true(request.args.get("details"))
    }
    try:
        club = get_club(club_id, options)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not club:
            return jsonify({"error": ERROR_404_CLUBS}), 404
        return jsonify(club), 200


@app.route("/clubs/<int:club_id>", methods=["PUT"])
def update_club_route(club_id):
    try:
        club = request.get_json()["club"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(club, CLUB_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        is_updated = update_club(club_id, club)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_updated:
            return jsonify({"error": ERROR_404_CLUBS}), 404
        return jsonify({"message": "Successfully updated club", "club": club}), 201


@app.route("/clubs/<int:club_id>", methods=["DELETE"])
def delete_club_route(club_id):
    try:
        is_deleted = delete_club(club_id)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_deleted:
            return jsonify({"error": ERROR_404_CLUBS}), 404
        return jsonify(), 204


@app.route("/clubs/<int:club_id>/colors", methods=["POST"])
def create_club_colors_route(club_id):
    try:
        club_colors = request.get_json()["colors"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(club_colors, COLORS_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        create_club_colors(club_id, club_colors)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        return jsonify({ "message": "Club colors created successfully!"}), 201


@app.route("/clubs/<int:club_id>/colors", methods=["PUT"])
def update_club_colors_route(club_id):
    try:
        club_colors = request.get_json()["colors"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(club_colors, COLORS_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        is_updated = update_club_colors(club_id, club_colors)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_updated:
            return jsonify({"error": ERROR_404_CLUBS}), 404
        return jsonify({"message": "Successfully updated club colors", "colors": club_colors}), 201


@app.route("/clubs/<int:club_id>/details", methods=["POST"])
def create_club_details_route(club_id):
    try:
        club_details = request.get_json()["details"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(club_details, DETAILS_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        create_club_details(club_id, club_details)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        return jsonify({ "message": "Club details created successfully!"}), 201


@app.route("/clubs/<int:club_id>/details", methods=["PUT"])
def update_club_details_route(club_id):
    try:
        club_details = request.get_json()["details"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(club_details, DETAILS_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        is_updated = update_club_details(club_id, club_details)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_updated:
            return jsonify({"error": ERROR_404_CLUBS}), 404
        return jsonify({"message": "Successfully updated club colors", "details": club_details}), 201


