from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Settings:

    ENV = getenv('ENV')

    if ENV == 'prd':
        DATABASE_URL = getenv('DATABASE_URL_PRD')
    else:
        DATABASE_URL = getenv('DATABASE_URL_HML')
