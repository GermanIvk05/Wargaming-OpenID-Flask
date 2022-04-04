# Wargaming-OpenID-Flask
Contians Flask Python code to receive OpenID requests from Wargaming. It uses Flask to create local server and ngrok to get a public link where the infromation from OpenID will be redirected to. The program automatically setups flask server with ngrok tunnel thus creating Wargaming OpenID link. The data from response will be collected and stored in JSON format in file named account.json.

### In the configuration file named config.py you will need to:

1. Input your **Wargaming Application ID**
2. Input your **ngrok** account authentication token

### You will need to install these libraries:

1. Flask
2. pytz

You can do so by typing `python -m pip install module_name`

### Then you are all set!
