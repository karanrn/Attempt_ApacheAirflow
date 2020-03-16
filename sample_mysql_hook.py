from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.dates import days_ago
import os

default_args = {
    'owner' : 'airflow',
    'retries' : 1,
    'retry_delay' : timedelta(minutes = 2),
    'email_on_failure' : True,
    'email_on_success' : True,
    'email' : ['karan.nadagoudar@datagrokr.com']
}

dag = DAG(
    'sample_mysql_hook',
    default_args=default_args,
    start_date=days_ago(1), #Start date for the workflow is neccesary
    description='An example MySQL hook',
    schedule_interval=timedelta(minutes=10)
    )   

def checkRecords(**kwargs):
    # Check for data, if present write results to file
    # If empty, log information to different file
    mysql_hook = MySqlHook(mysql_conn_id='local_mysql')
    # Table test1 contains list of postive integers
    sql = """
    select * from test1
    """
    records = mysql_hook.get_records(sql)
    # Pushing to Task instance
    if len(records) == 0:
        kwargs['task_instance'].xcom_push(key='check', value=False)
    else:
        kwargs['task_instance'].xcom_push(key='check', value=True)
        kwargs['task_instance'].xcom_push(key='recordcount', value=len(records))

def WriteToFile(**kwargs):
    # Path for output files
    path = '/home/karan/Attempt_ApacheAirflow/'
    file_name = kwargs['file_name']
    if kwargs['chk']:
        with open(path+file_name, "a+") as f:
            f.write("{}: {} records found for the day\n"\
                .format(str(datetime.now()), \
                str(kwargs['task_instance'].xcom_pull(task_ids='check_data_table', key='recordcount'))))
    else:
        with open(path+file_name, "a+") as f:
            f.write("{}: No records found for the day\n".format(str(datetime.now())))

def branching(**kwargs):
    check = kwargs['task_instance'].xcom_pull(task_ids='check_data_table', key='check')
    if check:
        return 'collect_data'
    else:
        return 'empty_table'

# Tasks
check_data = PythonOperator(
    task_id='check_data_table',
    python_callable=checkRecords,
    provide_context=True,
    dag=dag
)

empty_table = PythonOperator(
    task_id='empty_table',
    depends_on_past=False,
    python_callable=WriteToFile,
    op_kwargs={'file_name': 'empty_log.log', 'chk': False},
    provide_context=True,
    email=['karan.nadagoudar@datagrokr.com'],
    email_on_failure=True,
    dag=dag
)

collect_data = PythonOperator(
    task_id='collect_data',
    depends_on_past=False,
    python_callable=WriteToFile,
    op_kwargs={'file_name': 'data_log.log', 'chk': True},
    email=['karan.nadagoudar@datagrokr.com'],
    provide_context=True,
    email_on_failure=True,
    dag=dag
)

# Forking based on the condition
fork = BranchPythonOperator(
    task_id='branching',
    python_callable=branching,
    provide_context=True,
    dag=dag
)

check_data.set_downstream(fork)
fork.set_downstream(collect_data)
fork.set_downstream(empty_table)