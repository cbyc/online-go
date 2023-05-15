from flask import Flask, request, jsonify, send_from_directory
from collections import defaultdict
import os
import random
import string
import copy

app = Flask(__name__, static_folder='static')

games = defaultdict(
    lambda: {
        "board": [[None for _ in range(9)] for _ in range(9)],
        "current_player": "black",
        "history": []
    })


@app.route('/games/<game_id>', methods=['GET', 'POST'])
def game(game_id):
    if request.method == 'POST':
        game = games[game_id]
        data = request.json
        x, y, color = data['x'], data['y'], data['color']
        if game["board"][x][y] is not None:
            return 'This cell is already occupied!', 400  # Bad Request
        game["history"].append(copy.deepcopy(game["board"]))
        game["board"][x][y] = color
        game[
            "current_player"] = "white" if color == "black" else "black"  # Switch the current player
        return '', 204  # No Content
    else:
        return send_from_directory(app.static_folder, 'board.html')


@app.route('/games/<game_id>/state', methods=['GET'])
def game_state(game_id):
    game = games[game_id]
    return jsonify({
        "board": game["board"],
        "current_player": game["current_player"]
    }), 200


@app.route('/games/<game_id>/undo', methods=['POST'])
def undo(game_id):
    game = games[game_id]
    if game["history"]:
        game["board"] = game["history"].pop()  # Revert to the last state
        game["current_player"] = "white" if game[
            "current_player"] == "black" else "black"  # Switch the current player
    return {
        "board": game["board"],
        "current_player": game["current_player"]
    }, 200


@app.route('/games/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    games[game_id] = {
        "board": [[None for _ in range(9)] for _ in range(9)],
        "current_player": "black",
        "history": []
    }
    return '', 204  # No Content


@app.route('/games', methods=['POST'])
def new_game():
    game_name = request.json.get('game_name')
    if game_name in games:
        return {'error': 'Game name already exists'}, 400  # Bad Request
    games[game_name] = {"board": [[None for _ in range(9)] for _ in range(9)], 
                        "current_player": "black",
                        "history": []}
    return {'game_id': game_name}, 201  # Created


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
