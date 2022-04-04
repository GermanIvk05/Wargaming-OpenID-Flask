# Name: Wargaming OpenID Authentication Server
# Author: German Ivkovich
# Date: 04/03/2022
# File: server.py


from datetime import datetime
from flask import Flask, request
from threading import Thread
from werkzeug.serving import make_server

import json
import pytz

import config


# Add underscore to make the variable private
# User needs to create Flask instance using "create_app" function
_app = Flask(__name__)


class ServerThread(Thread):
    """Class for Server Thread controls"""

    def __init__(self, app: Flask) -> None:
        super().__init__(target=self)
        self.server = make_server('localhost', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self) -> None:
        """Runs the server thread"""

        print(" * Runnnig Server Thread!")
        self.server.serve_forever()

    def shutdown(self) -> None:
        """Shutdowns the server thread"""

        print(" * Shutting down server thread")
        self.server.shutdown()


def convert_timestamp(timestamp: int) -> str:
    """Convert timestamp to EST timezone"""

    timezone = pytz.timezone('US/Eastern')
    dt_object = datetime.fromtimestamp(timestamp)
    est_time = dt_object.astimezone(timezone)
    return est_time.strftime('%d %b %H:%M %p EST')


def create_app(port: int) -> Flask:
    """Create flask server to receive account data"""

    # Initialize ngrok settings into Flask
    _app.config.from_mapping(
        BASE_URL = f'https://localhost:{port}/',
        USE_NGROK = config.USE_NGROK == True
    )

    if _app.config['USE_NGROK']:

        # Initialize ngok only if we need it
        from pyngrok import ngrok

        #Setting an auth token to allow multiple tunnels
        ngrok.set_auth_token(config.NGROK_AUTH_TOKEN)

        # Open a ngrok tunnel to the server
        public_url = ngrok.connect(port, 'http').public_url
        print(f' * ngrok tunnel "{public_url}" -> "https://127.0.0.1:{port}"')

        # Update any base URLs or webhooks to use the public ngrok URL
        _app.config['BASE_URL'] = public_url

    return _app


@_app.route('/')
def receive_data() -> str:
    """Receives Account Information"""

    # Retrive data from URL request
    status = request.args.get('status', None)
    access_token = request.args.get('access_token', None)   
    nickname = request.args.get('nickname', None)
    account_id = int(request.args.get('account_id', 0))
    expires_at = int(request.args.get('expires_at', 0))

    # Convert account information into JSON format
    account_info = {
        'status': status,
        'access_token': access_token,
        'nickname': nickname,
        'account_id': account_id,
        'expires_at': convert_timestamp(expires_at)
    }

    # Record the results as JSON file
    with open('account.json', 'w') as file:
        json.dump(account_info, file, indent=4, ensure_ascii=False)
        file.close()

    # Create HTML page and return that page instead of this
    return f"<h1 align=\"center\">You're all set! You can close this window now.</h1>"


def main() -> None:
    """Contains main code of the program"""

    # Create a Flask instance with port 5000
    app = create_app(5000)
    
    # Print out the url to the wargaming authenticaion website
    print(config.LOGIN_URL.format(application_id=config.APPLICATION_ID, redirect_uri=app.config['BASE_URL']))

    # Create a server thread
    server = ServerThread(app)

    server.start()  # Starts the server thread

    # Add time delay here before server shutdowns

    server.shutdown()   # Shutdowns the server thread


if __name__ == '__main__':
    main()
