# reconciliation.py

import pandas as pd
import json
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

# Add the table to the dataset
dataset_id = "30"  # Replace with the actual dataset ID
table_name = "New_JOT_tiny_3"  # Define the name of the new table to add

# Retrieve the table data
try:
    table_data = dataset_manager.get_table_by_name(dataset_id, table_name)  # Attempt to retrieve the specified table from the dataset
    if table_data:
        print(f"Table '{table_name}' retrieved successfully!")  # Print success message if table is retrieved
        # No need to display the DataFrame
    else:
        print(f"Table '{table_name}' not found in the dataset.")  # Print message if table is not found
except Exception as e:
    print(f"Error retrieving table '{table_name}': {e}")  # Print error message if retrieving the table fails

# Define reconciliation parameters
column_name = "City"  # Define the column name to be reconciled
id_reconciliator = "geocodingHere"  # Define the ID of the reconciliator

# Reconcile the column
try:
    reconciled_table = reconciliation_manager.reconcile(table_data, column_name, id_reconciliator)  # Attempt to reconcile the specified column
    if reconciled_table:
        print("Column reconciled successfully!")  # Print success message
        # Save the reconciled table as JSON locally
        with open('reconciled_table.json', 'w') as f:
            json.dump(reconciled_table, f)
        print("Reconciled table saved as 'reconciled_table.json'")  # Confirm that the table is saved
    else:
        print("Failed to reconcile column.")  # Print failure message if reconciliation fails
except Exception as e:
    print(f"Error reconciling column: {e}")  # Print error message if reconciliation fails
