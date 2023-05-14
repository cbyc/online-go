from flask import Flask, request, jsonify, send_from_directory
from collections import defaultdict
import os

app = Flask(__name__, static_folder='static')

games = defaultdict(lambda: [[None for _ in range(9)] for _ in range(9)])

@app.route('/games/<game_id>', methods=['GET', 'POST'])
def game(game_id):
    if request.method == 'POST':
        data = request.json
        x, y, color = data['x'], data['y'], data['color']
        if games[game_id][x][y] is not None:
            return 'This cell is already occupied!', 400  # Bad Request
        games[game_id][x][y] = color
        return '', 204  # No Content
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/games/<game_id>/state', methods=['GET'])
def game_state(game_id):
    return jsonify(games[game_id])

@app.route('/games/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    games[game_id] = [[None for _ in range(9)] for _ in range(9)]
    return '', 204  # No Content

if __name__ == '__main__':
    app.run(debug=True)
