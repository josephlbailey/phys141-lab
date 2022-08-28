#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022/08/28 13:43:02

@author: josephlbailey@arizona.edu

Code can also be found at: https://github.com/josephlbailey/phys141-lab
"""

from Lab1Helpers import validate_input


def do_the_math(num1, num2):
    sum = num1 + num2
    product = num1 * num2

    sum_message = "Your two numbers added together: {:,}"
    print(sum_message.format(sum))

    product_message = "Your two numbers multiplied together: {:,}"
    print(product_message.format(product))

    print("\nGoodbye")


try:
    print("Hello there.\nLet me do some math for you!\nWhat's the first number?")
    num1 = validate_input(input("> "))
    print("What's the second number?")
    num2 = validate_input(input("> "))
    do_the_math(num1, num2)
except:
    print("Your entry was not a number")
