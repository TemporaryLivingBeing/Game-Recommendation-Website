from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

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

def get_recommendations(user_games):
    if df is None:
        load_data()
    
    test_user_id = 999999999
    filtered_games = {game: hours for game, hours in user_games.items() 
                     if hours >= MIN_HOURS_THRESHOLD}
    
    if not filtered_games:
        return []
    
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
        return []

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
        return []

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
        return []

    recommendations = pd.concat(all_recommendations)
    recommendations = recommendations.sort_values('hours', ascending=False)
    recommendations = recommendations.loc[recommendations.groupby('game')['hours'].idxmax()]
    recommendations = recommendations.head(10)

    return [{
        'name': row['game'],
        'appid': '0',
        'playtime_forever': int(row['hours'] * 60)
    } for _, row in recommendations.iterrows()]

@app.route('/get_recommendations', methods=['POST'])
def recommend_games():
    user_games = request.json
    if not user_games:
        return jsonify({'error': 'No games provided'}), 400
    recommendations = get_recommendations(user_games)
    return jsonify({'games': recommendations})

@app.route('/get_available_games', methods=['GET'])
def get_available_games():
    if df is None:
        load_data()
    valid_games = df[df['hours'] >= MIN_HOURS_THRESHOLD]['game'].unique()
    return jsonify({'games': sorted(valid_games.tolist())})

if __name__ == '__main__':
    load_data()
    app.run(debug=True)