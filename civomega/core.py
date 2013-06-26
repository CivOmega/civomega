import logging

from flask import Flask

from civomega import default_settings

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('DATAOMEGA_SETTINGS', silent=True)


# import this so the REGISTRY updates
#from civomega.modules import test_campaign_finance
from civomega.modules import census_population
from civomega.modules import bill_search
from civomega.modules import capitol_words
from civomega.modules import white_house_logs
from civomega.modules import werewolf
