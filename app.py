from flask import Flask, render_template
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Página principal
    @app.route('/')
    def inicio():
        return render_template('index.html')

    # Registro de blueprints
    from controllers.auth import auth_bp
    from controllers.empleados import empleados_bp
    from controllers.activos import activos_bp
    from controllers.reportes import reportes_bp
    from controllers.usuarios import usuarios_bp
    from controllers.dashboard import dashboard_bp
    


    app.register_blueprint(auth_bp)
    app.register_blueprint(empleados_bp)
    app.register_blueprint(activos_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(dashboard_bp)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
