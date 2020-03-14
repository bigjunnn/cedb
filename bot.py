import telebot
from telebot import types
import os
# from dotenv import load_dotenv

#API key for deployment
API_KEY = os.environ['API_KEY']

# load_dotenv()
# API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(API_KEY)

commands = {  # command description used in the "help" command
    'start': 'If you are a first time user of this bot, register yourself with this command!',
    'edit': 'Edits your user details',
    'recommend': 'Recommends food portion changes about meals in a canteen',
    'logmeal': 'Record down a meal that you had.',
    'help': 'Gives you information about the available commands',
    'report': 'Have feedback about food portions in NUS Canteens? Use this command to report about them!'
}

user_info = {}

# Helper methods to for the start command

# get age
def process_age_step(message):
    global user_info
    chat_id = message.chat.id
    age = message.text
    user_info["age"] = age
    msg = bot.reply_to(message, 'Are you male or female (M/F)?')
    bot.register_next_step_handler(msg, process_gender_step)

# get gender
def process_gender_step(message):
    global user_info
    chat_id = message.chat.id
    gender = message.text
    user_info["gender"] = gender
    msg = bot.reply_to(message, 'How tall are you, in centimetres? Reply with a number, eg 145 for 145 cm.')
    bot.register_next_step_handler(msg, process_height_step)

# get height
def process_height_step(message):
    global user_info
    chat_id = message.chat.id
    height = message.text
    user_info["height"] = height
    msg = bot.reply_to(message, 'What is your weight, in kg?')
    bot.register_next_step_handler(msg, process_weight_step)

# get weight
def process_weight_step(message):
    global user_info
    chat_id = message.chat.id
    weight = message.text
    user_info["weight"] = weight

    details = "Age: " + user_info["age"] + " years old\n" + "Gender: " + user_info["gender"] + "\nHeight: " + user_info["height"] + " cm\nWeight: " + user_info["weight"] + "kg"
    msg = bot.reply_to(message, 'Great! You are now registered in our database with the following details:\n' + details)
    user_info = {}


  
#start 
@bot.message_handler(commands = ['start'])
def start_message(message):
  msg = bot.reply_to(message, "We see that you are a first timer. We need to know some details from you. How old are you?")
  bot.register_next_step_handler(msg, process_age_step)
  
  

#edit
@bot.message_handler(commands = ['edit'])
def edit_details(message):
  #TODO retrieve current details from database 
  details = """"Your current details are: 
          Age: 
          Gender: 
          Height: 
          Weight: 
          
          To edit your details, reply with the attributes you want changed.\n
          For example, if you want to change your height to 160 cm and weight to 50kg, you reply with this:
          
          height: 160
          weight: 50
          
          Type /back if you do not want to edit your details."""
  #display current details 
  bot.send_message(chat_id = message.chat.id, text = details)
  #get user input
  msg = bot.reply_to(message, text)
  replies = msg.chat.text.split("\n")
  for reply in replies: 
    if reply[:3] == "Age":
      #TODO update age 
      global user_info 
      user_info["age"] = reply[3:]
      bot.send_message(chat_id = message.chat.id, text = "Age updated.")
    elif reply[:6] == "Gender":
      #update gender 
      user_info["gender"] = reply[6:]
      bot.send_message(chat_id = message.chat.id, text = "Gender updated.")
    elif reply[:6] == "Height":
      #update height 
      user_info["height"] = reply[6:]
      bot.send_message(chat_id = message.chat.id, text = "Height updated.")
    elif reply[:6] == "Weight":
      #update weight 
      user_info["weight"] = reply[6:]
      bot.send_message(chat_id = message.chat.id, text = "Weight updated.")
    elif msg['text'][:5] == "/back":
      bot.send_message(chat_id = message.chat.id, text = "Editing details complete. Please do something else. Type '/help' if you are not sure what to do.")
    else: 
      bot.send_message(chat_id = message.chat.id, text = "Invalid command.")
   
  #TODO after editing details update database and then reply user to say that details 
  #successfully changed 
  

stores = ["Science Canteen"]
#report
@bot.message_handler(commands = ['report'])
def select_canteen(message):
  chat_id = message.chat.id
  select_canteen_prompt = "You have chosen to report about a store's food portions. Select the canteen you ate from:\n"
  options = types.ReplyKeyboardMarkup()
  for store in stores: 
    options.row(types.KeyboardButton(store))
  
  canteen = bot.reply_to(message, select_canteen_prompt, reply_markup=options)
  bot.register_next_step_handler(canteen, process_canteens)
  # TODO implement a method called process_canteens

# help message
@bot.message_handler(commands = ['help'])
def launch_report(message):
  help_message = ""
  for command in commands:
    help_message += '/{} : {}\n'.format(command, commands[command])
    
    
  msg = bot.reply_to(message, help_message)
  
  
bot.polling()
