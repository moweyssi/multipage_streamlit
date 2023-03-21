import streamlit as st
import pandas as pd
import numpy as np

# Define a dictionary of usernames and corresponding data
user_data = {
    "john": pd.DataFrame(np.random.randint(1, 100, size=(5, 5)), columns=list("ABCDE")),
    "jane": pd.DataFrame(np.random.randint(1, 100, size=(5, 5)), columns=list("ABCDE")),
}

# Define a function to check if the username and password are valid
def authenticate(username, password):
    if username in user_data and password == "password":
        return True
    else:
        return False

# Define a function to color the cells based on their values
def color_cell(val):
    color = "black"
    if val > 80:
        color = "green"
    elif val > 50:
        color = "orange"
    elif val > 20:
        color = "red"
    return f"color: {color}"

# Define the main function that displays the login page and the editable dataframe
def main():
    # Display the login page
    st.title("Login")