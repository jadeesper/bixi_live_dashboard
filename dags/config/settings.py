import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    db_host = "postgres"
    db_port = 5432
    db_user = os.getenv('db_user')
    db_password = os.getenv('db_password')
    db_name = "airflow"

    @property
    def sqlalchemy_connection(self):
        return f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'



class DevConfig(object):
    db_host = "postgres"
    db_port = "5432"
    db_user = os.environ.get('db_user_dev')
    db_password = os.environ.get('db_password_dev')
    db_name = "bixi_dev"

class ProdConfig(object):
    db_host = "postgres"
    db_port = "5432"
    db_user = os.environ.get('db_user_prod')
    db_password = os.environ.get('db_password_prod')
    db_name = "bixi_prod"