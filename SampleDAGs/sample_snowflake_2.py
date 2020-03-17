import snowflake.connector
from datetime import datetime, timedelta
from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import random

default_args = {
    'owner' : 'airflow',
    'retries' : 1,
    'retry_delay' : timedelta(minutes = 2),
    'email_on_failure' : True,
    'email_on_success' : True,
    'email' : ['karan.nadagoudar@datagrokr.com']
}

# Snowflake information
# Information must be stored in connections
# It can be done with Airflow UI - 
# Admin -> Connections -> Create
database_name = 'DEMO_DB'
table_name = 'public.stage_status'
snowflake_username = BaseHook.get_connection('snowflake_sql').login
snowflake_password = BaseHook.get_connection('snowflake_sql').password
snowflake_account = BaseHook.get_connection('snowflake_sql').host

dag = DAG(
    dag_id="sample_snowflake_2", 
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None
)

def insert(**context):
    con = snowflake.connector.connect(user = snowflake_username, \
        password = snowflake_password, account = snowflake_account, \
        database=database_name)
    cs = con.cursor()

    status_sql = """
insert into public.stage_status values ({}, '{}', 'create_file', 'success');
""".format(str(random.randint(0, 100)), str(datetime.now()))
    
    cs.execute(status_sql)
    cs.close()

def get_count(**context):
    con = snowflake.connector.connect(user = snowflake_username, \
        password = snowflake_password, account = snowflake_account,\
        database=database_name)
    cs = con.cursor()

    get_count_sql = "select count(*) from public.stage_status;"
    
    row_count = cs.execute(get_count_sql).fetchone
    print("public.stage_status has {} rows".format(str(row_count)))
    cs.close()


with dag:
    create_insert = PythonOperator(
        task_id="snowflake_insert",
        python_callable=insert
    )

    get_count = PythonOperator(
        task_id="get_count", 
        python_callable=get_count
    )

create_insert >> get_count