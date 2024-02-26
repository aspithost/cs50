from flask import request, jsonify
from app import app
from app.constants.errors import DETAILS_400_INVALID, ERROR_400, ERROR_404_PLAYERS, ERROR_500
from app.constants.players import PLAYER_KEYS
from app.helpers.dict import validate_dict_keys
from app.services.player_service import create_player, get_player, update_player, delete_player


@app.route("/players", methods=["POST"])
def create_player_route():
    try:
        player = request.get_json()["player"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(player, PLAYER_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        create_player(player)
    except Exception:
        return jsonify({"error": ERROR_500, "details": "Could not create player"}), 500
    else: 
        return jsonify({ "message": "Player created successfully!"}), 201


@app.route("/players/<int:player_id>", methods=["GET"])
def get_player_route(player_id):
    try:
        player = get_player(player_id)
    except Exception:
        return jsonify({"error": ERROR_500}), 500    
    else:
        if not player:
            return jsonify({"error": ERROR_404_PLAYERS}), 404
        return jsonify(player), 200


@app.route("/players/<int:player_id>", methods=["PUT"])
def update_player_route(player_id):
    try:
        player = request.get_json()["player"]
    except KeyError:
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    if not validate_dict_keys(player, PLAYER_KEYS):
        return jsonify({"error": ERROR_400, "details": DETAILS_400_INVALID}), 400
    try:
        is_updated = update_player(player_id, player)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_updated:
            return jsonify({"error": ERROR_404_PLAYERS}), 404
        return jsonify({"message": "Successfully updated player", "player": player}), 201


@app.route("/players/<int:player_id>", methods=["DELETE"])
def delete_player_route(player_id):
    try:
        is_deleted = delete_player(player_id)
    except Exception:
        return jsonify({"error": ERROR_500}), 500
    else:
        if not is_deleted:
            return jsonify({"error": ERROR_404_PLAYERS}), 404
        return jsonify(), 204