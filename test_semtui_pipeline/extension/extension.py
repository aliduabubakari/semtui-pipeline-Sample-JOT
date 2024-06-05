# extension.py

import pandas as pd
from semtui_refactored.data_handler import DataHandler
from semtui_refactored.token_manager import TokenManager
from semtui_refactored.extension_manager import ExtensionManager
from semtui_refactored.reconciliation_manager import ReconciliationManager
from semtui_refactored.utils import Utility
from semtui_refactored.dataset_manager import DatasetManager
from semtui_refactored.semtui_evals import EvaluationManager
from semtui_refactored.data_modifier import DataModifier
import json

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

# Load the reconciled table from the JSON file
with open('reconciled_table.json', 'r') as f:
    reconciled_table = json.load(f)

reconciliated_column_name = 'City'  # Column that contains reconciled IDs
properties = ["apparent_temperature_max", "apparent_temperature_min", "precipitation_sum"]  # Replace with actual properties to extend
date_column_name = "Fecha_id"  # Replace with actual date column name
id_extender = "meteoPropertiesOpenMeteo"  # ID for Open Meteo Properties extender

try:
    extended_table = extension_manager.extend_column(
        reconciled_table['raw'], 
        reconciliated_column_name, 
        id_extender, 
        properties, 
        date_column_name=date_column_name,  # Pass date_column_name as a keyword argument
        weather_params = properties, 
        new_columns_name = properties
    )  # Attempt to extend the specified column

    if extended_table:
        print("Column extended successfully!")  # Print success message

        # Import the Utility class
        from semtui_refactored.utils import Utility

        # Convert JSON to DataFrame
        extended_df = Utility.load_json_to_dataframe(extended_table, georeference_data=True)  # Load the extended data into a DataFrame

        print("Extended data loaded into DataFrame successfully!")  # Print success message

        # Save the extended DataFrame as a CSV file
        extended_df.to_csv('extended_table.csv', index=False)
        print("Extended table saved as 'extended_table.csv'")  # Confirm that the table is saved

    else:
        print("Failed to extend column.")  # Print failure message if extension fails

except Exception as e:
    print(f"Error extending column: {e}")  # Print error message if extending column fails
