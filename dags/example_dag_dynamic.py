from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator

## Define JSON Variable
CUSTOMERS_LIST = [
    {
        'customer_name': 'Customer One',
        'customer_id': '123487fhg',
        'email': ['admin@customer_one.com'],
        'schedule_interval': None,
        'enabled': True
    },
    {
        'customer_name': 'Customer two',
        'customer_id': '098765fght',
        'email': ['admin@customer_two.com'],
        'schedule_interval': '@once',
        'enabled': True
    }
]

CUSTOMERS = Variable.get(
    "customer_list", default_var=CUSTOMERS_LIST, deserialize_json=True)


def create_dag(customer):
    """
    Takes a cust parameters dict, uses that to override default args creates DAG object
    
    Returns: DAG() Object
    """
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email': 'test@test.com',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'start_date': datetime(2021, 8, 1, 0, 0),
        'end_date': None
    }

    # To allow DAG parameters to be passed in from the Variable if a customer needs something specific overridden in their DAG
    replaced_args = {k: default_args[k] if customer.get(
        k, None) is None else customer[k] for k in default_args}


    dag_id = '{base_name}_{id}'.format(
        base_name='load_data', id=customer['customer_id'])

    return DAG(dag_id=dag_id, default_args=replaced_args, schedule_interval=customer['schedule_interval'], tags=['example', 'example_dynamic'])

# Loop the list of customers
for cust in CUSTOMERS:
    if cust['enabled']:
        dag = create_dag(cust)
        globals()[dag.dag_id] = dag

        extract = DummyOperator(
            task_id='extract',
            dag=dag
        )

        transform = DummyOperator(
            task_id='transform',
            dag=dag
        )

        load = DummyOperator(
            task_id='load',
            dag=dag
        )

        extract.set_downstream(transform)
        transform.set_downstream(load)

    else:
        pass