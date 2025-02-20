from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta

def exception_sample():
    raise Exception("Errou feio, errou rude!")

with DAG(
    "tutorial_exception",
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

    task_1 = PythonOperator(
        task_id="python_task",
        python_callable = exception_sample,
        retries=3,
        retry_delay=timedelta(seconds=5)
    )

    task_all_success = DummyOperator(
        task_id = "end_all_success",
        trigger_rule = "all_success"
    )

    task_all_done = DummyOperator(
        task_id = "end_all_done",
        trigger_rule = "all_done"
    )

    task_after_all_success = BashOperator(
        task_id = "task_after_all_success", bash_command = "echo 'Deu bom em todas!'"
    )

    task_after_all_done = BashOperator(
        task_id = "task_after_all_done", bash_command = "echo 'Deu bom em algumas só!'"
    )

    task_0 >> task_1 >> [task_all_success, task_all_done]
    task_all_success >> task_after_all_success
    task_all_done >> task_after_all_done