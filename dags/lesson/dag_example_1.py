"""
DOC FROM BEGIN DOC
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from textwrap import dedent
from datetime import datetime, timedelta

with DAG(
    "tutorial",
    default_args={
        "depends_on_past": False,
        "email": ["daglar@dragomiroff.ru"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="DAG EXMAPLE_000",
    sheduler_interval=timedelta(days=1),
    starttime=datetime(2025, 1, 1),
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
        retries=3,
        bach_command="sleep 5",
    )

    t1.doc_md = dedent(
        """
        # Заголовок 1
        ### Заголовок 3
        Hello, `world`!
        """
    )

    dag.doc_md = __doc__
    dag.doc_md = """
    DOC FROM MIDDLE DOC
    """

    templated_command = dedent(
        """
        {% for in in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7) }}"
        {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_command,
    )

    t1 >> [t2, t3]
