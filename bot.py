import telebot
from telebot import types
import os
from models import *
# from dotenv import load_dotenv
from cedbDatabase import cedbDatabase
from ML_Controller import *

#API key for deployment
# API_KEY = os.environ['API_KEY']

load_dotenv()
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(API_KEY)

commands = {  # command description used in the "help" command
    'start': 'If you are a first time user of this bot, register yourself with this command!',
    'edit': 'Edits your user details',
    'recommend': 'Recommends food portion changes about meals in a canteen',
    'logmeal': 'Record down a meal that you had.',
    'help': 'Gives you information about the available commands',
    'report': 'Have feedback about food portions in NUS Canteens? Use this command to report about them!'
}

# keyboards
canteenKeyBoard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True, row_width=2)
canteenKeyBoard.add('Frontier @ Science', 'The Deck @ Arts')

# ML model
ML_Model = ML_Controller()
users_DB = cedbDatabase()
canteens = {}
reports = {}

# Configure the canteens
def initialiseCanteens():

    # Add Science Canteen + Stores
    scienceStores = ['Thai Food', 'Noodles']
    canteens['Frontier @ Science'] = scienceStores

     # Add Arts Canteen + Stores
    artsStores = ['Chicken Rice', 'Mala']
    canteens['The Deck @ Arts'] = artsStores


# A method to configure the keyboard indicating store names
def configureStoresKeyboard(selectedCanteen):
    storesKeyBoard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True, row_width=2)
    if (selectedCanteen == "Frontier @ Science"):
        storesKeyBoard.add('Thai Food', 'Noodles')
    else:
        storesKeyBoard.add('Chicken Rice', 'Mala')
    return storesKeyBoard

# A method to configure the keyboard indicating food names
def configureFoodKeyboard(selectedStore):
    foodKeyBoard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True, row_width=2)
    if (selectedStore == "Thai Food"):
        foodKeyBoard.add('Basil Rice', 'Pineapple Fried Rice', 'Pad Thai')
    elif (selectedStore == "Noodles"):
        foodKeyBoard.add('Wanton Mee', 'Ban Mee')
    elif (selectedStore == "Chicken Rice"):
        foodKeyBoard.add("Roasted Chicken Rice", "Chicken Rice Set")
    else:
        foodKeyBoard.add('Mala (S)', 'Mala (M)', 'Mala (L)')
    
    return foodKeyBoard

# start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    
    if (users_DB.is_first_time_user(chat_id)):
        user  = User(chat_id)
        users_DB.put(chat_id, user)
        msg = bot.reply_to(
            message, "We see that you are a first timer. We need to know some details from you. How old are you?")
        bot.register_next_step_handler(msg, process_age_step)
    else:
        msg = bot.reply_to(message, "Welcome back, use /recommend to get your food recommendation!")



# get age
def process_age_step(message):
  chat_id = message.chat.id
  age = message.text

  # Validation for age
  if not age.isdigit():
      msg = bot.reply_to(
          message, 'Age should be a positive number! Please try again with valid values.')
      bot.register_next_step_handler(msg, process_age_step)
      return

  user = users_DB.get(chat_id)
  user.age = age

  # Buttons to select Male or Female
  genderKeyBoard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True, row_width=2)
  genderKeyBoard.add('Male', 'Female')

  msg = bot.reply_to(message, 'What is your gender?', reply_markup=genderKeyBoard)

  bot.register_next_step_handler(msg, process_gender_step)

# get gender
def process_gender_step(message):
    chat_id = message.chat.id
    gender = message.text
    user = users_DB.get(chat_id)
    if (gender == u'Male') or (gender == u'Female'):
        user.gender = gender

    msg = bot.reply_to(
        message, 'How tall are you, in centimetres? Reply with a number, eg 145 for 145 cm.')
    bot.register_next_step_handler(msg, process_height_step)


# get height
def process_height_step(message):
    chat_id = message.chat.id
    height = message.text
    user = users_DB.get(chat_id)

    # Validation for height
    if not height.isdigit():
        msg = bot.reply_to(
            message, 'Height should be a positive number. Please try again with valid values.')
        bot.register_next_step_handler(msg, process_height_step)
        return
    
    user.height = float(height) / 100

    msg = bot.reply_to(message, 'What is your weight, in kg?')
    bot.register_next_step_handler(msg, process_weight_step)

# get weight
def process_weight_step(message):
    chat_id = message.chat.id
    weight = message.text
    user = users_DB.get(chat_id)

    # Validation for weight
    if not weight.isdigit():
        msg = bot.reply_to(
            message, 'Weight should be a positive number. Please try again with valid values.')
        bot.register_next_step_handler(msg, process_weight_step)
        return

    user.weight = int(weight, 10)

    msg = bot.reply_to(message, 'Great! You are now registered in our database with the following details:\n' + str(user))
    msg = bot.reply_to(message, 'To get started, use /recommend to get your food recommendation!')
 
