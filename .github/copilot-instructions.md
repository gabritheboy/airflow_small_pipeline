# Copilot Instructions for mini_projet_airflow

## Project Overview
This project is a local development environment for Apache Airflow, orchestrating mock ETL workflows using Docker Compose. It leverages Airflow DAGs, Python, and the Moto library to simulate AWS S3 and Lambda interactions for testing and prototyping.

## Architecture & Key Components
- **Airflow Cluster**: Defined in `docker-compose.yaml` using CeleryExecutor, Redis, and PostgreSQL. Custom Airflow image built from `dockerfile`.
- **DAGs**: Located in `dags/`. Example DAGs:
  - `hello_variables_dag.py`: Demonstrates XCom usage for passing variables between tasks.
  - `mock_s3_dag.py`: Simulates S3 and Lambda with Moto, then processes data with Pandas.
- **Plugins**: Place custom Airflow plugins in `plugins/`.
- **Logs**: Airflow logs are stored in `logs/` and mapped via Docker volumes.
- **Tests**: Pytest-based tests in `tests/`, e.g., `test_mock_s3_dag.py`.

## Developer Workflows
- **Start Airflow**: Use `docker-compose up --build` to build and start all services. The webserver runs on port 8080.
- **Stop Airflow**: Use `docker-compose down`.
- **Run Tests**: Execute `pytest` in the project root. Tests use Moto to mock AWS services.
- **Install Python Dependencies**: Update `requirements.txt` and rebuild containers.

## Patterns & Conventions
- **Moto for AWS Mocking**: All S3 and Lambda interactions in DAGs/tests use Moto decorators (`@mock_s3`, `@mock_lambda`).
- **XCom for Data Passing**: Use `ti.xcom_push` and `ti.xcom_pull` for inter-task communication in DAGs.
- **No Scheduled DAGs**: DAGs use `schedule_interval=None` for manual triggering.
- **Custom Docker Image**: The Airflow webserver is built from the local `dockerfile` for extensibility.
- **Environment Variables**: Key settings (image name, user ID, etc.) are controlled via `.env` or directly in `docker-compose.yaml`.

## Integration Points
- **AWS SDK (boto3)**: Used for S3 and Lambda operations, always mocked in local/dev.
- **Pandas**: Used for data transformation in DAGs.
- **Databricks API**: Placeholder for future integration, currently mocked.

## Example: Mock S3 DAG
- Creates input/output buckets and uploads CSV using Moto/boto3.
- Triggers a mock Lambda, passes payload via XCom.
- Processes payload with Pandas, saves result to mock S3.

## Key Files
- `docker-compose.yaml`, `dockerfile`, `init_airflow.sh`: Environment setup.
- `dags/hello_variables_dag.py`, `dags/mock_s3_dag.py`: DAG logic and patterns.
- `requirements.txt`: Python dependencies.
- `tests/test_mock_s3_dag.py`: Example test structure.

## Tips for AI Agents
- Always use Moto for AWS mocking in local code/tests.
- Reference DAGs in `dags/` for task and XCom patterns.
- Use pytest for all new tests, following the structure in `tests/`.
- Update Docker image if adding new Python dependencies.

---
For questions or missing details, review the DAGs and test files for current conventions. Ask for feedback if any workflow or pattern is unclear or incomplete.
