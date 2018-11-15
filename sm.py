import json
import datetime

def load_sm_data():
    try:
        with open('sm.json') as data_file:
            sm_data = json.load(data_file)
            return sm_data
    except (IOError, ValueError):
        filex = open('sm.json', "w")
        filex.write('{"Home":{"water": {}, "gas": {},"electricity":{}}, "Work":{"water": {}, "gas": {},'
                    '"electricity":{}}, "Other":{"water": {}, "gas": {},"electricity":{}}}')
        filex.close()
        with open('sm.json') as data_file:
            sm_data = json.load(data_file)
            return sm_data

load_sm_data()