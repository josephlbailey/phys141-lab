#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022/08/28 15:47:26

@author: josephlbailey@arizona.edu

Code can also be found at: https://github.com/josephlbailey/phys141-lab
"""

from Lab1Helpers import validate_input


def convert_the_temp(temp_f):
    if (temp_f < -459.67):
        print("Nice try. Enter a temperature above absolute zero")
        return

    temp_c = (5/9) * (temp_f - 32)
    temp_c_message = "Your converted temperature rounded to two decimal places: {:0.2f}\u00B0C"
    print(temp_c_message.format(temp_c))

    print("\nGoodbye")


try:
    print("Hello there.\nLet me convert your temperature from Fahrenheit to Celsius!\nWhat's the temperature (in degrees Fahrenheit) that you want to convert?")
    temp = validate_input(input("> "))
    convert_the_temp(temp)
except:
    print("Your entry was not a number")
