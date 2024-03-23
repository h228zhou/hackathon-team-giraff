from flask import Flask, request, jsonify, render_template, redirect, url_for
import json 
import sqlite3
import os
import uuid

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
    # Extracting the TRPG topic
    topic = request.form['selectedTopic']
    # Extracting the number of players
    num_players = request.form['playerCount']
    
    # Extracting player names and phone numbers
    players_info = []
    for i in range(1, int(num_players) + 1):
        player_name_key = f'player{i}Name'
        player_phone_key = f'player{i}Phone'
        player_name = request.form.get(player_name_key, '')
        player_phone = request.form.get(player_phone_key, '')
        players_info.append({'name': player_name, 'phone': player_phone})
    
    game_data['topic'] = topic
    game_data['num_players'] = num_players
    game_data['players_info'] = players_info
    # Here, you can process the data or store it as needed
    print("Topic:", topic)
    print("Number of Players:", num_players)
    print("Players Info:", players_info)
    
    # Just returning the data for demonstration; in a real app, you might redirect or return a success response
    return redirect(url_for('show_game'))

@myapp.route('/game', methods=['GET'])
def show_game():
    # Todo: Check if the game is still in progress
    return render_template('game_start.html', game_setup=game_data)

if __name__ == '__main__':
    myapp.run(debug=True)
