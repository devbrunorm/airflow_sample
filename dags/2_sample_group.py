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

with DAG(
    "tutorial_group",
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A simple tutorial DAG",
    schedule="0 0 * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    
    task_0 = DummyOperator(task_id = "start")

    task_1 = BashOperator(
        task_id="print_date",
        bash_command="sleep 5"
    )

    task_2 = PythonOperator(
        task_id="python_task",
        python_callable = sleep
    )

    task_3 = DummyOperator(task_id = "end")

    task_0 >> [task_1, task_2] >> task_3

    with TaskGroup(group_id="group") as group:
        task_4 = BashOperator(
            task_id="print_date",
            bash_command="sleep 5"
        )

        task_5 = PythonOperator(
            task_id="python_task",
            python_callable = sleep
        )

        task_3 >> group

