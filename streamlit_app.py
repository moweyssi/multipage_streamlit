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

# Define the main function that displays the login page and the editable dataframe using ag-grid
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
            # Display the editable dataframe with colored cells using ag-grid
            st.title("Editable DataFrame")
            grid_options = {
                'editable': True,
                'enableRangeSelection': True,
                'enableCellChangeFlash': True,
            }
            components.iframe(
                f"https://cdn.jsdelivr.net/npm/ag-grid-community@25.2.0/dist/ag-grid-community.min.noStyle.js",
                height=0,
                width=0,
            )
            js = f"""
            const gridOptions = {grid_options};
            const data = {df.to_json(orient='records')};
            new agGrid.Grid(document.querySelector('#myGrid'), gridOptions);
            const updateData = (data) => {{
                gridOptions.api.setRowData(data);
            }};
            updateData(data);
            """
            components.html(f"""<div id="myGrid" style="height: 400px;width:100%;" class="ag-theme-balham"></div>""", 
                            height=500, 
                            scrolling=False)
            components.html(f"""<script>{js}</script>""")
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
