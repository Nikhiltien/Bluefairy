from quart import Quart, request, jsonify, websocket, render_template
from quart_cors import cors
from game_manager import ChessGame
from analysis import GameAnalyzer
import json

app = Quart(__name__)
app = cors(app, allow_origin="*") 
connected_clients = set()
game = ChessGame()
analyze = GameAnalyzer()

@app.route('/')
async def index():
    return await render_template('index.html')

@app.websocket('/ws')
async def ws():
    connected_clients.add(websocket._get_current_object())
    print("WebSocket client connected")
    try:
        while True:
            message = await websocket.receive()
            print("Message received:", message)  # Log the received message
            await process_message(message)
    finally:
        connected_clients.remove(websocket._get_current_object())
        print("WebSocket client disconnected")

async def broadcast_update(game_state):
    for client in connected_clients:
        await client.send(game_state)

async def process_message(message):
    data = json.loads(message)
    if 'command' in data and data['command'] == 'reset':
        await reset_board()
    elif 'move' in data:
        move_made = data['move']
        print(f"Move Made: {move_made}")
        move_result = analyze.make_move(move_made)  # Make the move and store the result
        print(f"Move result: {move_result}")
        if move_result:
            new_fen = analyze.current_fen()
            print(f"New Fen: {new_fen}")
            analyze.load_game_state_from_fen(new_fen)  # Sync GameAnalyzer with ChessGame
            evaluation_score = await analyze.evaluate_current_position()
            normalized_score = analyze.normalize_score(evaluation_score)
            print("Evaluation Score:", normalized_score)

            # Broadcast the new game state and evaluation to all clients
            await broadcast_update(json.dumps({'fen': new_fen, 'evaluation': normalized_score}))
            print("Broadcasting update")

async def broadcast_update(game_state):
    for client in connected_clients:
        print("Broadcasting:", game_state)  # Log the broadcast message
        await client.send(game_state)

@app.route('/evaluate', methods=['POST'])
async def evaluate():
    # Directly use the current state of the GameAnalyzer for evaluation
    score = await analyze.evaluate_current_position()
    return jsonify({'evaluation': score})

@app.route('/load_pgn', methods=['POST'])
async def load_pgn():
    try:
        data = await request.json
        pgn_string = data.get('pgn')
        print("Received PGN:", pgn_string)  # Log the received PGN string
        if not pgn_string:
            return jsonify({'status': 'error', 'message': 'No PGN provided'}), 400

        game_object = analyze.pgn_to_game(pgn_string)
        print("Converted to game object")  # Log success of conversion
        analyze.load_game_state_from_object(game_object)  
        current_fen = analyze.current_fen()
        move_list = analyze.extract_moves_from_game(game_object)
        print("FEN and move list extracted")  # Log success of extraction
        return jsonify({'status': 'success', 'fen': current_fen, 'moveList': move_list})
    except Exception as e:
        print(f"Error processing PGN: {e}")  # Log the exception
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/move', methods=['POST'])
async def make_move():
    data = await request.json
    if analyze.make_move(data['move']):
        return jsonify({'status': 'success', 'board': analyze.current_board()})
    else:
        return jsonify({'status': 'illegal move'}), 400

@app.route('/undo', methods=['POST'])
async def undo_move():
    if game.undo_move():
        return jsonify({'status': 'success', 'board': analyze.current_board()})
    else:
        return jsonify({'status': 'no moves to undo'}), 400

@app.route('/game_state', methods=['GET'])
async def game_state():
    return jsonify({'status': 'success', 'state': game.game_state(), 'board': game.current_board()})

@app.websocket('/reset_board')
async def reset_board():
    print("Resetting board")
    analyze.reset_board()  # Reset GameAnalyzer instance
    await broadcast_update(json.dumps({'fen': analyze.board.fen()}))

if __name__ == "__main__":
    app.run(debug=True)