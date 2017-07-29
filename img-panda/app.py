#!/usr/bin/env python
import os
import random
import yaml

from flask import Flask, request, redirect
from flask import send_from_directory

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'resources')
CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'config.yml')
APP = Flask('img-panda')


def get_config(config_file=CONFIG_PATH):
    with open(config_file, 'r') as f:
        config = yaml.load(f)
        return config

CONFIG = get_config()


@APP.before_request
def redirect_request_to_index():
    """
    This method will be call on every before every request to the website
    :return:    On GET request, returns a random image of Panda
                On any other request then GET, will return different page (LMGTFY)
    """
    if request.method == 'GET':
        img = random.choice(os.listdir(RESOURCES_DIR))
        return send_from_directory(RESOURCES_DIR, img)
    else:
        # If request METHOD is not 'GET' then return LMGTFY redirection :)
        return redirect('http://lmgtfy.com/?t=i&q=panda')


APP.run(**CONFIG['flask'])
