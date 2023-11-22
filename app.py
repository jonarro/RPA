from flask import Flask, jsonify, request
from flask_cors import CORS

import core.scraper as scraper
import model.config as config
from model.config import ConfigScrap
from scraper import scraper as scraper_v2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/v2/people', methods=['POST'])
def people_v2():
  print(request.form)
  data ={
    'keyword': request.form['keyword'] if 'keyword' in request.form and request.form['keyword'] else "",
    'location': request.form['location'] if 'location' in request.form and request.form['location'] else "Leon, Guanajuato",
    'final_page': int(request.form['final_page']) if 'final_page' in request.form and request.form['final_page'] else 1,
    'initial_page': int(request.form['initial_page']) if 'initial_page' in request.form and request.form['initial_page'] else 1,
    'profiles_to_search': list(request.form['profiles_to_search'].split(",")) if 'profiles_to_search' in request.form and request.form['profiles_to_search'] else [],
    'is_search': bool(request.form['is_search']) if 'is_search' in request.form and request.form['is_search'] else False,
  }
  config = ConfigScrap(**data)
  df = scraper_v2.search_people(config.__dict__)
  if df is not None:
   df.to_csv("data.csv", index=False)
  else:
    print("No hay datos")
  return {'message': 'ok'}
  
app.run(debug=True)
