import pandas as pd
import requests
import json
from bing_image_downloader import downloader
import telebot
import time

telegram_token = '5645219403:AAEoP4HG-9gj46ldZ4UozyPVCbnQYbJNxE4'
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start','help'])
def first_messsage(message):
    bot.reply_to(message, 'Hello there! :) Please choose one ore more ingredients for your desired cocktail. If more than one, please seperate them by "," : ')

@bot.message_handler(func = cocktail_api_response)
def cocktail_api_response(message):
    cocktail_url = 'https://api.api-ninjas.com/v1/cocktail?ingredients={}'.format(message.text)
    cocktail_api_headers = {'X-Api-Key': 'xxYE7P+HqeMKJmQNERD2TA==GjxmHax6p8mgatbE'}
    response = requests.get(cocktail_url, headers=cocktail_api_headers)
    try:
        bot.reply_to(message, 'The list of cocktails on its way! :)')
        json_response = json.loads(response.text)
        df = pd.DataFrame(json_response)
        output_dir = []
        for row in df.itertuples():
            downloader.download(row[3] +" Cocktail", limit=1, output_dir=r'C:\Users\lirir\Downloads'+"\\"+str(row[3]+" Cocktail"),
            adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
            output_dir.append(r'C:\Users\lirir\Downloads'+"\\"+str(row[3]+" Cocktail")+"\\"+str(row[3]+" Cocktail"))
        df["output_dir"] = output_dir
        df['ingredients'] = [' , '.join(map(str, l)) for l in df['ingredients']]
        top_3_df = df.head(3)
        list_df = []
        list_df.append(top_3_df)
        print(list_df[0])
        for row in list_df[0].itertuples():
            bot.reply_to(message, 'The cocktails name:\n' + "" + row[3].capitalize()) #name
            time.sleep(1)
            bot.reply_to(message, 'The cocktails ingredients:\n' + "" + row[1].capitalize()) #ingredients
            time.sleep(1)
            bot.reply_to(message, 'The cocktails preperation instructions:\n' + "" + row[2].capitalize()) #instructions
            time.sleep(1)
            bot.send_photo(message.chat.id, photo=open(r'C:\Users\lirir\Downloads'+"\\"+str(row[3]+" Cocktail")+"\\"+str(row[3]+" Cocktail")+"\\"+"Image_1.jpg", 'rb'))
    except:
        bot.reply_to(message, 'We could not find you a relevant cocktail :(')


bot.infinity_polling()