import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-default')

    # SQL Server LocalDB Connection String from .env
    _server = os.getenv('DB_SERVER', r'(localdb)\MSSqlLocalDB')
    _database = os.getenv('DB_NAME', 'StudentManagementDB')
    _driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

    _params = urllib.parse.quote_plus(
        f"DRIVER={{{_driver}}};"
        f"SERVER={_server};"
        f"DATABASE={_database};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={_params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False