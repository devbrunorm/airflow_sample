from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta

def sleep():
    import time
    time.sleep(10)

def print_number(number: int):
    print(f"Number: {number}")

def is_adult(name:str, age: int):
    if age >= 18:
        print(f"{name} é um adulto!")
    else:
        raise Exception (f"{name} é menor de idade!")

with DAG(
    "tutorial_for",
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    
    task_start = DummyOperator(task_id = "start")
    task_end = DummyOperator(task_id = "end")

    for i in range(10):
        task = PythonOperator(
            task_id=f"task_{i}",
            python_callable=print_number,
            op_kwargs={"number": i}
        )
        task_start >> task >> task_end

    task_start_age = DummyOperator(task_id = "start_age")
    task_end_age = DummyOperator(task_id = "end_age")

    for i in [
        {"name": "João", "age": 9}, 
        {"name": "Pedro", "age": 18}, 
        {"name": "Maria", "age": 16}, 
        {"name": "Joana", "age": 30},
        {"name": "José", "age": 25}
    ]:
        task = PythonOperator(
            task_id=f"task_check_{i['name']}",
            python_callable=is_adult,
            op_kwargs={
                "name": i["name"],
                "age": i["age"]
            },
            retries=0,
        )
        task_start_age >> task >> task_end_age
