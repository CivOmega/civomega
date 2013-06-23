import logging

from flask import Flask

from dataomega import default_settings

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('DATAOMEGA_SETTINGS', silent=True)


# import this so the REGISTRY updates
from dataomega.modules import test_campaign_finance
