import json
import os

# Path to the folder containing the JSON files
json_folder_path = 'game_details'

final_data = {}

for filename in os.listdir(json_folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(json_folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:

            game_data = json.load(f)
            steam_appid = str(game_data.get("steam_appid"))
            
            final_data[steam_appid] = game_data

with open('game_details_complete.json', 'w', encoding='utf-8') as outfile:
    json.dump(final_data, outfile, indent=4)

print("JSON files have been combined and saved as 'combined_games.json'")
