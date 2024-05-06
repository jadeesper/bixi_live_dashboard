import pandas as pd
import requests
from sqlalchemy import create_engine
from config.settings import BaseConfig


def get_stations_status():

    url_core="https://gbfs.velobixi.com/gbfs/en/station_status.json"
    
    response_core = requests.get(url_core)
    dict_core = response_core.json()

    stations_json = dict_core['data']['stations']
    data_stations=pd.json_normalize(stations_json)


    data_stations.drop(columns=["num_bikes_disabled","num_docks_disabled","eightd_has_available_keys",
                                    "is_charging","eightd_active_station_services"], inplace=True)
    
    return data_stations

def upload_data_to_db(table_name,dataframe):

    baseconfig_instance = BaseConfig()
    engine = create_engine(baseconfig_instance.sqlalchemy_connection)

    dataframe.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    dataframe.to_sql(name=table_name, con=engine, if_exists='append')
    
    return True

def upload_stations_info():
    table_name="bixi_stations_status"
    dataframe=get_stations_status()

    return upload_data_to_db(table_name,dataframe)
