import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# Create a dictionary of usernames and passwords
users = {
    "john": "password123",
    "jane": "password456"
}

# Define a function to check if the username and password are valid
def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    else:
        return False

# Define a function to generate the dataframe for a given user
def generate_dataframe(username):
    np.random.seed(ord(username[0]))
    data = np.random.randint(low=0, high=1000, size=(10, 10))
    df = pd.DataFrame(data, columns=[f"col{i+1}" for i in range(10)])
    return df

# Define a function to set the color of a cell based on its value
def set_color(value):
    if value < 300:
        color = "green"
    elif value < 700:
        color = "yellow"
    else:
        color = "red"
    return f"background-color: {color}"

# Define the main function that displays the login page and the editable dataframe
def main():
    # Display the login page
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login successful!")
            # Generate the dataframe for the user
            df = generate_dataframe(username)
            # Create the Ag-Grid
            ag_grid = components.declare_component(
                "ag_grid",
                url="https://cdn.jsdelivr.net/npm/@ag-grid-community/all-modules@27.0.1/dist/ag-grid-community.min.js",
                js_module=True,
            )
            # Define the Ag-Grid options
            grid_options = {
                "columnDefs": [{"field": col} for col in df.columns],
                "rowData": df.to_dict("records"),
                "onCellValueChanged": "function(params) {set_edit_key(params.rowIndex, params.colDef.field, params.oldValue, params.newValue)}",
                "components": {
                    "numericCellEditor": {
                        "params": {
                            "valueParser": "Number(newValue)",
                            "onKeyDown": "function(event) {if (event.key === 'Enter' && event.target.value > 1000) {set_error_message('Value must be less than or equal to 1000.'); event.preventDefault();}}"
                        }
                    }
                }
            }
            # Define the Ag-Grid callback functions
            grid_callback = """
                function set_edit_key(row, col, old_value, new_value) {
                    streamlitSession.setSessionState({'edit_key': [row, col], 'old_value': old_value, 'new_value': new_value})
                }
                function set_error_message(message) {
                    streamlitSession.setSessionState({'error_message': message})
                }
            """
            # Display the Ag-Grid
            with st.spinner("Loading Ag-Grid..."):
                ag_grid(grid_options=grid_options, callback=grid_callback, key="ag-grid")
            # Display an error message if an inputted value is greater than 1000
               
