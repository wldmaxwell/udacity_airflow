from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
        :Param string redshift_conn_id: What Redshift Database are you connecting to.
        :Param string sql: What SQL command are you using for your quality test.
        :Param string expected_result: What do you want your query result to be for your quality check to pass.
    """
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id ="",
                 sql="",
                 expected_result="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        self.expected_result = expected_result
        

    def execute(self, context):
        self.log.info('Getting AWS Credentials.......')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('Done Getting Credentials')
        
        self.log.info("Running Quality Check .....")
        records = redshift_hook.get_records(self.sql)
        if records[0][0] != self.expected_result:
            raise ValueError(f"""
                Quality Check Failed. {records[0][0]} does not equal {self.expected_result}
                """)
        else:
            self.log.info("Quality Check Passed ....")
        
        