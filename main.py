from re import A
import telebot
import pandas as pd
from telebot import types

token="my token"
bot=telebot.TeleBot(token)

# vocabulary csv file
df = pd.read_csv('vocab.csv')

# word adding block
# -----------------
isAsken = False

@bot.message_handler(commands = ['add'])    
def askAddWord(message):
    global isAsken
    msg = bot.send_message(message.chat.id, 'Enter the word: ')
    bot.register_next_step_handler(msg, askAddTrans)
    df.loc[len(df.index)] = [1, 1, 1]
    isAsken = True
def askAddTrans(message):
    global isAsken
    if isAsken:
        msg = bot.send_message(message.chat.id, 'Enter the translation: ')
        bot.register_next_step_handler(msg, askAddType)
        df.word[len(df.index) - 1] = message.text       
def askAddType(message):
    global isAsken
    if isAsken:
        msg = bot.send_message(message.chat.id, 'Choose the type: noun/verb/adjective')
        bot.register_next_step_handler(msg, saveAddedWord)
        df.translation[len(df.index) - 1] = message.text
def saveAddedWord(message):
    global isAsken
    if isAsken:
        df.type[len(df.index) - 1] = message.text
        df.to_csv('vocab.csv', index=False)
        isAsken = False
# -----------------

# show list of words
# -----------------
@bot.message_handler(commands = ['show'])
def askTypeWords(message):
    msg = bot.send_message(message.chat.id, 'Choose the the type: ')
    bot.send_message(message.chat.id, 'Types: noun/adjective/verb')
    bot.register_next_step_handler(msg, showList)
def showList(message):
    if message.text in ['noun', 'adjective', 'verb']:
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
    msg = bot.send_message(message.chat.id, 'Write the word you want to delete: ')
    bot.register_next_step_handler(msg, deleteWord)
def deleteWord(message):
    if (df.word.eq(message.text)).any():
        df.drop(df[df.word == message.text].index, inplace=True, axis=0)
        df.to_csv('vocab.csv', index=False)
        bot.send_message(message.chat.id, 'The word was removed!')
    else:
        bot.send_message(message.chat.id, 'There is no such word in dictionary!')
# -----------------

# words learning
@bot.message_handler(commands = ['learn'])
def askLearnType(message):
    msg = bot.send_message(message.chat.id, 'Choose the the type: ')
    bot.send_message(message.chat.id, 'Types: noun/adjective/verb')
    bot.register_next_step_handler(msg, learnWords)   
def learnWords(message):
      pass
def on():
    pass


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
