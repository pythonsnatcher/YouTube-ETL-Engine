# YouTube-ETL-Engine

# YouTube Data ETL with Apache Airflow on EC2

This project automates the extraction, transformation, and loading (ETL) of YouTube comment data using Apache Airflow on an AWS EC2 instance. The data is extracted from the YouTube Data API, transformed, and then stored in Amazon S3.

## Project Structure

- **youtube_dag.py**: Defines the Airflow DAG that schedules and manages the ETL process.
- **youtube_api_etl_2.py**: Contains the main ETL script that interacts with the YouTube API and processes the data.
- **.env**: Stores environment variables, including the YouTube API key.

## Prerequisites

- **AWS Account**: Access to launch and manage EC2 instances.
- **YouTube API Key**: Obtain a key from the Google Developer Console.

## EC2 Setup Instructions

1. **Create an EC2 Key Pair:**
   - In the AWS Management Console, navigate to EC2 > Key Pairs.
   - Create a new key pair and download the `.pem` file. This file is used to SSH into your EC2 instance.

2. **Launch EC2 Instance:**
   - Choose an appropriate AMI (e.g., Ubuntu 20.04).
   - Select an instance type (e.g., t2.medium) with sufficient resources.
   - Configure security groups to allow SSH (port 22) and Airflow web server access (port 8080).
   - Select the key pair you created for SSH access.

3. **SSH into the EC2 Instance:**
   ```bash
   ssh -i <your-key.pem> ubuntu@<ec2-public-ip>
   ```

4. **Update and Install Dependencies:**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv
   ```

5. **Set Up a Virtual Environment:**
   ```bash
   python3 -m venv airflow_venv
   source airflow_venv/bin/activate
   ```

6. **Install Apache Airflow:**
   ```bash
   export AIRFLOW_HOME=~/airflow
   pip install apache-airflow
   ```

7. **Initialize Airflow Database:**
   ```bash
   airflow db init
   ```

8. **Deploy the DAG:**
   - Copy `youtube_dag.py` and `youtube_api_etl_2.py` to the Airflow DAGs directory:
   ```bash
   cp /path/to/your/youtube_dag.py ~/airflow/dags/
   cp /path/to/your/youtube_api_etl_2.py ~/airflow/dags/
   ```

9. **Start Airflow Services:**
   ```bash
   airflow webserver --port 8080 &
   airflow scheduler &
   ```

10. **Trigger the DAG:**
    - Manually trigger the DAG using the CLI:
    ```bash
    airflow dags trigger youtube_dag
    ```

## Data Storage

- **Raw Data**: Stored in `youtube_raw_data.json` in the specified S3 bucket.
- **Transformed Data**: Stored in `youtube_transformed_data.json` in the same S3 bucket.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Apache Airflow](https://airflow.apache.org/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
