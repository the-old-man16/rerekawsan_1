from flask import Flask
from config.config import Config
from models.student import db, bcrypt
from routes.auth import auth_bp
from routes.student import student_bp  
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp, url_prefix='/')
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True)

