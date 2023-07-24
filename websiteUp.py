import json
import requests
from bs4 import BeautifulSoup
import datetime


# Current Date
def log_execution_time(filename):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_string = f"Executed from date {current_time}\n"
    with open(filename, 'a') as log_file:
        log_file.write(log_string)

# Send Telegram Notification
def telegram_bot_sendtext(bot_message):
    bot_token = 'BOT-TOKEN-HERE'
    bot_chatID = 'CHAT-ID-HERE'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()
# 

# Get Page Title
def get_title(url):
    try:
        # Fetch the HTML content of the page
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title tag content
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.text.strip()

    except requests.RequestException as e:
        # Handle any request-related errors (e.g., connection errors)
        print(f"Error: {e}")

    return None

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    websites_to_check = config["websites"]
    log_file_name = "logs.txt"
    log_execution_time(log_file_name)
    
    for website_url in websites_to_check:
        title = get_title(website_url)
        if title:
            print(f"The title of {website_url} is: {title}")
        else:
            print(f"Failed to retrieve the title of {website_url}.")
            telegram_bot_sendtext("Websites is dow: "+website_url)

