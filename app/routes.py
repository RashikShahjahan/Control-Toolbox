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


# ...
def to_array(str):
   list = str.split (",")
   li = []
   for i in list:
	   li.append(int(i))
   return li


@app.route('/', methods=['GET', 'POST'])

def home_page():
    errors = ""
    options = ['Step Response', 'Properties', 'poles', 'zeros', 'root locus', 'bode', 'nyquist' ]
    if request.method == "POST":
        num = request.form["num"]
        den = request.form["den"]

        num1 = to_array(num)
        den1 = to_array(den)

        sys = tf(num1,den1)

        select = request.form.get('options')

        if select == 'Step Response':
             step = control.step_response(sys)
             display = plt.plot(step[0],step[1])
             #display = plt.show()

             return '''
                     <html>
                         <body>
                             <p>{display}</p>
                             <p><a href="/">Click here to go to the main menu</a>
                         </body>
                     </html>
                 '''.format(display=display)

        if select == 'properties':
            wn = math.sqrt(num1[0])
            zeta = den1[1]/(2*wn)
            settle_time = 4/(zeta*wn)
            percent_overshoot = 100*math.exp((-1*math.pi*zeta)/math.sqrt(1-zeta**2))
            peak_time = math.pi/(wn*math.sqrt(1-zeta**2))

            return '''
                    <html>
                        <body>
                            <p>wn = {wn}</p>
                            <p>zeta = {zeta}</p>
                            <p>Settling time = {settle_time}s</p>
                            <p>Percentage overshoot = {percent_overshoot}%</p>
                            <p>Peak time = {peak_time}s</p>
                            <p><a href="/">Click here to go to the main menu</a>
                        </body>
                    </html>
                '''.format(wn=wn, zeta=zeta, settle_time=settle_time, percent_overshoot=percent_overshoot, peak_time=peak_time )

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
                              <p>The zeros of the syestem are{zeros}</p>
                              <p><a href="/">Click here to go to the main menu</a>
                          </body>
                      </html>
                  '''.format(zeros=zeros)

        if select == 'root locus':
            rlocus = control.matlab.rlocus(sys)
            plt.plot(rlocus[0],rlocus[1])
            display = plt.show()
            return '''
                      <html>
                          <body>
                              <p>{display}</p>
                              <p><a href="/">Click here to go to the main menu</a>
                          </body>
                      </html>
                  '''.format(display=display)

        if select == 'bode':
            bode = control.matlab.bode((sys))
            plt.plot(bode[0],bode[1])
            display = plt.show()
            return '''
                          <html>
                              <body>
                                  <p>{display}</p>
                                  <p><a href="/">Click here to go to the main menu</a>
                              </body>
                          </html>
                      '''.format(display=display)

        if select == 'nyquist':
            nyquist = control.matlab.nyquist((sys))
            plt.plot(nyquist[0],nyquist[1])
            display = plt.show()
            return '''
                          <html>
                              <body>
                                  <p>{display}</p>
                                  <p><a href="/">Click here to go to the main menu</a>
                              </body>
                          </html>
                      '''.format(display=display)
    return render_template('options.html', errors=errors, options = options)
