from quart import Quart, request, jsonify, websocket, render_template
from game_manager import ChessGame
from analysis import GameAnalyzer

app = Quart(__name__)
connected_clients = set()
game = ChessGame()
analysis = GameAnalyzer()

@app.route('/')
async def index():
    return await render_template('index.html')

@app.websocket('/ws')
async def ws():
    connected_clients.add(websocket._get_current_object())
    try:
        while True:
            message = await websocket.receive()
            await process_message(message)
    finally:
        connected_clients.remove(websocket._get_current_object())

async def broadcast_update(game_state):
    for client in connected_clients:
        await client.send(game_state)

async def process_message(message):
    # Process incoming messages and broadcast updates
    pass

@app.route('/move', methods=['POST'])
async def make_move():
    data = await request.json
    if game.make_move(data['move']):
        return jsonify({'status': 'success', 'board': game.current_board()})
    else:
        return jsonify({'status': 'illegal move'}), 400

@app.route('/undo', methods=['POST'])
async def undo_move():
    if game.undo_move():
        return jsonify({'status': 'success', 'board': game.current_board()})
    else:
        return jsonify({'status': 'no moves to undo'}), 400

@app.route('/game_state', methods=['GET'])
async def game_state():
    return jsonify({'status': 'success', 'state': game.game_state(), 'board': game.current_board()})

@app.route('/evaluate', methods=['POST'])
async def evaluate():
    data = await request.json
    board = game.Board(data['fen'])
    info = await analysis.analyze_position_async(board)
    score = info['score']
    return jsonify({'evaluation': score.string()})

if __name__ == "__main__":
    app.run(debug=True)