from __future__ import annotations

from flask import Flask

from productivity.api.employees import bp as employees_bp

def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(employees_bp)

    #basic health check
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200
    
    return app