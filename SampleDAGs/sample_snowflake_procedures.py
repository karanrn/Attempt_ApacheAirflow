import logging
import snowflake.connector
from datetime import datetime, timedelta
from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow import AirflowException

# Logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
schema_name = 'public'
snowflake_username = BaseHook.get_connection('snowflake_sql').login
snowflake_password = BaseHook.get_connection('snowflake_sql').password
snowflake_account = BaseHook.get_connection('snowflake_sql').host

dag = DAG(
    dag_id="sample_snowflake_procedures", 
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None
)

def load_merge_table(**context):
    con = snowflake.connector.connect(user = snowflake_username, \
        password = snowflake_password, account = snowflake_account, \
        database=database_name, schema=schema_name)
    cs = con.cursor()

    status_sql = "call mergetableProc();"
    
    status = cs.execute(status_sql).fetchall()[0][0]

    cs.close()

    if status == 'Done.':
        logger.info("Procedure executed successfully")
    else:
        logger.error("Procedure failed with {}".format(str(status)))
        raise AirflowException("Failed procedure run.")
    

def drop_merge_table(**context):
    con = snowflake.connector.connect(user = snowflake_username, \
        password = snowflake_password, account = snowflake_account,\
        database=database_name, schema=schema_name)
    cs = con.cursor()

    get_count_sql = "call dropmergetableProc();"
    
    status = cs.execute(get_count_sql).fetchall()[0][0]

    cs.close()

    if status == 'Done.':
        logger.info("Procedure executed successfully")
    else:
        logger.error("Procedure failed with {}".format(str(status)))
        raise AirflowException("Failed procedure run.")


with dag:
    load_table = PythonOperator(
        task_id="load_merge_table",
        python_callable=load_merge_table
    )

    drop_table = PythonOperator(
        task_id="drop_merge_table", 
        python_callable=drop_merge_table
    )

load_table >> drop_table