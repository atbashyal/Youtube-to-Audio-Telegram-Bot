# Youtube video to mp3 converter using Telegram Bot

## REQUIREMENTS
os <br>
telebot <br>
youtube_dl <br>
time <br>
dotenv<br>
re <br>

## WORKING
<b> Step 1: </b>The code starts by importing the necessary modules such as os, telebot, youtube_dl, time, and dotenv.<br><br>

<b> Step 2: </b>It then loads the bot token from the environment variable using the load_dotenv() function from the dotenv module and stores it in a variable called bot_token.<br><br>

<b> Step 3: </b>The code then initializes a telebot object using the bot_token and stores it in a variable called bot.<br><br>

<b> Step 4: </b>The code defines a function called send_welcome, which is triggered when the user sends the bot a /start or /help command. It replies to the user with a message that tells them how to use the bot.<br><br>

<b> Step 5: </b>The code defines another function called download_file, which is triggered when the user sends the bot a message containing a YouTube link. This function downloads the video or audio from the YouTube link, converts it to mp3 if necessary, and sends it to the user.<br><br>

<b> Step 6: </b>The download_file function starts by extracting the chat ID and YouTube link from the message object.<br><br>

<b> Step 7: </b>The function checks if the YouTube link contains '/a' or '/v' in its text. If '/a' is in the text, it assumes that the user wants to download the audio of the video, and if '/v' is in the text, it assumes that the user wants to download the video.<br><br>

<b> Step 8: </b>If '/a' is in the text, the function sends a message to the user saying that it is downloading the audio and sets some options for the youtube_dl module to extract the audio from the video and convert it to mp3 format. It also sets the output directory for the downloaded file.<br><br>

<b> Step 9: </b>If '/v' is in the text, the function sends a message to the user saying that it is downloading the video and sets some options for the youtube_dl module to download the best quality video and audio.<br><br>

<b> Step 10: </b>The function then calls the download_and_send_file function, which downloads the file using the youtube_dl module and sends it to the user using the telebot module. The function takes three arguments: the YouTube link, the youtube_dl options, and the chat ID.<br><br>

<b> Step 11: </b>The download_and_send_file function initializes a youtube_dl object with the specified options, passes in the YouTube link to the extract_info method, and sets download to True. This method downloads the video or audio and returns some information about the video.<br><br>

<b> Step 12: </b>The function checks if the downloaded file is an mp3 file, and if it is not, it raises a ValueError.<br><br>

<b> Step 13: </b>The function then checks the size of the downloaded file, and if it is greater than the maximum allowed size (20MB), it raises a ValueError.<br><br>

<b> Step 14: </b>If the downloaded file is an mp3 file and its size is less than or equal to the maximum allowed size, the function sends the file to the user using the bot.send_audio method.<br><br>

<b> Step 15: </b>The function handles any exceptions that may occur during the file sending process. If the file size is too big, it sends a message to the user saying that the file size is too big. If the bot is blocked by the user, it waits for 5 seconds before trying again. If the bot gets a flood error, it waits for 30 seconds before trying again. If it is another error, it raises the exception.<br><br>

<b> Step 16: </b>If the YouTube link is not valid or the video could not be found, the function sends a message to the user saying that it could not find the requested video.<br><br>

## RESULT
![image](https://user-images.githubusercontent.com/68748665/222450604-de9f2ae2-4254-4353-be1a-dfb801ead013.png)
