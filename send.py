import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = '832441474:AAGeWzau9CZxInYkFmislgmnrK0vj8GzNGw'
    chat_id = '-1001407136445'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    
    response = requests.get(send_text)
    
    return response.json()

