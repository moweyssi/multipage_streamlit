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
            # Display the editable dataframe with colored cells
            st.title("Editable DataFrame")
            grid_response = components.declare_component(
            "agGrid", url="https://unpkg.com/ag-grid-community@27.0.0/dist/ag-grid-community.min.js"
            )
            data = df.to_dict('records')
            columns = [{'field': col, 'editable': True} for col in df.columns]
            params = {
                'rowData': data,
                'columnDefs': columns,
                'enableCellChangeFlash': True,
                'enableRangeSelection': True,
                'rowSelection': 'multiple',
                'getRowNodeId': 'function(data) { return data.id; }'
            }
            grid_result = grid_response(**params)
            st.components.v1.html(grid_result, height=500)
        else:
            st.error("Invalid username or password.")
    # Display an error message if an inputted value is greater than 1000
    if "dataframe" in st.session_state:
        df = st.session_state.dataframe
        if st.session_state.edit_key and st.session_state.new_value > 1000:
            row, col = st.session_state.edit_key
            df.iloc[row, col] = st.session_state.old_value
            st.error("Value must be less than or equal to 1000.")

if __name__ == "__main__":
    main()
