from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests


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
    with open('files/game_details_complete.json', 'r') as file:
        game_json = json.load(file)    
    if game_id not in game_json.keys():
        game_json = {}
    else:
        game_json = game_json[game_id]
    return render_template("game_page.html", game_json=game_json)

df = None
def load_data():
    global df
    df = pd.read_csv(
        'files/steam-200k.csv', 
        header=None,
        names=['user', 'game', 'purchase', 'hours', '0'],
        quotechar='"',
    )
    df = df.drop(columns=['0', 'purchase'])

def find_appid(game_name):
    url = "https://store.steampowered.com/api/storesearch"
    params = {
        'term': game_name,
        'l': 'english',
        'cc': 'US'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get('total', 0) > 0:
            return str(data['items'][0]['id'])
        return '0'

    except Exception as e:
        print(f"Error finding AppID for {game_name}: {e}")
        return '0'


@app.route('/get_available_games', methods=['POST'])
def get_available_games():
    if df is None:
        load_data()
    game_request = request.json.get('game')
    percent = request.json.get('percent')/100
    print(game_request)
    print(percent)
    if not game_request:
        return jsonify({'error': 'No games provided'}), 400

    hours_percent = df[df['game'] == game_request]['hours'].quantile(percent)
    real_gamers = df[(df['game'] == game_request) & (df['hours'] >= hours_percent)]['user'].unique()
    games = df[(df['user'].isin(real_gamers))]['game'].unique().tolist()
    temp_df = (
        df[df['user'].isin(real_gamers) & df['game'].isin(games) & (df['hours'] > 0)]
        .groupby('game', as_index=False)['hours']
        .mean()
    )
    temp_df.rename(columns={'hours': 'average_hours'}, inplace=True)
    temp_df = temp_df.sort_values(['average_hours'], ascending=False)
    if temp_df.shape[0] == 0:
        return jsonify({"games": []})
    elif temp_df.shape[0] <= 10:
        top_games = temp_df.head(temp_df.shape[0])['game'].tolist()
    else:
        top_games = temp_df.head(10)['game'].tolist()
    x =  jsonify({'games': [{'name' : game, 'appid' : find_appid(game)} for game in top_games]})
    print(x)
    return x

if __name__ == "__main__":
    app.run(debug=True)
