import os

from src import create_app

config_name = os.getenv( 'CLUSTER_CONFIG' )
connexion_app = create_app( config_name )

if __name__ == '__main__':
    connexion_app.run()