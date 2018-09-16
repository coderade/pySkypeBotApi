# pySkypeBotApi

A simple Skype bot wrapper using Python and Flask for the 
[Bot Connector/Rest service](https://docs.microsoft.com/en-us/azure/bot-service/rest-api/bot-framework-rest-connector-quickstart?view=azure-bot-service-3.0).


  * [Getting started.](#getting-started)
  * [Writing your first bot](#writing-your-first-bot)
    * [Prerequisites](#prerequisites)
    * [A simple echo bot](#a-simple-echo-bot)
  * [Examples](#examples)

## Status
[![Known Vulnerabilities](https://snyk.io/test/github/coderade/pySkypeBotApi/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/coderade/pySkypeBotApi?targetFile=requirements.txt)

## Getting started

This API is tested with the latest version of Python (3.6), Pypy and Pypy 3.
There are two ways to install the library:

* Installation using pip (a Python package manager)* **(ps. not available yet)**:

```
$ pip install pySkypeBotApi
```
* Installation from source (requires git):

```
$ git clone https://github.com/coderade/pySkypeBotApi.git
$ cd pySkypeBotApi
$ python setup.py install
```

It is generally recommended to use the first option.

**The API is not production-ready, but I will try to make this ASAP (You can too!). So it is not recommended to use in 
a Production environment yet**. 

## Writing your first bot

### Prerequisites

If you have not already done so, you must [register your bot](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-registration?view=azure-bot-service-3.0)
with the Bot Framework to obtain its App ID and password. You will need the bot's AppID and password to use this api.

### A simple echo bot

The SkypeBotApi class (defined in \__init__.py) encapsulates all API calls in a single class.

It provides functions such as `send_xyz` (`send_message`, `send_document` etc.) and several ways to listen for incoming messages.

Create a `.env` to put your `SKYPE_BOT_APP_ID` and `SKYPE_BOT_APP_SECRET` of your bot, also create a 
file called `send_message.py`.

Then, open the file and create an instance of the SkypeBotApi class.
```python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import json
from importlib import reload
import pyskypebot
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

reload(sys)

app = Flask(__name__)

APP_ID = os.getenv("SKYPE_BOT_APP_ID")
APP_SECRET = os.getenv("SKYPE_BOT_APP_SECRET")

bot = pyskypebot.SkypeBotApi(APP_ID, APP_SECRET)


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
                        bot.send_message(service, sender, "Hello World")

                else:
                    # private chat
                    sender = data['conversation']['id']
                    print(sender)
                    text = data['text']
                    bot.send_message(service, sender, "Hello World")
        except Exception:
            print(traceback.format_exc())  # something went wrong

```
*Note: Make sure to actually set `SKYPE_BOT_APP_ID` and `SKYPE_BOT_APP_SECRET` in the .env file.*

## Examples

You can found some examples of how handle a message in a private our group chats or how handle the conversations updates
like members removed aor added and how handle when the bot is added or removed in a private chat on the 
[send_message.py](examples/send_mensage.py) file on the [examples](examples) directory on this project.

### Another examples

#### Adding the Bot for a private conversation
Example of how handle when you add the bot as your contact

```
if data['type'] == 'contactRelationUpdate':
  if data['action']=='add':
        sender = data['conversation']['id']
        bot.send_message(sender,"Welcome! Thank you for adding me as your friend")
        pass
    elif data['action']=='remove':
        pass
    else:
        pass
```


#### Receiving a message in group
Example of how handle when you receive a message in a group that you have the bot as contact

```
if data['type'] =='message':
    if 'isGroup' in data['conversation'].keys():
        sender = data['conversation']['id']
```


#### Create buttons for the bot message
Example of how create buttons for the bot message

| Action Type   | Content of value property |
| ------------- |---------------------------|
| openUrl       | URL to be opened in the built-in browser.|
| imBack        | Text of message which client will sent back to bot as ordinary chat message. All other participants will see that was posted to the bot and who posted this. |
| call          | Destination for a call in following format: "tel:123123123123"   |
|showImage      |show image referenced by URL |

Tip : You can use meta tags in imBack action to send hidden information.

```
button1 = bot.create_buttons("imBack","test1","testing success")
button2 = bot.create_buttons("openUrl","test3","https://www.youtube.com/watch/?v=pAHjNyJHllc")
```


#### Sending attachments from your bot
Example of how send attachments from your bot

Attachments types:

1. Hero card
2. Thumbnail card
3. Carousel card (with hero or thumbnail images)
4. Sign in card - Not Implemented in this wrapper yet
5. Receipt card - Not implemented in this wrapper yet


##### Send a image attachment
```
def process_message(sender,text):

            button1 = bot.create_buttons("imBack","test1","testing success")
            button2 = bot.create_buttons("openUrl","test3","https://www.youtube.com/watch/?v=pAHjNyJHllc")
            
            url = 'https://d1u5p3l4wpay3k.cloudfront.net/zelda_gamepedia_en/thumb/3/30/HW_Link_Render.png/316px-HW_Link_Render.png'
            img1 = bot.create_card_image(url,alt="hello")
            
            #here in place of `hero` you can specify `thumbnail` to send thumnail card.  
            attachment1 = bot.create_card_attachment("hero","hero card test",subtitle="hero card subtitle",text="card text",images=[img1],buttons=[button1,button2])

            bot.send_card(sender,"carousel", [attachment1],text="hello")
```

#### Send a carousel attachment

```
def process_message(sender,text):

            button1 = bot.create_buttons("imBack","test1","testing success")
            button2 = bot.create_buttons("openUrl","test3","https://www.youtube.com/watch/?v=pAHjNyJHllc")
            
            url = 'https://i.ytimg.com/vi/EIu0_NVhrmM/hqdefault.jpg'
            img1 = bot.create_card_image(url,alt="hello")
            
            #here in place of `hero` you can specify `thumbnail` to send thumnail card.  
            attachment1 = bot.create_card_attachment("hero","hero card test",subtitle="hero card subtitle",text="card text",images=[img1],buttons=[button1,button2])

            bot.send_card(sender,"carousel", [attachment1,attachment1,attachment1,attachment1,attachment1],text="hello")
```

### Send a media attachment

| Property       | Description |
| ------------- |-------------|
| content type      | mimetype/contenttype of the URL |
| content url      |a link to the actual file  |

```
def process_message(sender,text):

  bot.send_media(sender,"image/jpg", 'http://foo.com/1312312 ')
```

## TODO

- Finish the tests 
- Create a initial release and a pip package

## Credits
This project is based on the [puneetsngh](https://github.com/puneetsngh) - [pythonSkypeBot](https://github.com/puneetsngh/pythonSkypeBot) 
for python 2.


