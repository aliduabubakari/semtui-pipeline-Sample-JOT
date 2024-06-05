# load_and_modify.py

import pandas as pd
from IPython.display import display
from semtui_refactored.data_handler import DataHandler
from semtui_refactored.token_manager import TokenManager
from semtui_refactored.extension_manager import ExtensionManager
from semtui_refactored.reconciliation_manager import ReconciliationManager
from semtui_refactored.utils import Utility
from semtui_refactored.dataset_manager import DatasetManager
from semtui_refactored.semtui_evals import EvaluationManager
from semtui_refactored.data_modifier import DataModifier

# Set up the API URL and credentials
api_url = "http://192.168.99.175:3003/api/"  # Use the provided IP instead of localhost
username = "test"  # Username for authentication
password = "test"  # Password for authentication

# Initialize TokenManager
signin_data = {"username": username, "password": password}  # Payload for sign-in request
signin_headers = {
    "accept": "application/json",  # Specify the response format
    "content-type": "application/json"  # Specify the request content type
}
token_manager = TokenManager(api_url, signin_data, signin_headers)  # Create an instance of TokenManager

# Get token
token = token_manager.get_token()  # Retrieve the authentication token

# Initialize managers
reconciliation_manager = ReconciliationManager(api_url, token_manager)
dataset_manager = DatasetManager(api_url, token_manager)
evaluation_manager = EvaluationManager()
extension_manager = ExtensionManager(api_url, token)
data_modifier_manager = DataModifier()

# Path to your CSV file
csv_file_path = "JOT_data_tutorial_notebook_tiny.csv"  # Define the path to the CSV file

# Read CSV data
try:
    df = pd.read_csv(csv_file_path)
    print("CSV file imported successfully!")
    display(df.head())
except Exception as e:
    print(f"Error importing CSV file: {e}")

# Convert the 'Fecha_id' column to ISO date format
df = DataModifier.iso_date(df, date_col='Fecha_id')

# Add the table to the dataset
dataset_id = "30"  # Replace with the actual dataset ID
table_name = "New_JOT_tiny_3"  # Define the name of the new table to add
try:
    dataset_manager.add_table_to_dataset(dataset_id, df, table_name)
    print(f"Table '{table_name}' added to dataset ID {dataset_id} successfully.")
except Exception as e:
    print(f"Error adding table to dataset: {e}")
