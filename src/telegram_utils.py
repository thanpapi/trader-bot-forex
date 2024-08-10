import requests

TELEGRAM_TOKEN = '7430415385:AAGXJRFEJtbqdGdTEsayKB5tmN16wXOLeYU'
CHAT_ID = '915854855'
          # MI ID PERSONAL 915854855
          #ID GRUPO -1002165469196
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"Message sent: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        if response:
            print(f"Response content: {response.content}")
