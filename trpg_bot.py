import telebot
import random
import openai
from telebot.types import ChatPermissions
import time

# OpenAI Keys
gpt_client = openai.OpenAI(api_key= "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",)

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

n = 2
r = 2
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


This should be a game for {n} different players, start with player 1, giving choice, receive his/her choice, then adjust the story, the move to next player, then repeating the step above, after all player make choice, this count as a round. After a round start a new round, continue start with player 1 as mentioned above. After receive the reply of one player move to the next player.the game will end at the {r} round, Untill the end of the game, give a conclusion.
Start the mutiplayer game 

Each response must be no more than 4000 characters and the response must be plain text
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    unmute_all = ChatPermissions(can_send_messages=True)
    bot.set_chat_permissions(chat_id, permissions=unmute_all)
    bot.reply_to(message, "Hello! Send any message to this group, and I'll assign you a unique role.")

@bot.message_handler(commands=['assign_role'])
def assign_role(message):
    user_id = message.from_user.id
    if user_id not in roles_user.values():
        # Assign a role randomly and ensure it's unique
        role = "Player " + str(n - len(roles_user))
        roles_user[role] = user_id
        user_roles[user_id] = role
        bot.reply_to(message, f"Your role is {role}!")
        if len(roles_user) == n:
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
        gpt_messages.append({"role": "user", "content": choice})
        gpt_response = interact_with_gpt(str(gpt_messages))
        gpt_messages[-1]["response"] = gpt_response

        bot.send_message(chat_id, gpt_response)

        player_turn += 1
        if player_turn > n:
            player_turn -= n

def interact_with_gpt(prompt):
    response = gpt_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def game_start():
    bot.send_message(chat_id, "All players roles have been assigned. The game is about to begin. Please check your DM boxes to continue")
    # mute_all = ChatPermissions(can_send_messages=False)
    # unmute_all = ChatPermissions(can_send_messages=True)
    # bot.set_chat_permissions(chat_id, permissions=unmute_all)

    gpt_response = interact_with_gpt(game_text)
    gpt_messages.append({"role": "user", "content": game_text, "response": gpt_response})
    bot.send_message(chat_id, gpt_response)

    i = 0
    while i < r:
        for player in range(n):
            next_turn(player + 1)
            print("player = " + str(player))
            while player_turn == player + 1:
                time.sleep(3)
        
        i += 1
    print("out of the loop")

def next_turn(player):
    prompt = f'''
    Give me 3 choice for Player {player}, I will choose 1 
    and then you need to give the story adjusted by the choice.
    '''
    gpt_messages.append({"role": "user", "content": prompt})
    gpt_response = interact_with_gpt(str(gpt_messages))

    gpt_messages[-1]["response"] = gpt_response

    bot.send_message(roles_user[f"Player {player}"], gpt_response)

def main():
    bot.polling()

if __name__ == '__main__':
    main()
