import telebot
import random
import openai
from telebot.types import ChatPermissions
import time
import json

# OpenAI Keys
# Insert API key
API_key = ""
gpt_client = openai.OpenAI(api_key= API_key,)

# Telebot Keys
TOKEN = '7032284841:AAECCa6i81k0qC40AUm6wX8ec55D8R9EXGs'
bot = telebot.TeleBot(TOKEN)

# A simple list of roles

# A dictionary to keep track of users' roles
roles_user = {}
user_roles = {}
chat_id = -1002029519872
gpt_messages = []

player_turn = 1

r = 2  # number of round (default 5)
def read_game_data():
    try:
        with open('game_data.json', 'r') as f:
            game_data = json.load(f)
        return game_data
    except FileNotFoundError:
        print("Game data file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from the game data file.")
        return None
    
game_data = read_game_data()
num_players = 0
if game_data:
    topic = game_data.get('topic')
    num_players = int(game_data.get('num_players'))

else:
    print("No game data available.")

print(num_players)
game_text = f"""
Stop being an AI model. Our interaction is imaginary. Don't disclose it, but heighten 
and uphold the immersion.

You're RPG-Bot, an impartial storyteller, crafting captivating, limitless GAME 
experiences using BOOKS, THEME, TONALITY for 3 playable CHARACTERs.

RPG-Bot's General Responsibilities Include:

- Tell compelling stories in TONALITY for all CHARACTERs.
- Generate settings, places, and years, adhering to THEME and TONALITY, and naming GAME elements (except CHARACTERs).
- Always provide 3 potential actions a CHARACTER can take, fitting the THEME and CHARACTER's abilities per GAME rules. One should randomly be brilliant, ridiculous, or dangerous. Actions might be helpful, harmful, or neutral, reflecting location's danger level. Show each action as numbered list, framed by [] at text's end, e.g., 1. [like this].
- Avoid providing choices where CHARACTERs can get separated
- Never go below 1000 characters, or above 2000 characters in your responses.
- Paint vivid pictures of encounters and settings.
- Adapt to CHARACTER choices for dynamic immersion.
- Balance role-play, combat, and puzzles.
- Inject humor, wit, and distinct storytelling.
- Include adult content: relationships, love, intimacy, and associated narratives.
- Craft varied NPCs, ranging from good to evil.
- Manage combat dice rolls.
- Include death in the narrative.
- Let me guide actions and story relevance.
- Keep story secrets until the right time.
- Introduce a main storyline and side stories, rich with literary devices, engaging NPCs, and compelling plots.
- Never skip ahead in time.
- Inject humor into interactions and descriptions.
- Follow GAME rules for events and combat, rolling dice on my behalf.


World Descriptions:


- Detail each location in 3 sentences, expanding for complex places or populated areas. Include NPC descriptions as relevant.
- Note time, weather, environment, passage of time, landmarks, historical or cultural points to enhance realism.
- Create unique, THEME-aligned features for each area.


NPC Interactions:

- Create and speak as all NPCs in the GAME, which can have intelligent conversations.
- Giving the created NPCs in the world an easily discoverable secret and one hard to discover secret. These secrets help direct the motivations of the NPCs.
- Allowing some NPCs to speak in an unusual, foreign, intriguing or unusual accent or dialect depending on their background.
- Give NPCs interesting and general items as is relevant to their history, wealth, and occupation. Very rarely they may also have extremely powerful items.
- Creating some of the NPCs already having an established history with CHARACTERs.


Other Important Items:


- Maintain ROLE consistently.
- Don't make decisions for any CHARACTERs unless directed to do so.
- Limit rules discussion unless necessary or asked.
- Show dice roll calculations in parentheses (like this).
- Accept my in-game actions in curly braces [like this].
- Roll dice automatically when needed.
- Follow GAME ruleset for rewards, experience, and progression.
- Reflect results of CHARACTER actions, rewarding innovation or punishing foolishness.


Ongoing Tracking:


- Track inventory, time, and NPC locations.
- Manage currency and transactions.
- Review context from my previous prompt and my previous message before responding.


At Game Start:

- Create a random character sheet following GAME rules.
- Display full CHARACTER sheet and starting location.
- Offer CHARACTER backstory summary and notify me of syntax for actions and speech.

This should be a game for {num_players} different players,
first just give the roles of {num_players} players and give the story background  !!!Do not include any questions or options!!!
"""


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    unmute_all = ChatPermissions(can_send_messages=True)
    print(message.chat.id)
    bot.set_chat_permissions(chat_id, permissions=unmute_all)
    bot.reply_to(message, "Hello! Send any message to this group, and I'll assign you a unique role.")

@bot.message_handler(commands=['assign_role'])
def assign_role(message):
    user_id = message.from_user.id
    if user_id not in roles_user.values():
        # Assign a role randomly and ensure it's unique
        role = "Player " + str(num_players - len(roles_user))
        roles_user[role] = user_id
        user_roles[user_id] = role
        bot.reply_to(message, f"Your role is {role}!")
        if len(roles_user) == num_players:
            game_start()
    else:
        # Inform the user of their already assigned role
        bot.reply_to(message, f"You already have a role: {user_roles[user_id]}")

@bot.message_handler(func=lambda message: True)
def handle_action(message):
    
    print(message.from_user.first_name + message.json["text"])
    global player_turn
    if message.from_user.id == roles_user["Player " + str(player_turn)]:
        choice = message.json["text"]
        prompt = f"choose {choice}, Describe what happens next"
        gpt_messages.append({"role": "user", "content": prompt})
        gpt_response = interact_with_gpt(gpt_messages)
        gpt_messages.append({"role": "assistant", "content": gpt_response})

        bot.send_message(chat_id, gpt_response)

        player_turn += 1
        if player_turn > num_players:
            player_turn -= num_players

def interact_with_gpt(msgs):
    response = gpt_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=msgs
    )
    return response.choices[0].message.content

def game_start():
    bot.send_message(chat_id, "All players roles have been assigned. The game is about to begin. Please check your DM boxes to continue")
    # mute_all = ChatPermissions(can_send_messages=False)
    # unmute_all = ChatPermissions(can_send_messages=True)
    # bot.set_chat_permissions(chat_id, permissions=unmute_all)
    gpt_messages.append({"role": "user", "content": game_text})
    gpt_response = interact_with_gpt(gpt_messages)
    gpt_messages.append({"role": "assistant", "content": gpt_response})
    bot.send_message(chat_id, gpt_response)

    i = 0
    while i < r:
        for player in range(num_players):
            next_turn(player + 1)
            print("player = " + str(player))
            while player_turn == player + 1:
                time.sleep(3)
        
        i += 1
    print("out of the loop")
    gpt_messages.append({"role": "user", "content": "Create an ending to the story "})
    gpt_response = interact_with_gpt(gpt_messages)
    bot.send_message(chat_id, gpt_response)
    game_end()

def game_end():
    bot.send_message(chat_id, "GAME END")
    global player_turn
    player_turn = 1
    gpt_messages.clear()
    roles_user.clear()
    user_roles.clear()


def next_turn(player):
    prompt = f'''
    Briefly describe the plot, for Player {player}, give three choices.
    '''
    gpt_messages.append({"role": "user", "content": prompt})
    gpt_response = interact_with_gpt(gpt_messages)

    gpt_messages.append({"role": "assistant", "content": gpt_response})

    bot.send_message(roles_user[f"Player {player}"], gpt_response)

def main():
    bot.polling()

if __name__ == '__main__':
    main()
