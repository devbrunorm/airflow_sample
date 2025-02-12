from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta

def print_connection():
    from airflow.hooks.base import BaseHook
    conn = BaseHook.get_connection("sample_conn")
    print(f"Login: {conn.login}")
    print(f"Password: {conn.password}")

def print_variable(variable: str):
    from airflow.models import Variable
    from airflow.exceptions import AirflowSkipException

    try:
        print(f"Variable {variable}: {Variable.get(variable)}")
    except:
        raise AirflowSkipException

with DAG(
    "tutorial_variables",
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
    
    conn_task = PythonOperator(
        task_id="print_connection",
        python_callable=print_connection
    )

    for var in ["sample_var", "secret_var", "null_var"]:
        var_task = PythonOperator(
            task_id=f"print_{var}",
            python_callable=print_variable,
            op_kwargs={"variable": var}
        )
