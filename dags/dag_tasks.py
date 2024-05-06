import pandas as pd
import requests
from sqlalchemy import create_engine
from config.settings import BaseConfig

class DagTasks:

    def __init__(self,url="https://gbfs.velobixi.com/gbfs/en/"):
        self.url = url

    def _transform_data(self,api_data):

        url_core = self.url + api_data
        
        response_core = requests.get(url_core)
        dict_core = response_core.json()

        stations_json = dict_core['data']['stations']
        return pd.json_normalize(stations_json)
    
    def get_stations_status(self):

        df_stations_status=self._transform_data("station_status.json")

        df_stations_status.drop(columns=["num_bikes_disabled","num_docks_disabled","eightd_has_available_keys",
                                        "is_charging","eightd_active_station_services"], inplace=True)

        return df_stations_status
    
    def get_stations_info(self):

        df_stations_info=self._transform_data("station_information.json")

        df_stations_info.drop(columns=["external_id","short_name","rental_methods",
                                        "electric_bike_surcharge_waiver","is_charging",
                                        "eightd_has_key_dispenser","has_kiosk",
                                        "eightd_station_services"], inplace=True)

        return df_stations_info


    def upload_data_to_db(table_name,dataframe):

        baseconfig_instance = BaseConfig()
        engine = create_engine(baseconfig_instance.sqlalchemy_connection)

        dataframe.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        dataframe.to_sql(name=table_name, con=engine, if_exists='append')
        
        return True
    
# if __name__=="__main__":
#     DagTasks_instance=DagTasks()
#     DagTasks_instance.upload_data_to_db("bixi_stations_status",DagTasks_instance.get_stations_status())
#     DagTasks_instance.upload_data_to_db("bixi_stations_info",DagTasks_instance.get_stations_info())