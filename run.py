import os
from flask import Flask
from app.admin.routes import admin
from app.blog.routes import blog
from dotenv import load_dotenv
from app.extensions import limiter
from app.db_setup import DatabaseManager

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(admin,)
    app.register_blueprint(blog)
    load_dotenv()
    app.secret_key = os.environ.get('SECRET_KEY')
    limiter.init_app(app)
    DatabaseManager.init_db()
    return app
    
app: Flask = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=False)