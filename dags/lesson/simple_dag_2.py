"""
DOC FROM BEGINING FILE
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from textwrap import dedent
from datetime import datetime, timedelta

default_args = {
    "depends_on_past": False,
    "email": ["daglar@dragomiroff.ru"],
    "email_on_retry": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "simple_dag_2",
    default_args=default_args,
    description="SIMLE DAG_2",
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
        # Title1
        ### Title3
        Hello, `world`!
        """
    )

    dag.doc_md = __doc__
    dag.doc_md = """
    DOC FROM MIDDLE FILE
    """

    temlated_command = dedent(
        """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7) }}"
        {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=temlated_command,
    )

    t1 >> [t2, t3]
