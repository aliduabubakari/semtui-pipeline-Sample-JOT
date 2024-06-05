# SEMTUI Pipeline Project

## Overview

This project is designed to automate data processing, reconciliation, and extension using the SEMTUI framework. The pipeline consists of three main steps:
1. **Loading and Modifying Data**
2. **Reconciling Data**
3. **Extending Data**

The pipeline is orchestrated using Docker Compose to ensure each step is executed in the correct order.

## Prerequisites

- Docker and Docker Compose installed on your machine
- Python 3.x installed
- Internet connection for fetching dependencies

## Directory Structure

Create the following directory structure to store the necessary files and outputs:

project_folder/
|-- load_and_modify.py
|-- Dockerfile
|-- requirements.txt
|-- JOT_data_tutorial_notebook_tiny.csv
|-- docker-compose.yml
|-- reconciled_table.json
|-- reconciliation/
|   |-- Dockerfile
|   |-- reconciliation.py
|   |-- requirements.txt
|-- extension/
    |-- Dockerfile
    |-- extension.py
    |-- requirements.txt



## Docker Compose Configuration

Create a `docker-compose.yml` file in the root directory of your project with the following content:

```yaml
version: '3.8'
services:
  load_and_modify:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: load_and_modify_container
    volumes:
      - .:/app
    networks:
      - my_network

  reconciliation:
    build:
      context: ./reconciliation
      dockerfile: Dockerfile
    container_name: reconciliation_container
    volumes:
      - ./reconciliation:/app  # Map the reconciliation folder correctly
    networks:
      - my_network
    depends_on:
      - load_and_modify

  extension:
    build:
      context: ./extension
      dockerfile: Dockerfile
    container_name: extension_container
    volumes:
      - ./extension:/app  # Map the extension folder correctly
      - ./reconciliation/reconciled_table.json:/app/reconciled_table.json:ro  # Ensure it can access reconciled_table.json as a file
    networks:
      - my_network
    depends_on:
      - reconciliation

networks:
  my_network:
    driver: bridge
```

## Running the Pipeline

1. **Clone the Repository**

   Clone this repository to your local machine.

   ```sh
   git clone https://github.com/your-repository/semtui_pipeline.git
   cd semtui_pipeline
   ```

2. **Build and Run the Docker Containers**

   Use Docker Compose to build and run the containers:

   ```sh
   docker-compose up --build
   ```

4. **Check Output**

   After the pipeline completes, the extended CSV file will be available in the specified output directory:


## Troubleshooting

- If the pipeline fails at any step, check the logs of the respective container for error messages:
  
  ```sh
  docker logs <container_name>
  ```

- Verify that all necessary directories exist and are correctly mapped in the Docker Compose file.

## Conclusion

This setup ensures a streamlined and automated workflow for data processing, reconciliation, and extension using the SEMTUI framework. By following the steps outlined in this guide, you can efficiently manage and execute the data pipeline.
