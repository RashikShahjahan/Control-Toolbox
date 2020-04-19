# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:44:18 2020

@author: rashi
"""

from flask import render_template, request
from app import app
import control
from control.matlab import *
import matplotlib.pyplot as plt
import numpy as np
import math
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64


# ...
def to_array(str):
   list = str.split (",")
   li = []
   for i in list:
	   li.append(float(i))
   return li




@app.route('/', methods=['GET', 'POST'])

def home_page():
    errors = ""
    options = ['Step Response', 'damping', 'Poles', 'zeros', 'root locus', 'bode', 'nyquist', 'sisotool', 'dc gain', 'pole-zero plot','Impulse Response','gain and phase margins' ]
    if request.method == "POST":
        num = request.form["num"]
        den = request.form["den"]

        num1 = to_array(num)
        den1 = to_array(den)

        sys = tf(num1,den1)

        select = request.form.get('options')

        if select == 'Step Response':
             step = control.step_response(sys)
             plt.plot(step[0],step[1])
             img = io.BytesIO()
             plt.savefig(img, format='png')
             plt.clf()
             img.seek(0)
             plot_url = base64.b64encode(img.getvalue()).decode()
             return '<img src="data:image/png;base64,{}">'.format(plot_url)

        if select == 'Impulse Response':
             impulse = control.matlab.impulse(sys)
             plt.plot(impulse[0],impulse[1])
             img = io.BytesIO()
             plt.savefig(img, format='png')
             plt.clf()
             img.seek(0)
             plot_url = base64.b64encode(img.getvalue()).decode()
             return '<img src="data:image/png;base64,{}">'.format(plot_url)

        if select == 'pole-zero plot':
             pz = control.matlab.pzmap(sys, Plot=True, grid=True)
             img = io.BytesIO()
             plt.savefig(img, format='png')
             plt.clf()
             img.seek(0)
             plot_url = base64.b64encode(img.getvalue()).decode()
             return '<img src="data:image/png;base64,{}">'.format(plot_url)


        if select == 'damping':
            damp1 = damp(sys)
            natural_frequency = damp1[0]
            damping_ratio = damp1[1]

            return '''
                    <html>
                        <body>
                            <p>damping ratio = {damping_ratio}</p>
                            <p>natural frequency = {natural_frequency}</p>
                        </body>
                    </html>
                '''.format(damping_ratio=damping_ratio, natural_frequency=natural_frequency)

        if select == 'poles':
            poles = control.pole(sys)
            return '''
                      <html>
                          <body>
                              <p>The poles of the syestem are {poles}</p>
                              <p><a href="/">Click here to go to the main menu</a>
                          </body>
                      </html>
                   '''.format(poles=poles)

        if select == 'zeros':
            zeros = control.zero(sys)
            return '''
                      <html>
                          <body>
                              <p>The zeros of the syestem are {zeros}</p>
                              <p><a href="/">Click here to go to the main menu</a>
                          </body>
                      </html>
                  '''.format(zeros=zeros)

        if select == 'dc gain':
            dc_gain = control.matlab.dcgain(sys)
            return '''
                      <html>
                          <body>
                              <p>The dc gain of the syestem is {dc_gain}</p>
                              <p><a href="/">Click here to go to the main menu</a>
                          </body>
                      </html>
                  '''.format(dc_gain=dc_gain)

        if select == 'gain and phase margins':
            margins = control.matlab.margin(sys)
            return '''
                      <html>
                          <body>
                              <p>The gain and phase margins and crossover frequencies of the system are {margins}</p>
                              <p><a href="/">Click here to go to the main menu</a>
                          </body>
                      </html>
                  '''.format(margins=margins)

        if select == 'root locus':
            rlocus = control.matlab.rlocus(sys)
            plt.plot(rlocus[0],rlocus[1])
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.clf()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)

        if select == 'bode':
            bode = control.matlab.bode((sys))
            plt.plot(bode[0],bode[1])
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.clf()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)

        if select == 'nyquist':
            nyquist = control.matlab.nyquist((sys))
            plt.plot(nyquist[0],nyquist[1])
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.clf()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)

        if select == 'sisotool':
            sisotool = control.matlab.sisotool((sys))
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.clf()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)

    return render_template('options.html', errors=errors, options = options)
