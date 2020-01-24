import os

from behave import *
from splinter.browser import Browser
import logging

# Configure things to be used later
# For user data, URLs, etc
from features.logging_handler import loggerDEBUG


def set_context(context):
  context.userdata = {
    'preferred_language': 'en'
  }
  context.basicurl = "http://127.0.0.1:5000"
  # context.basicurl = 'http://18.185.125.231:8080'

# def after_step(context, step):
  # if step.status == "failed":
  #   screenshot_filename = os.path.abspath('screenshot\screenshot')
  #   screenshot_path = context.browser.screenshot(screenshot_filename)
  #   loggerDEBUG.error("Screenshot for the acusing page %s", screenshot_path)


# Runs before any steps
def before_all(context):
  context.browser = Browser(driver_name='chrome')
  # logformat = '%(levelname)s:%(asctime)s:%(relativeCreated)d:%(message)s'
  # logfilename = './mylogging.log'
  # loglevel = logging.INFO
  # logging.basicConfig(filename=logfilename,level=loglevel,format=logformat)
  # logging.info("Things have started")
  set_context(context)

def after_all(context):
  context.browser.quit()