from flask import Flask, request, jsonify, render_template, redirect, url_for
import json 
import sqlite3
import os
import uuid
import qrcode
import io
import base64

myapp = Flask(__name__)

game_data = {}

@myapp.route('/')
def index():
    return render_template('home.html')

@myapp.route('/setup')
def game_setup():
    game_data.clear()
    return render_template('trpg_setup.html')

@myapp.route('/submit', methods=['POST'])
def submit():
    topic = request.form['selectedTopic']
    # Extracting the number of players
    num_players = request.form['playerCount']
    
    # Update the game setup data
    game_data['topic'] = topic
    game_data['num_players'] = num_players
    # Note: Players' names and phone numbers are no longer collected or stored

    # Here, you can process the data or store it as needed
    print("Topic:", topic)
    print("Number of Players:", num_players)
    
    # Save game_data to a file
    with open('game_data.json', 'w') as f:
        json.dump(game_data, f)
    
    # Redirect to the game display page, or handle as needed
    return jsonify({'status': 'success'}), 200


@myapp.route('/game', methods=['GET'])
def show_game():
    # Todo: Check if the game is still in progress

    qr = qrcode.make('https://t.me/+kMZLpdF_OT5jMjA9')
    qr_io = io.BytesIO()
    qr.save(qr_io, "PNG")
    qr_io.seek(0)
    qr_base64 = base64.b64encode(qr_io.getvalue()).decode()

    return render_template('game_start.html', game_setup=game_data, qr_code=qr_base64)

if __name__ == '__main__':
    myapp.run(debug=True)
