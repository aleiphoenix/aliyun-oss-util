# -*- coding: utf-8 -*-
from os.path import abspath, dirname, isfile, join
import pprint

from flask import Config

root = abspath(dirname(__file__))

config = Config('.')

fn = join(root, 'config.py')
print('loading config from {}'.format(fn))
config.from_pyfile(fn)

fn = join(root, 'config_local.py')
if isfile(fn):
    print('loading config from {}'.format(fn))
    config.from_pyfile(fn)


pprint.pprint(config)
