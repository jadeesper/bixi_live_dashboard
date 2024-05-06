#Verifier le timedelta en fonction des informations dans la table 

from airflow.operators.python import PythonOperator
from datetime import timedelta
from airflow import DAG
import pendulum
from info_task import upload_stations_info

# from dag_tasks import DagTasks  

default_args = {
    'owner': 'jade',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# Create an instance of the DagTasks class
# dag_tasks_instance = DagTasks()

# def upload_data():
#     return dag_tasks_instance.upload_data_to_db("bixi_stations_info", dag_tasks_instance.get_stations_status())



with DAG(
    dag_id="docks_info",
    schedule_interval=timedelta(seconds=60),
    start_date=pendulum.datetime(2024, 5, 5),
    catchup=False
) as dag:
    upload_info = PythonOperator(
        task_id="upload_docks_info",
        python_callable=upload_stations_info
        
    )

    upload_info
