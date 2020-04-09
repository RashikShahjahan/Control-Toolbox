# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 23:27:31 2020

@author: rashi
"""

import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'