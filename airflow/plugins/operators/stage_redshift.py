from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    copy_sql = """
            COPY {}
            FROM '{}'
            ACCESS_KEY_ID '{}'
            SECRET_ACCESS_KEY '{}'
            REGION AS '{}'
            FORMAT AS json '{}'

        """

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # redshift_conn_id=your-connection-name
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 copy_json_option="",
                 region="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.copy_json_option = copy_json_option
        self.region = region

    def execute(self, context):

        
        # Setting up AWS/Redshift Connections and Clearing table 
        self.log.info('Setting Up AWS Connections.....')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info(f'Clearing Data from {self.table}...')
        redshift.run(f'DELETE FROM {self.table}')
        self.log.info(f'Done Clearing Data from {self.table}')

        # Copying Data From S3 to Redshift

        self.log.info('Copying Data from S3 to Redshift...')
        s3_rendered_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{s3_rendered_key}"
        

        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.copy_json_option
        )
        self.log.info("Starting S3 to Redshift Copy Operation...")
        redshift.run(formatted_sql)
        self.log.info("Done with Redshit Copy Operation...")










