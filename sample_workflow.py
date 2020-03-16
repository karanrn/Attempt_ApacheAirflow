from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import os
import random
# from write_date_to_file import WriteToFile

default_args = {
    'owner' : 'airflow',
    'retries' : 1,
    'retry_delay' : timedelta(minutes = 2),
    'email_on_failure' : True,
    'email_on_success' : True,
    'email' : ['karan.nadagoudar@datagrokr.com']
}

# Path for output files
path = '/home/karan/Attempt_ApacheAirflow/'

dag = DAG(
    'sample_workflow',
    default_args=default_args,
    start_date=days_ago(1), #Start date for the workflow is neccesary
    description='A sample workflow',
    schedule_interval=timedelta(minutes=10)
)

# task 1
command1 = """
echo "Time: $(date)" >> /home/karan/Attempt_ApacheAirflow/t1.log
"""
t1 = BashOperator(
    task_id='print_date',
    depends_on_past=False,
    bash_command=command1,
    # email=['karan.nadagoudar@datagrokr.com'],
    # email_on_failure=True,
    # email_on_success=True,
    dag=dag
)

# task 2
command2 = """
touch /home/karan/Attempt_ApacheAirflow/t2-$(date +"%T").log
"""
t2 = BashOperator(
    task_id='create_file',
    depends_on_past=False,
    bash_command=command2,
    dag=dag
)
t2_complete = datetime.now()

# task 3 - python function
def WriteToFile():
    dir_path = '/home/karan/Attempt_ApacheAirflow/'
    file_name = 't3.log'
    full_path = dir_path + file_name
    f = open(full_path, "a+")
    f.write("T3 Time start: {}\n".format(str(datetime.now())))
    f.close()

t3 = PythonOperator(
    task_id='python_write_file',
    depends_on_past=False,
    python_callable=WriteToFile,
    email=['karan.nadagoudar@datagrokr.com'],
    email_on_failure=True,
    dag=dag
)

t3_complete = datetime.now()
t3_status_sql = """
insert into stage_status values (3, '{}', 'python_create_file', 'success'),
(2, '{}', 'create_file', 'success');
""".format(str(t3_complete), str(t2_complete))

t4 = MySqlOperator(
    task_id='Update_status_table',
    sql=t3_status_sql,
    mysql_conn_id='local_mysql',
    owner='airflow',
    dag=dag
)
# Dependancy
t1 >> [t2, t3] >> t4