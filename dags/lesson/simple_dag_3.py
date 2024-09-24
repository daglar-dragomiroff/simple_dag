"""
DOC FROM BEGINING DOC
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from textwrap import dedent
from datetime import datetime, timedelta

default_args = {
    "depends_on_past": False,
    "email": ["daglar@dragomiroff.ru"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "simple_dag_3",
    default_args=default_args,
    description="SIMPLE DAG_3",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )

    t1.doc_md = dedent(
        """
        # title 1
        ### title 3
        hello, `World`!
        """
    )

    dag.doc_md = __doc__
    dag.doc_md = """
    DOC FROM MIDDLE DOC
    """

    templated_commad = dedent(
        """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds   , 7) }}"
        {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_commad,
    )

    def print_context(ds, **kwargs):
        print(f"ds={ds}")
        print(f"kwargs={kwargs}")
        return "It' PRINT CONTEXT!"

    t4 = PythonOperator(
        task_id="print_context",
        python_callable=print_context,
    )

    t1 >> [t2, t3] >> t4
