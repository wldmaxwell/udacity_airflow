
**Project Three: Data Pipeline With Airflow and Redshift**

 

**Overview**

This project builds an Airflow ETL Data Warehouse Pipeline for a music streaming company called Sparkify. This project aims to create improved automation, monitored, and data quality checks for Sparkify's ETL Pipeline. ”

**Technologies used**



*   SQL -
    *   Used for creating, inserting, copying JSON files, and running test queries 
*   Python 
    * Used to Create Airflow Operators and Functions  
*   Redshift
    *   Data Warehouse used to Stage data from S3 and create dimension tables for analytics team
*   S3 
    *   Storage service that holds event and song data JSON files
* Apache Airflow
    * Workflow Managment Tool

**How to Run**



*   AWS 
    *   Create an IAM user 
        *   With permissions to use Redshift
    *   Create IAM role for Redshift with AmazonS3ReadOnlyAccess rights
    *   Create the Redshift cluster
        *   Get the Endpoint ---- also known as Host
*   Airflow
    * Set up Connection for AWS
        * Conn Id: Enter aws_credentials.
        * Conn Type: Enter Amazon Web Services.
        * Login: Enter your Access key ID from the IAM User credentials
        * Password: Enter your Secret access key from the IAM User credentials
     * Set up Redshift Connection
        * Conn Id: Enter redshift.
        * Conn Type: Enter Postgres.
        * Host: Enter the endpoint of your Redshift cluster, excluding the port at the end.
        * Schema: Enter dev. This is the Redshift database you want to connect to.
        * Login: Enter awsuser.
        * Password: Enter the password you created when launching your Redshift cluster.
        * Port: Enter 5439. 

**Information About Dataset**



*   s3://udacity-dend/song_data
    *   31 JSON files
*   **Song_Data Example**






![alt_text](images/Song_Data.png "image_tooltip")




*   s3://udacity-dend/log_data
    *   14897 JSON files
*   **Log_Data Example**






![alt_text](images/Log_Data.png "image_tooltip")




*   Staging_events_table
    *   8056 rows
*   Staging_songs_table
    *   14896 rows
*   User_table
    *   104 Unique Users
*   Song_table
    *   14896 Unique Songs
*   Artist_table
    *   10025 Unique Artist
*   Songplay table
    *   9957 song plays

**Test Query from sql_queries.py**

*   **Query:** 

		SELECT count(*)
		     
		FROM songplays

		WHERE playid

		is null;



*   **Expected Query Result:** 0
	* If query result is not 0 throw Error "Quality Check Failed. {records[0][0]} does not equal {self.expected_result}"

**Database Info and Tables**


*   **Redshift Cluster Info:** 
    *   DWH_CLUSTER_TYPE=multi-node
    *   DWH_NUM_NODES=4
    *   DWH_NODE_TYPE=dc2.large


![alt_text](images/Staging_Tables.png "image_tooltip")



![alt_text](images/Analytics_Tables.png "image_tooltip")

