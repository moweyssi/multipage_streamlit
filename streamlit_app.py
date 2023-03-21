import streamlit as st
import pandas as pd
import numpy as np

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

# Define the main function that displays the login page and the editable dataframe
def main():
    # Display the login page
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login successful!")
            # Define a dataframe with random numbers unique to each user
            np.random.seed(ord(username[0]))
            data = np.random.randint(0, 100, size=(5, 5))
            df = pd.DataFrame(data, columns=["A", "B", "C", "D", "E"])
            # Define a function to set the cell color based on the value
            def color_negative_red(val):
                if val > 1000:
                    raise ValueError("Value cannot be greater than 1000")
                elif val < 30:
                    color = "red"
                elif val < 70:
                    color = "orange"
                else:
                    color = "green"
                return f"background-color: {color}"
            # Display the editable dataframe with cell color based on the value
            st.title("Editable DataFrame")
            st.write("Click on a cell to edit it.")
            st.experimental_data_editor(df.style.applymap(color_negative_red))
        else:
            st.error("Invalid username or password.")

if __name__ == "__main__":
    main()
