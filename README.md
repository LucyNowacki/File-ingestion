# File-Ingestion Project
Compares different approaches to loading and processing large CSV files.


## Overview
This project demonstrates various methods to handle, process, and validate large CSV files in Python, using pandas and other tools. It provides insights into writing efficient data processing scripts, validating data schema against predefined configurations, and using Git and GitHub for version control.

## Features
- **Data Loading and Processing**: Utilize pandas to load and process large datasets efficiently.
- **Data Validation**: Implement checks to ensure the data matches a predefined schema specified in a YAML file.
- **File Compression**: Techniques to write data to a compressed format to save space and ensure faster transmission.
- **Git Integration**: Using Git for version control and GitHub for remote storage and sharing of the code.

## Technologies Used
- Python
- pandas for data manipulation
- YAML for configuration management
- Git for version control
- GitHub for online repository hosting

## Setup and Installation
Optionally you should integrate Python with the Hadoop connection
Ensure you have Python installed on your system, along with pandas and PyYAML libraries. You can install the required packages using pip:


```bash
pip install pandas pyyaml modin pyspark parquet polars datatable
