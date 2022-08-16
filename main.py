from re import A
import telebot
import pandas as pd
from telebot import types

token="5466738128:AAH0alQqffVY1NcpEHccT0NCuo1z0pRLDtk"
bot=telebot.TeleBot(token)

# vocabulary csv file
df = pd.read_csv('vocab.csv')
userinfo = pd.read_csv('userinfo.csv')

# start block
# -----------------
@bot.message_handler(commands = ['start'])
def start(message):
    if not (userinfo.userid.eq(message.from_user.id)).any():
        userinfo.loc[len(df.index)] = [message.from_user.id, 0, 0]
        userinfo.to_csv('userinfo.csv', index=False)
        bot.send_message(message.chat.id, 'You have successfully registered! Try to "/add" new word.')
    else:
        bot.send_message(message.chat.id, 'You already registered! Try to "/add" new word.')
# -----------------

# word adding block
# -----------------
@bot.message_handler(commands = ['add'])
def askAddWord(message):
    if (userinfo.userid.eq(message.from_user.id)).any():
        msg = bot.send_message(message.chat.id, 'Enter the word: ')
        bot.register_next_step_handler(msg, askAddTrans)
        df.loc[len(df.index)] = [1, 1, 1, message.from_user.id]
    else:
        bot.send_message(message.chat.id, 'First of all, you should register (/start)')
def askAddTrans(message):
    msg = bot.send_message(message.chat.id, 'Enter the translation: ')
    bot.register_next_step_handler(msg, askAddType)
    df.word[len(df.index) - 1] = message.text       
def askAddType(message):
    df.translation[len(df.index) - 1] = message.text
    msg = bot.send_message(message.chat.id, 'Choose the type (e.g. noun/verb):')
    bot.register_next_step_handler(msg, saveAddedWord)
def saveAddedWord(message):
    df.type[len(df.index) - 1] = message.text
    userinfo['words count'][userinfo.userid == message.from_user.id] += 1
    df.to_csv('vocab.csv', index=False)
    userinfo.to_csv('userinfo.csv', index=False)
# -----------------

# show list of words
# -----------------
@bot.message_handler(commands = ['show'])
def askTypeWords(message):
    if (userinfo.userid.eq(message.from_user.id)).any():
        msg = bot.send_message(message.chat.id, 'Choose the the type: ')
        bot.send_message(message.chat.id, 'Your types: ' + str(list(df[df.userid == message.from_user.id].type.unique())))
        bot.register_next_step_handler(msg, showList)
    else:
        bot.send_message(message.chat.id, 'First of all, you should register (/start)')
def showList(message):
    if message.text in list(df[df.userid == message.from_user.id].type.unique()):
        words = list(df[df.type == message.text].word)
        translations = list(df[df.type == message.text].translation)
        for i in range(len(words)):
            words[i] = words[i] + ' - ' + translations[i]
        bot.send_message(message.chat.id, '\n'.join(words))
    else:
        bot.send_message(message.chat.id, 'There is an error in your type!')
# -----------------

# words deleting
# -----------------
@bot.message_handler(commands = ['remove'])
def askDeleteWord(message):
    if (userinfo.userid.eq(message.from_user.id)).any():
        msg = bot.send_message(message.chat.id, 'Write the word you want to delete: ')
        bot.register_next_step_handler(msg, deleteWord)
    else:
        bot.send_message(message.chat.id, 'First of all, you should register (/start)')
def deleteWord(message):
    if (df.word.eq(message.text)).any():
        df.drop(df[df.word == message.text].index, inplace=True, axis=0)
        df.to_csv('vocab.csv', index=False)
        bot.send_message(message.chat.id, 'The word was removed!')
    else:
        bot.send_message(message.chat.id, 'There is no such word in dictionary!')
# -----------------

# words checking
# -----------------
@bot.message_handler(commands = ['learn'])
def askLearnType(message):
    msg = bot.send_message(message.chat.id, 'Choose the the type: ')
    bot.send_message(message.chat.id, 'Types: noun/adjective/verb')
    bot.register_next_step_handler(msg, learnWords)   
def learnWords(message):
    msg = bot.send_message(message.chat.id, df.word.sample(n=1))
    bot.send_message(message.chat.id, 'Enter the translation: ')
    bot.register_next_step_handler(msg, checkAnswer)
def checkAnswer(message):
    pass
# -----------------







# # type adding
# # -----------------
# @bot.message_handler(commands = ['addtype'])
# def askAddNewType(message):
#     msg = bot.send_message(message.chat.id, 'Write the type you want to add: ')
#     bot.register_next_step_handler(msg, addNewType)
# def addNewType(message):
#     if not (df.type.eq(message.text)).any():
#         df.loc[len(df.index)] = [1, 1, message.text, message.from_user.id]
#         bot.send_message(message.chat.id, 'Congratulations! You have added new type!')

# ------------------
# @bot.message_handler(commands = ['addword'])
# def addword(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
#     bt1 = types.KeyboardButton("add new word")
#     markup.add(bt1)
#     bot.send_message(message.chat.id,'Выберите что вам надо', reply_markup=markup)
# ------------------
# class Word:
#     def __init__(self,word):
#         self.word = word
    
#     def getWord(self):
#         return self.word
    
#     def setWord(self, word):
#         self.word = word

# word1 = Word("hello")
# word1.getWord()
# ------------------

bot.infinity_polling()
