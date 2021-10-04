import sys
sys.path.append("../")
import pytz as pytz
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta, time


from connector.mysql.source import GetData

tz = pytz.timezone('Asia/Shanghai')
dt = datetime.now(tz=tz) - timedelta(days=1)
utc_dt = dt.astimezone(pytz.utc).replace(tzinfo=None)


# 定义默认参数
default_args = {
    'owner': 'lwj',  # 拥有者名称
    'start_date': utc_dt,  # 第一次开始执行的时间，为格林威治时间，为了方便测试，一般设置为当前时间减去执行周期
    'retries': 1,  # 失败重试次数
    'retry_delay': timedelta(minutes=20)  # 失败重试间隔
}

# 定义DAG
dag = DAG(
    dag_id='bash_operator_test',
    default_args=default_args,
    schedule_interval="*/5 * * * *",
    catchup=False
)

start_run = DummyOperator(
    task_id='start_run',
    dag=dag,
)

# [START howto_operator_bash]
run_echo = BashOperator(
    task_id='run_echo',
    bash_command='echo 1',
    dag=dag,
)
# [END howto_operator_bash]

start_run >> run_echo

# [START howto_operator_python]
def print_context(ds, **kwargs):
    print(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'


run_python_print = PythonOperator(
    task_id='run_python_print',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)
# [END howto_operator_python]

run_echo >> run_python_print


# 连接mysql
getMysqlVersion = GetData().getMaysqlVersion()
run_python_connect_mysql = PythonOperator(
    task_id='run_python_connect_mysql',
    provide_context=True,
    python_callable=getMysqlVersion,
    dag=dag,
)

run_python_print >> run_python_connect_mysql