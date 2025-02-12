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

