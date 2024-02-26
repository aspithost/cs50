from flask import request, jsonify
from app import app
from app.helpers.is_true import is_true
from app.constants.errors import DETAILS_400_INVALID, ERROR_400, ERROR_404_TEAMS, ERROR_404_TEAM_MEMBERS, ERROR_500
from app.constants.teams import TEAM_KEYS, SEASON_KEYS
from app.helpers.dict import validate_dict_keys
from app.helpers.list import validate_list_keys
from app.services.team_service import create_team, get_team, update_team, delete_team, get_team_members, create_team_member, delete_team_member


@app.route("/teams", methods=["POST"])
def create_team_route():
    try:
        team = request.get_json()["team"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(team, TEAM_KEYS):
        return jsonify({"error": ERROR_400, "details": "Invalid input"}), 400
    try:
        create_team(team)
    except Exception:
        return jsonify({"error": "Could not create team"}), 500
    return jsonify({ "message": "Team created successfully!"}), 201


@app.route("/teams/<int:team_id>", methods=["GET"])
def get_team_route(team_id):
    options = {
        "colors": is_true(request.args.get("colors")),
        "details": is_true(request.args.get("details"))
    }
    try:
        team = get_team(team_id, options)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not team:
            return jsonify({"error": ERROR_404_TEAMS}), 404
        return jsonify(team), 200


@app.route("/teams/<int:team_id>", methods=["PUT"])
def update_team_route(team_id):
    try:
        team = request.get_json()["team"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(team, TEAM_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        is_updated = update_team(team_id, team)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_updated:
            return jsonify({"error": ERROR_404_TEAMS}), 404
        return jsonify({"message": "Successfully updated team", "team": {**team, "team_id": team_id}}), 201


@app.route("/teams/<int:team_id>", methods=["DELETE"])
def delete_team_route(team_id):
    try:
        is_deleted = delete_team(team_id)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_deleted:
            return jsonify({"error": ERROR_404_TEAMS}), 404
        return jsonify(), 204


@app.route("/teams/<int:team_id>/players", methods=["GET"])
def get_team_members_route(team_id):
    req_seasons = request.args.get("seasons")
    seasons = req_seasons.split(",") if req_seasons else ["23-24"]
    try:
        team_players = get_team_members(team_id, seasons)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not team_players:
            return jsonify({"error": ERROR_404_TEAM_MEMBERS}), 404
        return jsonify(team_players), 200


@app.route("/teams/<int:team_id>/players/<int:player_id>", methods=["POST"])
def create_team_member_route(team_id, player_id):
    try:
        seasons = request.get_json()["seasons"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_list_keys(seasons, SEASON_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        create_team_member(team_id, player_id, seasons)
    except Exception as err:
        return jsonify({"error": "Could not add team member"}), 500
    return jsonify({ "message": "Team member added successfully!"}), 201


@app.route("/teams/<int:team_id>/players/<int:player_id>", methods=["DELETE"])
def delete_team_member_route(team_id, player_id):
    try:
        if not request.get_data():
            return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
        seasons = request.get_json()["seasons"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_list_keys(seasons, SEASON_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        is_deleted = delete_team_member(team_id, player_id, seasons)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_deleted:
            return jsonify({"error": ERROR_404_TEAM_MEMBERS}), 404
        return jsonify(), 204