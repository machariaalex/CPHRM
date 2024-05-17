import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the page config
st.set_page_config(page_title='Data Visualizer', layout='wide', page_icon='📊')

# Title
st.title('📊 CPHRM')

# Sidebar radio button for selecting between About and Visualization
menu_selection = st.sidebar.radio("Menu", ["About", "Visualization"])

if menu_selection == "About":
    st.subheader("About")
    st.write("This app allows you to visualize data from Excel files. "
             "Select 'Visualization' from the sidebar to explore the data.")

elif menu_selection == "Visualization":
    # Specify the GitHub repository URL
    repo_url = "https://api.github.com/repos/machariaalex/CPHRM/contents"

    # Fetch the contents of the repository
    response = requests.get(repo_url)
    if response.status_code != 200:
        st.error("Error fetching data from GitHub.")
    else:
        contents = response.json()

        # Filter for Excel files
        files = [file['name'] for file in contents if file['name'].endswith('.xlsx')]

        # Dropdown to select a file
        selected_file = st.sidebar.selectbox('Select a file', files, index=None)

        if selected_file:
            # Fetch the raw content of the selected file
            file_url = f"https://raw.githubusercontent.com/machariaalex/CPHRM/main/{selected_file}"
            file_content = requests.get(file_url).content

            # Read the selected Excel file
            df = pd.read_excel(io.BytesIO(file_content))

            col1, col2 = st.columns(2)

            columns = df.columns.tolist()

            with col1:
                st.write("")
                st.write(df.head())

            with col2:
                # Plot type options
                plot_list = [
                    'Bar Chart',
                    'Stacked Bar Chart',
                    'Line Plot',
                    'Pie Chart',
                    'Horizontal Bar Chart'
                ]
                # Allow the user to select the type of plot
                plot_type = st.selectbox('Select the type of plot', options=plot_list)

            # Generate the plot based on user selection
            if plot_type:
                fig, ax = plt.subplots(figsize=(10, 6))
                if plot_type == 'Bar Chart':
                    # Plot bar chart
                    plot_bar_chart(df, ax)
                elif plot_type == 'Stacked Bar Chart':
                    # Plot stacked bar chart
                    plot_stacked_bar_chart(df, ax)
                elif plot_type == 'Line Plot':
                    # Plot line plot
                    plot_line_plot(df, ax)
                elif plot_type == 'Pie Chart':
                    # Plot pie chart
                    plot_pie_chart(df, ax)
                elif plot_type == 'Horizontal Bar Chart':
                    # Plot horizontal bar chart
                    plot_horizontal_bar_chart(df, ax)
                
                st.pyplot(fig)

def plot_bar_chart(df, ax):
    # Plot bar chart
    sns.barplot(x='District', y='Total Households', data=df, color='blue', label='Total Households', ax=ax)
    sns.barplot(x='District', y='Total Number Correct Match', data=df, color='green', label='Correct Match', ax=ax)
    sns.barplot(x='District', y='Total Number of Mismatch', data=df, color='red', label='Mismatch', ax=ax)
    plt.legend()
    plt.title('Total Households, Correct Matches, and Mismatches by District')
    plt.xticks(rotation=45)

def plot_stacked_bar_chart(df, ax):
    # Plot stacked bar chart
    sns.barplot(x='District', y='Total Number Correct Match', data=df, color='green', label='Correct Match', ax=ax)
    sns.barplot(x='District', y='Total Number of Mismatch', data=df, color='red', bottom=df['Total Number Correct Match'], label='Mismatch', ax=ax)
    plt.legend()
    plt.title('Total Households Breakdown by District')
    plt.xticks(rotation=45)

def plot_line_plot(df, ax):
    # Plot line plot
    sns.lineplot(x='District', y='% Change', data=df, marker='o', ax=ax)
    plt.title('Percentage Change of Water Source Mismatches by District')
    plt.xlabel('District')
    plt.ylabel('% Change')
    plt.xticks(rotation=45)

def plot_pie_chart(df, ax):
    # Plot pie chart
    totals = df[df['District'] == 'Totals']
    sizes = [totals['Total Number Correct Match'].values[0], totals['Total Number of Mismatch'].values[0]]
    labels = ['Correct Match', 'Mismatch']
    colors = ['green', 'red']

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Overall Correct Matches vs Mismatches')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

def plot_horizontal_bar_chart(df, ax):
    # Plot horizontal bar chart
    sns.barplot(y='District', x='% Change', data=df, palette='coolwarm', ax=ax)
    plt.title('Percentage Change of Water Source Mismatches by District')
    plt.xlabel('% Change')
    plt.ylabel('District')
