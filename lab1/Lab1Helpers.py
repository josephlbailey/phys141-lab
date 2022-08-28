#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022/08/28 15:16:20

@author: josephlbailey@arizona.edu

Code can also be found at: https://github.com/josephlbailey/phys141-lab
"""


def validate_input(num):
    try:
        return int(num)
    except:
        try:
            return float(num)
        except:
            raise Exception("Input was not a number")
