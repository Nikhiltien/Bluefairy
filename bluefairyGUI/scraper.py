import json
import os
import requests
from requests.exceptions import HTTPError

PLAYER_NAME = "nikix0x0"

headers = {
    'User-Agent': 'Bluefairy/1.0 (bluefairy@gmail.com)',
}

base_url = "https://api.chess.com/pub/player/"
player_name = PLAYER_NAME
final_url = f"{base_url}{player_name}"

response = requests.get(final_url, headers=headers)

# Check for errors
if response.status_code != 200:
    print(f"Failed to fetch data: {response.status_code}")
    exit(1)

class ChessComPlayerArchives:
    def __init__(self, username):
        self.username = username
        self.archives = []
    
    def fetch_last_archives(self, num_archives=1):
        try:
            response = requests.get(f"https://api.chess.com/pub/player/{self.username}/games/archives", headers=headers)
            response.raise_for_status()
            json_data = response.json()
            self.archives = json_data.get('archives', [])[-num_archives:]  
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return
        except json.JSONDecodeError:
            print("Failed to decode the JSON response.")
            return
    
    def get_games(self):
        return self.games
    
    def download_archives(self, folder_path='./games'):
        os.makedirs(folder_path, exist_ok=True)
        
        for i, archive_url in enumerate(self.archives):
            month_str = archive_url.split('/')[-1]  # Extract the month from the URL
            pgn_response = requests.get(f"{archive_url}/pgn", headers=headers)
            if pgn_response.status_code == 200:
                file_path = f"{folder_path}/{self.username}_{month_str}.pgn" # needs year
                with open(file_path, 'w') as f:
                    f.write(pgn_response.text)
                print(f"Successfully downloaded archive {i + 1} to {file_path}")
            else:
                print(f"Failed to download archive {i + 1} with status code {pgn_response.status_code}")

if __name__ == "__main__":
    player_archives = ChessComPlayerArchives('hikaru')
    player_archives.fetch_last_archives()
    player_archives.download_archives()
    
    for i, archive in enumerate(player_archives.archives):
        print(f"Archive {i + 1}:\n{archive}\n{'=' * 40}\n")