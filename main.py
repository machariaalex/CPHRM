import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='wide',
                   page_icon='📊')

# Title
st.title('📊 Data Visualizer')

# Sidebar radio button for selecting between About and Visualization
menu_selection = st.sidebar.radio("Menu", ["About", "Visualization"])

if menu_selection == "About":
    st.subheader("About")
    st.write("This app allows you to visualize data from Excel files. "
             "Select 'Visualization' from the sidebar to explore the data.")

elif menu_selection == "Visualization":
    # Specify the GitHub repository URL
    repo_url = "https://github.com/machariaalex/CPHRM/tree/main"

    # Fetch the contents of the repository page
    page_content = requests.get(repo_url).content

    # Parse the HTML content
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find all links in the page
    links = soup.find_all('a', href=True)

    # Filter for Excel files
    files = [link['href'].split('/')[-1] for link in links if link['href'].endswith('.xlsx')]

    # Dropdown to select a file
    selected_file = st.sidebar.selectbox('Select a file', files, index=None)

    if selected_file:
        # Construct the full URL to the selected file
        file_url = f"{repo_url}/{selected_file}"

        # Read the selected Excel file
        df = pd.read_excel(file_url)

        col1, col2 = st.columns(2)

        columns = df.columns.tolist()

        with col1:
            st.write("")
            st.write(df.head())

        with col2:
            # Allow the user to select columns for plotting
            x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
            y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

            plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot', 'Pie Chart']
            # Allow the user to select the type of plot
            plot_type = st.selectbox('Select the type of plot', options=plot_list)

        # Generate the plot based on user selection
        if st.button('Generate Plot'):
            fig, ax = plt.subplots(figsize=(6, 4))

            if plot_type == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                sns.histplot(df[x_axis], kde=True, ax=ax)
                y_axis = 'Density'
            elif plot_type == 'Count Plot':
                sns.countplot(x=df[x_axis], ax=ax)
                y_axis = 'Count'
            elif plot_type == 'Pie Chart':
                # Pie chart requires only one column for data and labels
                if x_axis != "None" and y_axis == "None":
                    data = df[x_axis].value_counts()
                    labels = data.index.tolist()
                    sizes = data.values.tolist()
                    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
                    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                    plt.title(f'Pie Chart of {x_axis}')
                    st.pyplot(fig)
                else:
                    st.write("For Pie Chart, please select only one column for data (X-axis) and 'None' for Y-axis.")
