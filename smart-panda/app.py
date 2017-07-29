#!/usr/bin/env python
import os
import yaml

from flask import Flask, request, redirect
from multiprocessing import Value

APP = Flask('smart-panda')
CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'config.yml')
COUNTER = Value('i', 0)


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
                On any other request then GET, will return different page
                (LMGTFY)
    """
    if request.method == 'POST':
        with COUNTER.get_lock():
            COUNTER.value += 1
    if request.method == 'GET':
        return str(COUNTER.value)
    else:
        # If request METHOD is not 'GET' then return LMGTFY redirection :)
        return redirect('http://lmgtfy.com/?t=i&q=panda')

APP.run(**CONFIG['flask'])
