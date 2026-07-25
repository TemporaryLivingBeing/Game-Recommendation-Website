from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os
import requests
import json
import sqlite3
import csv
from datetime import datetime

MIN_HOURS_THRESHOLD = 15
df = None

def create_app(test_config = False, shared_server = False):
    app = Flask(__name__, 
                static_folder='../www/static',
                template_folder='templates')
    app.config['TESTING'] = test_config
    app.config['SHARED_SERVER'] = shared_server

    prepend = ''
    if app.config['SHARED_SERVER']:
        prepend = '/gamefetch'

    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    DATABASE = os.path.join(basedir, 'databases', 'database.db')
    print(f"Database path: {DATABASE}")

    def get_db_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    def load_data():
        global df
        csv_path = os.path.join(os.path.dirname(__file__), 'files', 'steam-200k.csv')
        df = pd.read_csv(csv_path,
                        header=None,
                        names=['user', 'game', 'purchase', 'hours', '0'],
                        quotechar='"')
        df = df.drop(columns=['0', 'purchase'])
        df = df[df['hours'] >= MIN_HOURS_THRESHOLD]
        # print(df.head())

    load_data()

    @app.route(prepend + '/')
    def index():
        return send_from_directory('../www', 'rec.html')

    @app.route(prepend + "/index")
    def main_index():
        return render_template('index.html', prepend=prepend)

    @app.route(prepend + "/about")
    def about():
        return render_template('about.html', prepend=prepend)

    @app.route(prepend + "/contact")
    def contact():
        return render_template('contact.html', prepend=prepend)

    @app.route(prepend + '/saveMessage', methods=['POST'])
    def save_message():
        data = request.get_json()
        
        csv_file = 'test_contacts.csv' if test_config else 'contacts.csv'
        file_exists = os.path.exists(csv_file)
        
        if file_exists:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                row_count = sum(1 for row in csv.reader(file))
                if row_count >= 1000:
                    return jsonify({'message': 'Contact list is full. Try again later.'}), 404
                
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(['NAME', 'EMAIL', 'MESSAGE', 'TIMESTAMP'])
            
            writer.writerow([
                data['name'],
                data['email'],
                data['message'],
                data.get('timestamp', datetime.now().isoformat())
            ])
        return jsonify({'message': 'Contact saved successfully'}), 200

    @app.route(prepend + '/get_recommendations', methods=['POST'])
    def recommend_games():
        user_games = request.json
        if not user_games:
            return jsonify({'error': 'No games provided'}), 400

        test_user_id = 999999999
        filtered_games = {game: hours for game, hours in user_games.items()
                         if hours >= MIN_HOURS_THRESHOLD}

        if not filtered_games:
            return jsonify({'games': []})

        test_user_df = pd.DataFrame({
            'user': [test_user_id] * len(filtered_games),
            'game': list(filtered_games.keys()),
            'hours': list(filtered_games.values())
        })

        temp_df = pd.concat([df, test_user_df], ignore_index=True)
        user_hours = temp_df.groupby('user')['hours'].sum()
        valid_users = user_hours[user_hours >= 50].index
        temp_df = temp_df[temp_df['user'].isin(valid_users)]

        user_profiles = temp_df.pivot_table(
            index='user',
            columns='game',
            values='hours',
            fill_value=0
        )

        if test_user_id not in user_profiles.index:
            return jsonify({'games': []})

        similarity_matrix = cosine_similarity(user_profiles)
        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=user_profiles.index,
            columns=user_profiles.index
        )

        similarity_scores = similarity_df[test_user_id]
        most_similar_users = similarity_scores[
            (similarity_scores.index != test_user_id) &
            (similarity_scores > 0)
        ].nlargest(5).index

        if len(most_similar_users) == 0:
            return jsonify({'games': []})

        all_recommendations = []
        seen_games = set(filtered_games.keys())

        for similar_user in most_similar_users:
            similar_user_games = temp_df[temp_df['user'] == similar_user]
            new_recommendations = similar_user_games[
                (~similar_user_games['game'].isin(seen_games)) &
                (similar_user_games['hours'] >= MIN_HOURS_THRESHOLD)
            ]
            if not new_recommendations.empty:
                seen_games.update(new_recommendations['game'].tolist())
                all_recommendations.append(new_recommendations)

        if not all_recommendations:
            return jsonify({'games': []})

        recommendations = pd.concat(all_recommendations)
        recommendations = recommendations.sort_values('hours', ascending=False)
        recommendations = recommendations.loc[recommendations.groupby('game')['hours'].idxmax()]
        recommendations = recommendations.head(10)

        return jsonify({'games': [{
            'name': row['game'],
            'appid': find_appid(row['game']),
            'playtime_forever': int(row['hours'] * 60)
        } for _, row in recommendations.iterrows()]})

    @app.route(prepend + '/get_games_list')
    def get_games_list():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM games')
        games = cursor.fetchall()
        conn.close()
        return jsonify([dict(game) for game in games])

    @app.route(prepend + "/game_page/<game_id>")
    def create_game_page(game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM games WHERE steam_appid = ?', (game_id,))
        game = cursor.fetchone()
        conn.close()

        if game:
            game_json = dict(game)
            for field in ['genres', 'categories', 'developers', 'publishers']:
                if game_json.get(field):
                    game_json[field] = json.loads(game_json[field])
        else:
            with open('files/game_details_complete.json', 'r') as file:
                game_json = json.load(file)    
            if game_id not in game_json.keys():
                game_json = {}
            else:
                game_json = game_json[game_id]
        
        return render_template("game_page.html", game_json=game_json, prepend=prepend)

    @app.route(prepend + '/get_available_games', methods=['GET'])
    def get_available_games():
        if df is None:
            load_data()
        valid_games = df[df['hours'] >= MIN_HOURS_THRESHOLD]['game'].unique()
        return jsonify({'games': sorted(valid_games.tolist())})

    @app.route(prepend +  '/get_available_games_index', methods=['POST'])
    def get_available_games_index():
        if df is None:
            load_data()
        game_request = request.json.get('game')
        percent = request.json.get('percent')
        tags = request.json.get('tags')
        if percent == None:
            percent = .7
        else:
            percent = percent/100
        if tags == "":
            tags = None
        
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

        conn = get_db_connection()
        cursor = conn.cursor()
        games_data = []
        
        for game in top_games:
            cursor.execute("SELECT name, steam_appid, genres FROM games WHERE name LIKE ?", (f"%{game}%",))
            result = cursor.fetchone()
            if tags:
                if result:
                    if tags.lower() in result['genres'].lower():
                        games_data.append({
                            'name': result['name'],
                            'appid': result['steam_appid']
                        })
                else:
                    appid = find_appid(game)
                    games_data.append({
                        'name': game,
                        'appid': appid
                    })
            
            else:
                if result:
                    games_data.append({
                        'name': result['name'],
                        'appid': result['steam_appid']
                    })
                else:
                    appid = find_appid(game)
                    games_data.append({
                        'name': game,
                        'appid': appid
                    })
        
        conn.close()
        print()
        return jsonify({'games': games_data})

    return app

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