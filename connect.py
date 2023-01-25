from pymongo import MongoClient
from configparser import ConfigParser
import os

def connect():
    config = ConfigParser()
    config.read("config.cfg")    
    
    client = MongoClient(
                    config["fulltekst_api"]['host'],
                    username=config["fulltekst_api"]['username'],
                    password=config["fulltekst_api"]['pwd'],
                    # password=os.getenv("PASSWD"),
                    authSource=config["fulltekst_api"]['authSource'])

    return client

if __name__ == '__main__':
    print(connect())