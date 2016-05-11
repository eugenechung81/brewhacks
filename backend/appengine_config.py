# coding: utf-8
"""
This module inserts third party libraries into Google's python PATHs
In production we import this from lib.zip file, whereas in development
from main/lib folder
"""
import os
import sys

# sys.path.insert(0, './pylibs')
# sys.path.insert(0, '~/.virtualenv/brewhacks/lib/python2.7/site-packages')
sys.path.insert(0, '/home/eugene/.virtualenvs/brewhacks/lib/python2.7/site-packages/')
