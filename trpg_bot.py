import telebot
import random

# Your bot's token here
TOKEN = '7032284841:AAECCa6i81k0qC40AUm6wX8ec55D8R9EXGs'
bot = telebot.TeleBot(TOKEN)

# A simple list of roles
roles = ["Warrior", "Mage", "Archer", "Healer", "Rogue"]

# A dictionary to keep track of users' roles
user_roles = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send any message to this group, and I'll assign you a unique role.")

@bot.message_handler(func=lambda message: True)
def assign_role(message):
    user_id = message.from_user.id
    if user_id not in user_roles:
        # Assign a role randomly and ensure it's unique
        role = random.choice([r for r in roles if r not in user_roles.values()])
        user_roles[user_id] = role
        bot.reply_to(message, f"Your role is {role}!")
    else:
        # Inform the user of their already assigned role
        bot.reply_to(message, f"You already have a role: {user_roles[user_id]}")

def main():
    bot.polling()

if __name__ == '__main__':
    main()
