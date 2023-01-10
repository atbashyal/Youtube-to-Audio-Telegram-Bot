import os
import telebot
import youtube_dl
import time
from dotenv import load_dotenv
import re

# load the bot token from environment variable
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)

# maximum file size allowed in bytes
MAX_FILE_SIZE = 20 * (1 << 20) # 20MB

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "To use this bot, send it a YouTube link and I will download the video for you.")

@bot.message_handler(func=lambda m: m.text and 'youtube.com' in m.text)
def download_audio(message):
    chat_id = message.chat.id
    youtube_url = message.text
    match = re.match(
        "(https?:\/\/www\.youtube\.com\/watch\?v=)[a-zA-Z0-9_-]{11}", youtube_url)
    if not match:
        bot.send_message(
            chat_id, "Sorry, it doesn't look like a valid YouTube link. Please try again.")
        return
    bot.send_message(chat_id, "Downloading audio, please wait...")
    artist_name = 'My artist name'
    album_name = 'My album name'
    
    # create a temporary directory to store the downloaded files
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'addmetadata': True,
        'metadata': {
            'artist': artist_name,
            'album': album_name,
        }
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            # download the video and extract info
            result = ydl.extract_info(youtube_url, download=True)
            
            # check if the file is an mp3, if not raise an exception
            # if not result["ext"] == "mp3":
            #     raise ValueError("The file is not an mp3 format")
                
            file_path = os.path.join(temp_dir, result['title']) + ".mp3"
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                raise ValueError("The file size is bigger than the allowed size")
            
            sent = False
            while not sent:
                try:
                    bot.send_audio(chat_id, open(file_path, 'rb'), title=result['title'], reply_to_message_id=message.message_id)
                    sent = True
                except telebot.apihelper.ApiException as e:
                    #if the file size was bigger than 20MB, then send message to user
                    if "file_size" in str(e):
                        bot.send_message(chat_id, "File size too big, the maximum allowed size is 20MB")
                        sent = True
                    # if the bot was blocked by telegram, sleep for 5 sec
                    elif "bot was blocked by the user" in str(e):
                        time.sleep(5)
                    # if the bot got a flood error, sleep for 30 sec
                    elif "flood" in str(e):
                        time.sleep(30)
                    # if it's another error, raise the exception
                    else:
                        raise e
        except youtube_dl.utils.ExtractorError:
            bot.send_message(chat_id, "Sorry, I couldn't find the video you requested. Please make sure you have entered a valid YouTube link.")
        except ValueError as e:
            bot.send_message(chat_id, str(e))
        except Exception as e:
            bot.send_message(chat_id, "An error occurred: "+str(e))
        finally:
            # delete the downloaded file and the temp dir
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass
            os.rmdir(temp_dir)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print("An error occurred: ", e)
        time.sleep(10) # Wait 10 seconds before trying again
