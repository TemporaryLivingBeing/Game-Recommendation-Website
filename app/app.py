from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/hello")
def hello():
    return render_template('index.html')

@app.route("/game_page/<game_id>")
def create_game_page(game_id):
    print('something')
    with open('/Users/jacksbigmac/Downloads/Game-Recommendation-Website/app/files/game_details_complete.json', 'r') as file:
        game_json = json.load(file)    
    game_json = game_json[str(game_id)]
    print(game_json)
    return render_template("game_page.html", game_title = game_json["name"], game_info = game_json["detailed_description"])

df = None
MIN_HOURS_THRESHOLD = 15

def load_data():
    global df
    df = pd.read_csv(
        'files/steam-200k.csv', 
        header=None,
        names=['user', 'game', 'purchase', 'hours', '0'],
        quotechar='"',
    )
    df = df.drop(columns=['0', 'purchase'])
    df = df[df['hours'] >= MIN_HOURS_THRESHOLD]

@app.route('/get_available_games', methods=['GET'])
def get_available_games():
    if df is None:
        load_data()
    valid_games = df[df['hours'] >= MIN_HOURS_THRESHOLD]['game'].unique()
    return jsonify({'games': sorted(valid_games.tolist())})

if __name__ == "__main__":
    app.run(debug=True)