# edit
@bot.message_handler(commands=['edit'])
def edit_details(message):
    # TODO retrieve current details from database
    text = """"Your current details are: 
          Age: 
          Gender: 
          Height: 
          Weight: 
          
          Type /back if you do not want to edit your details."""
    # display current details
    bot.reply_to(message, text)

    # TODO how do i get user input
    # TODO after editing details update database and then reply user to say that details
    # successfully changed
  
# recommend
@bot.message_handler(commands=['recommend'])
def start_recommendation(message):
    msg = bot.reply_to(message, 
        "Let's start recommending you some food! Where are you eating today?", 
        reply_markup=canteenKeyBoard)
    bot.register_next_step_handler(msg, process_stall)

def process_stall(message):
    selectedCanteen = message.text
    stores = canteens[selectedCanteen]
    storesKeyBoard = configureStoresKeyboard(selectedCanteen)
    msg = bot.reply_to(message, 'Which store are you eating from?', reply_markup=storesKeyBoard)
    bot.register_next_step_handler(msg, process_food)

def process_food(message):
    selectedStore = message.text
    # TODO Find a way to add food w/o having to hardcode
    foodKeyBoard = configureFoodKeyboard(selectedStore)
    msg = bot.reply_to(message, 'Which food item are you having?', reply_markup=foodKeyBoard)
    bot.register_next_step_handler(msg, recommend_food)


def recommend_food(message):
    food_item = message.text
    chat_id = message.chat.id
    user = users_DB.get(chat_id)

    gender = user.gender 
    weight = user.weight
    height = user.height
    recommendation = ML_Model.provideRecommendation(gender, weight, height, food_item)
    bot.reply_to(message, recommendation)


#report
@bot.message_handler(commands = ['report'])
def start_report(message):
  chat_id = message.chat.id
  report = Report(chat_id)
  reports[chat_id] = report
  select_canteen_prompt = "You have chosen to report about a store's food portions. Select the canteen you ate from:\n"
  canteen = bot.reply_to(message, select_canteen_prompt, reply_markup=canteenKeyBoard)
  bot.register_next_step_handler(canteen, process_canteen)

# get store
def process_canteen(message):
    chat_id = message.chat.id
    selectedCanteen = message.text
    report = reports[chat_id]
    report.canteen = selectedCanteen

    stores = canteens[selectedCanteen]
    storesKeyBoard = configureStoresKeyboard(selectedCanteen)
    msg = bot.reply_to(message, 'Which store are you eating from?', reply_markup=storesKeyBoard)
    bot.register_next_step_handler(msg, process_store)


def process_store(message):
    store = message.text
    chat_id = message.chat.id
    report = reports[chat_id]
    report.store = store
    msg = bot.reply_to(message, 
        "Which food item did you have?")
    bot.register_next_step_handler(msg, report_food)

def report_food(message):
    chat_id = message.chat.id
    report = reports[chat_id]
    selectedStore = report.store
    report.food_item = message.text

    foodKeyBoard = configureFoodKeyboard(selectedStore)
    msg = bot.reply_to(message, 'From a scale of 1 to 10, rate how full you are after eating the food. 1 means too little food, 10 means too much.', reply_markup=foodKeyBoard)
    bot.register_next_step_handler(msg, process_fullness_rating)


def process_fullness_rating(message):
    chat_id = message.chat.id
    report = reports[chat_id]
    fullness_rating = int(message.text, 10)
    report.fullness_rating = fullness_rating

    if fullness_rating < 1 or fullness_rating > 10:
        msg = bot.reply_to(message, "The rating should be an integer from 1 to 10 (inclusive). Please rate again with valid values")
        bot.register_next_step_handler(msg, process_fullness_rating)

    
    bot.register_next_step_handler(message, process_report)

def process_report(message):
    chat_id = message.chat.id
    report = reports[chat_id]
    user = users_DB.get(chat_id)

    gender = user.gender 
    height = user.height
    weight = user.weight
    food_item = report.food_item
    fullness = report.fullness_rating
    ML_Model.addUserReport(gender, height, weight, food_item, fullness)

    bot.reply_to(message, "Thank you for making the following rating: \n" + str(report))

# help message
@bot.message_handler(commands = ['help'])
def launch_report(message):
  help_message = ""
  for command in commands:
    help_message += '/{} : {}\n'.format(command, commands[command])

  msg = bot.reply_to(message, help_message)
  
initialiseCanteens()
try:  
    bot.polling()
except:
    bot.polling()
