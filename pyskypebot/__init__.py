# -*- coding: utf-8 -*-
import threading
import time

import requests

from pyskypebot import apihelper


class SkypeBotApi:
    # https://docs.microsoft.com/en-us/azure/bot-service/rest-api/bot-framework-rest-connector-quickstart?view=azure-bot-service-3.0#get-token
    # https://docs.microsoft.com/en-us/azure/bot-service/rest-api/bot-framework-rest-connector-quickstart?view=azure-bot-service-3.0
    def __init__(self, client_id, client_secret):
        def token_func():
            global token
            payload = "grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret \
                      + "&scope=https%3A%2F%2Fapi.botframework.com%2F.default"
            response = requests.post(
                "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token?client_id=" + client_id
                + "&client_secret=" + client_secret
                + "&grant_type=client_credentials&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default",
                data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
            data = response.json()
            token = data["access_token"]

        def execute():
            while True:
                token_func()
                time.sleep(3000)

        self.t = threading.Thread(target=execute)
        self.t.daemon = True
        self.t.start()

    def send_message(self, service, sender, text):
        return apihelper.send_message(token, service, sender, text)

    def create_card_image(self, url, alt=None):
        return apihelper.create_card_image(url, alt)

    def create_buttons(self, type, title, value):
        return apihelper.create_buttons(type, title, value)

    def create_card_attachment(self, type, title, subtitle=None, text=None, images=None, buttons=None):
        return apihelper.create_card_attachment(type, title, subtitle, text, images, buttons)

    def create_animation(self, type, url, images, title=None, subtitle=None, text=None, buttons=None):
        return apihelper.create_animation(type, url, images, title, subtitle, text, buttons)

    def send_media(self, service, sender, type, url):
        return apihelper.send_media(token, service, sender, type, url)

    def send_card(self, service, sender, type, card_attachment, summary=None, text=None):
        return apihelper.send_card(token, service, sender, type, card_attachment, summary, text)

    # Not yet supported
    def send_action(self, service, sender):
        return apihelper.send_action(token, service, sender)
