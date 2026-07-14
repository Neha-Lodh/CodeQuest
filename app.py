from flask import Flask
from config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.worlds import worlds_bp
from routes.challenges import challenges_bp
from routes.shop import shop_bp
from routes.achievements import achievements_bp
from routes.profile import profile_bp
from routes.leaderboard import leaderboard_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(worlds_bp)
app.register_blueprint(challenges_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(achievements_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(leaderboard_bp)

if __name__ == "__main__":
    app.run(debug=True)