import os
import logging
from dotenv import load_dotenv
import random
import time

try:
    from google.cloud import storage
    import google.cloud.storage
    import json
    import os
    import sys
except Exception as e:
    print("Error : {} ".format(e))
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    start_time = time.time()
    folder_name = os.getenv('KEY_FOLDER_NAME')
    path = os.getcwd() + "/" + os.getenv('KEY_FOLDER_NAME')
    print(type(path))
    KEY_FILE_lOCATION = ''
    if os.path.isdir(path):
        get = os.listdir('keyFolder')
        KEY_FILE_lOCATION = KEY_FILE_lOCATION + str(get[0])
    else:
        print("folder not found")
    path = path + "/" + KEY_FILE_lOCATION
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

    storage_client = storage.Client(path)
    print(storage_client)

    try:
        bucket = storage_client.get_bucket(os.getenv("BUCHET_NAME"))
    except Exception as e:
        print("Connection Build Error")
    print("Connecion Build Success")


class DevelopmentConfig(Config):
    """
    Development Configuration
    """
    TESTING = True
    myValue = os.getenv("BUCHET_NAME")
    DEBUG = True
    ENV = 'development'
    DATABASE_USER = 'postgres'
    DATABASE_NAME = 'CR4'
    DATABASE_PASSWORD = '3366'
    DATABASE_URI = '127.0.0.1'
    DATABASE_PORT = 5432
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "app.log"
    LOG_TYPE = logging.DEBUG
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URI}:{DATABASE_PORT}/{DATABASE_NAME}"


class TestingConfig(Config):
    """
    Development Configuration
    """
    TESTING = True
    DEBUG = True
    ENV = 'development'
    DATABASE_USER = 'postgres'
    DATABASE_NAME = 'CR'
    DATABASE_PASSWORD = '3366'
    DATABASE_URI = '127.0.0.1'
    DATABASE_PORT = 5432
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "app.log"
    LOG_TYPE = logging.DEBUG
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URI}:{DATABASE_PORT}/{DATABASE_NAME}"


class ProductionConfig(Config):
    """
    Production Environment Config FIle Configuration
    Environment Required Variable:
        variable         :     operation                 :      example
    ==================================================================================================================
        DATABASE_USER    : export user name              :       "root"
        DATABASE_NAME    : export name                   :       "mydb"
        DATABASE_PASSWORD: export DATABASE_USER password :       "xyz"
        DATABASE_URI     : export databse URI            :       IP Address
        DATABASE_PORT    : export port                   :       "5432"
    ==================================================================================================================
    """
    TESTING = False
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_URI = os.environ.get("DATABASE_URI")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    LOG_FILE = "app.log"
    LOG_TYPE = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URI}:{DATABASE_PORT}/{DATABASE_NAME}"


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
