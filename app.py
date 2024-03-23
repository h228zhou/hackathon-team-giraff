from flask import Flask, request, jsonify, render_template

myapp = Flask(__name__)

@myapp.route('/')
def index():
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
    
    # Here, you can process the data or store it as needed
    print("Topic:", topic)
    print("Number of Players:", num_players)
    print("Players Info:", players_info)
    
    # Just returning the data for demonstration; in a real app, you might redirect or return a success response
    return jsonify({
        'topic': topic,
        'num_players': num_players,
        'players_info': players_info
    })

if __name__ == '__main__':
    myapp.run(debug=True)
