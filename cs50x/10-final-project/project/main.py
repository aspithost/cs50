from flask import jsonify
from app import app
from app.constants.errors import ERROR_400, ERROR_404, ERROR_500


@app.errorhandler(Exception)
def generic_error_handler(err):
    return jsonify({"error": ERROR_500, "details": str(err)}), 500


@app.errorhandler(400)
def handle_bad_request(err):
    return jsonify({"error": ERROR_400, "details": str(err)}), 400


@app.errorhandler(404)
def handle_not_found(err):
    return jsonify({"error": ERROR_404, "details": str(err)}), 404


if __name__ == '__main__':
    app.run(debug=True)