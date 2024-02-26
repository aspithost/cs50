from flask import Flask
from app.db import init_football_db


app = Flask(__name__)


# Initialize db
init_football_db()


from app.controllers import club_controller, player_controller, team_controller