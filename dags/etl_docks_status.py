from airflow.operators.python import PythonOperator
from datetime import timedelta
from airflow import DAG
import pendulum
# from dag_tasks import DagTasks  
from status_task import upload_stations_info

default_args = {
    'owner': 'jade',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# # Create an instance of the DagTasks class
# dag_tasks_instance = DagTasks()

# def upload_data():
#     return dag_tasks_instance.upload_data_to_db("bixi_stations_status", dag_tasks_instance.get_stations_status())


with DAG(
    dag_id="docks_status",
    schedule_interval=timedelta(seconds=60),
    start_date=pendulum.datetime(2024, 5, 5),
    catchup=False
) as dag:
    upload_status = PythonOperator(
        task_id="upload_docks_status",
        python_callable=upload_stations_info
        
    )

    upload_status





        
