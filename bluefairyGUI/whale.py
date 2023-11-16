import aiofiles
import os
import logging
import traceback
import asyncio
import threading
from asyncio import Semaphore
from datetime import timedelta
import re
import csv
import os
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Parser():
    def __init__(self, pgn: str):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.pgn = pgn
        self.games = []
        
    def parse(self):
        individual_games = re.split(r'(?=\[Event\s+"[^"]+"\])', self.pgn.strip())
        individual_games = [game.strip() for game in individual_games if game.strip()]

        for game_text in individual_games:
            metadata = self._parse_headers(game_text)
            moves_text = re.sub(r'^\[\w+\s+".*?"\]', '', game_text, flags=re.MULTILINE).strip()
            moves_text = moves_text.replace('\n', ' ')  # This line is added to handle line breaks in moves and annotations
            moves = self._parse_moves(moves_text)

            game = {
                "Metadata": metadata,
                "Moves": moves
            }
            self.games.append(game)

    def _parse_headers(self, game_text: str):
        header_lines = re.findall(r'^\[\w+\s+".*?"\]', game_text, re.MULTILINE)
        headers = {}
        for line in header_lines:
            key, value = re.match(r'\[(.*?)\s+"(.*?)"\]', line).groups()
            headers[key] = value
        return headers
    
    def _parse_moves(self, game_text: str):
        annotations = re.findall(r'\{.*?\}', game_text, re.DOTALL)
        clock_times_str = self.extract_clock_times(annotations)
        moves_str = re.sub(r'\{.*?\}', '', game_text, flags=re.DOTALL).strip()
        moves = self.extract_moves(moves_str)
        clock_times = self.convert_clock_times(clock_times_str)

        paired_moves = []
        for i in range(0, len(moves), 2):
            white_move = moves[i]
            black_move = moves[i+1] if i+1 < len(moves) else None
            move_time = clock_times[i // 2] if clock_times and i // 2 < len(clock_times) else None
            paired_moves.append({
                "move": i // 2 + 1,
                "white": white_move,
                "black": black_move,
                "time": move_time.total_seconds() if move_time else None
            })

        return paired_moves

    @staticmethod
    def extract_moves(moves_str):
        moves = re.findall(r'\b([a-hxNBRQKPO0-9\-+#=]+)\b(?! \{)', moves_str)
        refined_moves = [
            move for move in moves 
            if not move.isdigit() and 
            not re.fullmatch(r'([01]/?[02]-[01]/?[02])', move) and 
            not re.fullmatch(r'([01]-0|0-1)', move) and
            not re.fullmatch(r'(\d+\+\d+)', move)
        ]
        return refined_moves

    @staticmethod
    def associate_moves_with_times(moves, times):
        # Pairing each move with its corresponding time
        move_time_pairs = list(zip(moves, times))
        return move_time_pairs

    @staticmethod
    def extract_clock_times(annotations):
        clock_times = []
        pattern = re.compile(r'%clk (\d+:\d+:\d+(\.\d+)?)', re.DOTALL)
        
        for annotation in annotations:
            match = pattern.search(annotation)
            if match:
                clock_times.append(match.group(1))

        return clock_times if clock_times else None

    @staticmethod
    def convert_clock_times(clock_times_str):
        if not clock_times_str:
            return None
        
        clock_times = []
        for time_str in clock_times_str:
            try:
                # Try to parse with milliseconds
                time = datetime.strptime(time_str, "%H:%M:%S.%f").time()
            except ValueError:
                # If it fails, try to parse without milliseconds
                time = datetime.strptime(time_str, "%H:%M:%S").time()
            clock_times.append(time)

        timedelta_objects = [
            timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond) 
            for t in clock_times
        ]
        return timedelta_objects

    @staticmethod
    def format_timedelta(tdelta):
        total_seconds = tdelta.total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def export_to_csv(self, file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Writing headers
            headers = ['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 
                       'WhiteElo', 'BlackElo', 'TimeControl', 'EndTime', 'Termination',
                       'MoveNumber', 'Move', 'Time']
            writer.writerow(headers)
            
            for game in self.games:
                metadata = game['Metadata']
                for move in game['Moves']:
                    move_number, move_notation, time = move
                    time = '' if time is None else time  # Handle None case for time
                    
                    row = [
                        metadata.get('Event', ''),
                        metadata.get('Site', ''),
                        metadata.get('Date', ''),
                        metadata.get('Round', ''),
                        metadata.get('White', ''),
                        metadata.get('Black', ''),
                        metadata.get('Result', ''),
                        metadata.get('WhiteElo', ''),
                        metadata.get('BlackElo', ''),
                        metadata.get('TimeControl', ''),
                        metadata.get('EndTime', ''),
                        metadata.get('Termination', ''),
                        move_number,
                        move_notation,
                        time
                    ]
                    writer.writerow(row)

async def parse_pgn_files(directory: str):
    parsed_games = []

    if not os.path.exists(directory):
        logging.error(f"The directory {directory} does not exist.")
        return parsed_games

    files = os.listdir(directory)
    logging.info(f"Files in directory {directory}: {files}")

    if not files:
        logging.info(f"The directory {directory} is empty.")
        return parsed_games

    for filename in files:
        logging.info(f"Processing file {filename}")

        if filename.endswith(".pgn"):
            filepath = os.path.join(directory, filename)
            async with aiofiles.open(filepath, mode='r') as file:
                content = await file.read()

                parser = Parser(content)
                parser.parse()
                parsed_games.extend(parser.games)

                # Debug print for verification
                logging.info(f"Parsed {len(parser.games)} games from {filename}")
        else:
            logging.info(f"Skipping file {filename} as it does not have a .pgn extension.")

    logging.info(f"Total games parsed: {len(parsed_games)}")
    return parsed_games

async def main():
    directory = 'games'  # Path to your directory containing PGN files
    parsed_games = await parse_pgn_files(directory)

    # Optional: Print a summary of parsed data for verification
    for game in parsed_games:
        logging.info(f"Game metadata: {game['Metadata']}")
        logging.info(f"First few moves: {game['Moves'][:5]}")  # Print first few moves for each game

asyncio.run(main())