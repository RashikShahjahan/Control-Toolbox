# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:52:00 2020

@author: rashi
"""

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["DEBUG"] = True


from app import routes
