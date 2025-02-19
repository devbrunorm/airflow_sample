from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def random_number(ti):
    from random import randint
    number = randint(10)
    print(f"O número escolhido foi: {number}")
    ti.xcom_push(key='number', value=number)

def sum_numbers(ti):
    numbers = ti.xcom_pull(key='number', task_ids=[f'generate_random_number_{i}' for i range(2)])
    print(f"A soma dos números é de {sum(numbers)}")

with DAG(
    "tutorial_xcom",
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    
    print_sum = PythonOperator(
        task_id="sum_numbers",
        python_callable=sum_numbers
    )

    for i in range(2):
        random_number = PythonOperator(
            task_id=f"generate_random_number_{i}",
            python_callable=random_number
        )
