# -*- coding: utf-8 -*-

import sys
import traceback
import json
from imp import reload
import pyskypebot

from flask import Flask, request

reload(sys)

app = Flask(__name__)

client_id = ''
client_secret = ''

bot = pyskypebot.SkypeBotApi(client_id, client_secret)


@app.route('/', methods=['POST'])
def main():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            service = data['serviceUrl']
            if data['type'] == 'message':

                if 'isGroup' in data['conversation'].keys():
                    sender = data['conversation']['id']
                    text = data['text']

                    # do what ever you want to do here for GROUPS
                    process_messages(sender, text, service)

                else:
                    # private chat
                    sender = data['conversation']['id']
                    print(sender)
                    text = data['text']
                    process_messages(sender, text, service)

            elif data['type'] == 'conversationUpdate':
                sender = data['conversation']['id']
                if 'membersRemoved' in data.keys():
                    left_member = data['recipient']['name']

                    print("""The {member} has been removed from the group""".format(member=left_member))

                elif 'membersAdded' in data.keys():
                    member = data['recipient']['name']

                    print("""The {member} has been removed from the group""".format(member=member))

                    bot.send_message(service, sender,
                                     "Hi, I am emoji bot. I can transform your text in messages to emojies. "
                                     "I also have an emoji game to play simply send @emojirobor #emojigame")
                else:
                    pass
            elif data['type'] == 'contactRelationUpdate':

                # bot added for private chat
                if data['action'] == 'add':

                    sender = data['conversation']['id']
                    bot.send_message(service, sender, "Hi, I am a bot.")
                    pass
                elif data['action'] == 'remove':
                    pass
                else:
                    pass

            else:
                pass
        except Exception as e:
            print(traceback.format_exc())  # something went wrong

    return 'Ok'


# Set a simple Hello word message
def process_messages(sender, text, service):
    bot.send_message(service, sender, "Hello World")


if __name__ == '__main__':
    # The context is needed if you are running with SSL, but not needed if you are running locally and using ngrok.
    # context = ('/etc/ssl/localcerts/mycert.pem', '/etc/ssl/localcerts/mykey.key')
    app.run(host='127.0.0.1', port=8080, debug=True)
