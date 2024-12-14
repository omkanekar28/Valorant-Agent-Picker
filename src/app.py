import logging
from flask import Flask, jsonify, request, Response
from inference import InferenceEngine
from typing import Union

# LOADING THE CLASSIFIER
inference_engine = InferenceEngine()

# LOGGER
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('app_logs.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app_logger.addHandler(file_handler)

app = Flask(__name__)
app_logger.info("App started successfully")

@app.route("/", methods=['GET'])
def hello_world() -> str:
    """
    GET:
    Returns the homepage.
    """
    app_logger.info("Homepage accessed")
    return "<h1>Homepage</h1><hr>"

@app.route("/find_your_agent", methods=['GET', 'POST'])
def find_your_agent() -> Union[str, Response]:
    """
    GET:
    Returns the 'Find your Agent' page where user can submit 
    their data to the model.

    POST:
    Takes user data, performs inference and returns the 
    predicted agent.
    """
    if request.method == 'GET':
        try:
            app_logger.info("GET request to /find_your_agent")
            # TODO: HAVE A FORM TO SEND USER INPUT
            # EXPECTED JSON OUTPUT FROM THE FORM
            # {
            #     "Agent_Type": "Initiator",
            #     "Playstyle": "Supportive",
            #     "Difficulty": "Easy",
            #     "Ability_Preference": "Agility",
            #     "Gun_Type": "Snipers"
            # }
            return "<h1>Find your Agent</h1><hr>"
        except Exception as e:
            app_logger.info(f"Error handling GET request to /find_your_agent: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    if request.method == 'POST':
        try:
            app_logger.info("POST request to /find_your_agent")
            # TODO: INSTEAD OF request.json, USE request.form TO HANDLE USER INPUT FORM DATA
            data = request.json
            inference_engine.input = data
            agent = inference_engine.get_prediction()
            return jsonify({"agent": agent})
        except Exception as e:
            app_logger.info(f"Error handling POST request to /find_your_agent: {str(e)}")
            return jsonify({"error": str(e)}), 500
