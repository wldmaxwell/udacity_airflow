from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 # https://www.tutorialspoint.com/sql/sql-truncate-table.htm
                 redshift_conn_id = "",
                 table = "",
                 sql = "",
                 truncate=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        # 
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.truncate = truncate
            
    def execute(self, context):
        
        self.log.info('Getting AWS Credentails.....')
        redshift = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        
        if self.truncate:
            self.log.info(f'Truncating table {self.table}...')
            redshift.run(f'TRUNCATE {self.table}')
            self.log.info(f'Done Truncating {self.table}....')
        
        self.log.info(f'Loading JSON Data into {self.table}....')
        redshift.run(f'INSERT INTO {self.table} {self.sql}')
        self.log.info(f'Insert into {self.table} completed....')
