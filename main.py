import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the page config
st.set_page_config(page_title='Data Visualizer', layout='wide', page_icon='📊')

# Title
st.title('📊 CPHRM')

# Sidebar radio button for selecting between About and Visualization
menu_selection = st.sidebar.radio("Menu", ["About", "Visualization"])

selected_file = None  # Define selected_file outside conditional blocks

if menu_selection == "About":
    st.subheader("About")
    st.write("This app allows you to visualize data from Excel files. "
             "Select 'Visualization' from the sidebar to explore the data.")

elif menu_selection == "Visualization":
    # Upload your own dataset
    uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        selected_file = uploaded_file.name  # Set selected_file to the name of the uploaded file

    if selected_file and df is not None:
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
                'Horizontal Bar Chart',
                'Box Plot',
                'Violin Plot',
                'Scatter Plot',
                'Correlation Heatmap'
            ]
            # Allow the user to select the type of plot
            plot_type = st.selectbox('Select the type of plot', options=plot_list)

            # Additional plot customization options
            if plot_type in ['Bar Chart', 'Stacked Bar Chart', 'Horizontal Bar Chart']:
                color = st.color_picker("Select a color", "#00ff00")  # Default to green
            else:
                color = None

        # Generate the plot based on user selection
        if st.button('Generate Plot'):
            fig, ax = plt.subplots(figsize=(10, 6))

            if plot_type == 'Bar Chart':
                sns.barplot(x='District', y='Total Households', data=df, color=color, ax=ax)
                plt.title('Total Households by District')
                plt.xticks(rotation=45)

            elif plot_type == 'Stacked Bar Chart':
                districts = df['District']
                correct_match = df['Total Number Correct Match']
                mismatch = df['Total Number of Mismatch']
                bar_width = 0.6
                r = np.arange(len(districts))

                plt.bar(r, correct_match, color='green', edgecolor='grey', width=bar_width, label='Correct Match')
                plt.bar(r, mismatch, bottom=correct_match, color='red', edgecolor='grey', width=bar_width, label='Mismatch')

                plt.xlabel('District', fontweight='bold')
                plt.xticks(r, districts, rotation=45)
                plt.title('Total Households Breakdown by District')
                plt.legend()

            elif plot_type == 'Line Plot':
                sns.lineplot(x='District', y='% Change', data=df, marker='o', ax=ax)
                plt.title('Percentage Change by District')
                plt.xlabel('District')
                plt.ylabel('% Change')
                plt.xticks(rotation=45)

            elif plot_type == 'Pie Chart':
                totals = df[df['District'] == 'Totals']
                sizes = [totals['Total Number Correct Match'].values[0], totals['Total Number of Mismatch'].values[0]]
                labels = ['Correct Match', 'Mismatch']
                colors = ['green', 'red']

                plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
                plt.title('Overall Correct Matches vs Mismatches')
                plt.axis('equal')

            elif plot_type == 'Horizontal Bar Chart':
                sns.barplot(y='District', x='% Change', data=df, palette='coolwarm', ax=ax)
                plt.title('Percentage Change by District')
                plt.xlabel('% Change')
                plt.ylabel('District')

            elif plot_type == 'Box Plot':
                sns.boxplot(data=df.drop(columns=['District']), ax=ax)
                plt.title('Box Plot of Numerical Data')

            elif plot_type == 'Violin Plot':
                sns.violinplot(data=df.drop(columns=['District']), ax=ax)
                plt.title('Violin Plot of Numerical Data')

            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x='Total Number Correct Match', y='Total Number of Mismatch', data=df, hue='District', ax=ax)
                plt.title('Scatter Plot of Correct Matches vs Mismatches')
                plt.xlabel('Total Number Correct Match')
                plt.ylabel('Total Number of Mismatch')

            elif plot_type == 'Correlation Heatmap':
                corr = df.corr()
                sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
                plt.title('Correlation Heatmap')

            st.pyplot(fig)
