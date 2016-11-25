# coding: utf-8

from os import path
from logging import getLogger

from jinja2 import Template, Environment, FileSystemLoader

logger = getLogger()

env = Environment(loader=FileSystemLoader(path.join(path.dirname(__file__), 'templates'), encoding='utf8'))


def root():
    template = env.get_template('index.html')
    return template.render()

def handle(event, context):
    logger.info(event)
    return root()
