import os
from flask_cors import CORS
import connexion

from config import app_config

def create_app( config_name: str ) -> object:
    """
    :param config_name: Name of the configuration
    :return: An application with all of the necessary configuration information.
    """
    # First create the Connexion application
    connexion_app = connexion.App( __name__, debug=True)
    # connexion_app.add_api('openapi.yml', arguments={'title': 'ADMS Swagger'}, pythonic_params=True, strict_validation=True, validate_responses=True)

    # Now that the Connexion application is created get Flask application
    application = connexion_app.app
    application.config.root_path = application.instance_path
    application.config.from_object( app_config[ config_name ] )
    application.config.from_pyfile( os.getcwd() + '/config.py' )

    CORS( application )

    # Register all of the controllers
    with application.app_context():
        from src.controllers import (
            hello_world_controller
        )

        application.register_blueprint( hello_world_controller.hello_world_controller, url_prefix = f'/{application.config[ "URL_ROOT" ]}' )

    return connexion_app