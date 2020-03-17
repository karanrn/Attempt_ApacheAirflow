from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner' : 'airflow',
    'retries' : 1,
    'retry_delay' : timedelta(minutes = 2),
    'email_on_failure' : True,
    'email_on_success' : True,
    'email' : ['karan.nadagoudar@datagrokr.com']
}

dag = DAG(
    dag_id="sample_snowflake", 
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None
)

status_sql = """
insert into public.stage_status values (101, '{}', 'create_file', 'success');
""".format(str(datetime.now()))

def row_count(**context):
    dwh_hook = SnowflakeHook(snowflake_conn_id="snowflake_sql")
    result = dwh_hook.get_first("select count(*) from public.stage_status")
    print("Number of rows in `public.test_table`  - %s", result[0])


with dag:
    create_insert = SnowflakeOperator(
        task_id="snowflake_insert",
        sql=status_sql,
        snowflake_conn_id="snowflake_sql",
    )

    get_count = PythonOperator(
        task_id="get_count", 
        python_callable=row_count
    )

create_insert >> get_count