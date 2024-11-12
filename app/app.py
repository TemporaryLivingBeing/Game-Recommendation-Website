from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/game_page/<game_id>")
def create_game_page(game_id):
    with open('/app/files/game_details_complete.json', 'r') as file:
        game_json = json.load(file)    
    if game_id not in game_json.keys():
        game_json = {}
    else:
        game_json = game_json[game_id]
    return render_template("game_page.html", game_json=game_json)

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
    # valid_games = df[df['hours'] >= MIN_HOURS_THRESHOLD]['game'].unique()
    game_request = request.json.get('game')
    hours_percent = df[df['game'] == game_request]['hour'].quantile(0.7)
    gamers = df[df[df['game'] == game_request]['hours'] > hours_percent]
    # gamers[gamers['game'] != game_request][]
    # return jsonify({'games': sorted(valid_games.tolist())})

if __name__ == "__main__":
    app.run(debug=True)
