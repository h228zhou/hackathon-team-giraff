import telebot
import random

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_TOKEN' with your bot's actual token
TOKEN = '7032284841:AAECCa6i81k0qC40AUm6wX8ec55D8R9EXGs'
bot = telebot.TeleBot(TOKEN)

# Roles and user tracking
roles = ['Dungeon Master', 'Warrior', 'Mage', 'Rogue', 'Cleric']
chat_user_tracking = {}  # Key: chat_id, Value: set of user_ids


@bot.message_handler(commands=['startroles'])
def start_roles(message):
    chat_id = message.chat.id
    chat_user_tracking[chat_id] = set()  # Initialize or reset the user set
    bot.reply_to(message, "Role assignment started. Please send me any message to register for a role.")

@bot.message_handler(func=lambda message: True)
def track_user_interaction(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    # Ensure only to track after startroles command is issued
    if chat_id in chat_user_tracking:
        chat_user_tracking[chat_id].add(user_id)

@bot.message_handler(commands=['assignrole'])
def assign_roles(message):
    bot.reply_to(message, "Assignrole command received.")
    chat_id = message.chat.id
    if chat_id not in chat_user_tracking or len(chat_user_tracking[chat_id]) == 0:
        bot.reply_to(message, "No participants detected or registration has not started. Use /startroles to initiate.")
        return
    
    participants = list(chat_user_tracking[chat_id])
    random.shuffle(roles)  # Shuffle roles for random assignment

    if len(participants) > len(roles):
        bot.reply_to(message, "Not enough roles for all participants. Some participants will not receive a role.")
        participants = participants[:len(roles)]  # Limit participants to the number of roles available
    
    # Assign roles to participants
    assignments = {user_id: role for user_id, role in zip(participants, roles)}
    
    # Inform each participant of their role
    for user_id, role in assignments.items():
        try:
            bot.send_message(user_id, f"Your assigned role: {role}")
        except Exception as e:
            print(f"Error sending role to user {user_id}: {e}")

    bot.send_message(chat_id, "Roles have been assigned. Please check your private messages from me!")

if __name__ == '__main__':
    bot.polling()
