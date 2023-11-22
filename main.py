import json
import os
import openai
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ping")
  return "pong"



def lambda_handler(event, context):
  from flask_lambda import FlaskLambda
  return FlaskLambda(app).dispatch_request(event)

