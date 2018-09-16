# -*- coding: utf-8 -*-
import requests
import sys
from importlib import reload

reload(sys)


# text should be UTF-8 and has a 320 character limit

def send_message(token, service, sender, text):
    try:
        payload = {
            "type": "message",
            "text": text
        }
        r = requests.post(service + 'v3/conversations/' + sender + '/activities/',
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
                          json=payload)
        print(r)
    except Exception as e:
        print(e)
        pass


def create_buttons(type, title, value):
    buttons_dict = {
        "type": type,
        "title": title,
        "value": value
    }

    return buttons_dict


def create_card_image(url, alt):
    img_dict = {
        "url": url,
        "alt": alt
    }
    return img_dict


def create_card_attachment(type, title, subtitle, text, images, buttons):
    card_attachment = {
        "contentType": "application/vnd.microsoft.card." + type,
        "content": {
            "title": title,
            "subtitle": subtitle,
            "text": text,
            "images": images,
            "buttons": buttons
        }
    }

    return card_attachment


def send_media(token, service, sender, type, url):
    try:
        response = requests.get(url).content
        payload = {
            "type": "message",
            "attachments": [{
                "contentType": type,
                "contentUrl": url
            }]
        }

        r = requests.post(service + '/v3/conversations/' + sender + '/activities/',
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
                          json=payload)
        print(r)
    except Exception as e:
        print(e)
        pass


def send_card(token, service, sender, type, card_attachment, summary, text):
    try:
        payload = {"type": "message",
                   "attachmentLayout": type,
                   "summary": summary, "text": text,
                   "attachments": card_attachment
                   }

        r = requests.post(service + '/v3/conversations/' + sender + '/activities/',
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
                          json=payload)
        print(payload)
        print(r)
    except Exception as e:
        print(e)
        pass


# typing action not yet supported

def send_action(token, service, sender):
    try:
        payload = {
            "type": "typing"
        }
        r = requests.post(service + '/v3/conversations/' + sender + '/activities/',
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
                          json=payload)
        print(payload)
        print(r)
    except Exception as e:
        print(e)
        pass


def create_animation(type, url, images, title, subtitle, text, buttons):
    card_animation = {
        "contentType": "application/vnd.microsoft.card." + type,
        "content": {
            "autoloop": True,
            "autostart": True,
            "shareable": True,
            "media": [{"profile": "gif", "url": url}],
            "title": title,
            "subtitle": subtitle,
            "text": text,
            "images": images,
            "buttons": buttons
        }
    }

    return card_animation
