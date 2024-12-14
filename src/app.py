import logging
from flask import Flask, jsonify, request, Response
from inference import InferenceEngine
from typing import Union

# LOGGER
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app_logs.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
logger.info("App started successfully")

# LOADING THE CLASSIFIER
inference_engine = InferenceEngine()
logger.info("Classifier loaded successfully")

@app.route("/", methods=['GET'])
def hello_world() -> str:
    """
    GET:
    Returns the homepage.
    """
    logger.info("Homepage accessed")
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
            logger.info("GET request to /find_your_agent")
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
            logger.info(f"Error handling GET request to /find_your_agent: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    if request.method == 'POST':
        try:
            logger.info("POST request to /find_your_agent")
            # TODO: INSTEAD OF request.json, USE request.form TO HANDLE USER INPUT FORM DATA
            data = request.json
            inference_engine.input = data
            agent = inference_engine.get_prediction()
            return jsonify({"agent": agent})
        except Exception as e:
            logger.info(f"Error handling POST request to /find_your_agent: {str(e)}")
            return jsonify({"error": str(e)}), 500
