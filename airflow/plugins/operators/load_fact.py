from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """
        :Param redshift_conn_id: What Redshift Database are you connecting to.
        :Param table: Staging table name you are loading data into.
        :Param sql: SQL Command to Load data into dimension tables from staging tables.
   
    """

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id = "",
                 table = "",
                 sql = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql

    def execute(self, context):
        self.log.info('Setting up AWS Connections.... ')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Loading JSON Data into Fact Tables in Redshift")
        redshift_hook.run(f'INSERT INTO {self.table} {self.sql}') 
        self.log.info(f'Insert into {self.table} completed ... ')
