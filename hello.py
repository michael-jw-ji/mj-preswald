from preswald import text, plotly, connect, get_df, table, query, slider
import pandas as pd
import plotly.express as px
import logging

text("# Welcome to Preswald!")
text("This is your first app. :tada:")



# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# logger.info("zsdfasdfasdon")


# Load the CSV
connect() # load in all sources, which by default is the sample_csv
df = get_df('evpd_csv')

# logger.info(df.columns)


table(df, title="Full Dataset Preview")
sql = "SELECT \"Electric Range\" FROM evpd_csv WHERE \"Electric Range\" > 50"
filtered_df = query(sql, "evpd_csv")
text("# My Data Analysis App")
table(filtered_df, title = "Filtered Data")

threshold = slider("Threshold", min_val=0, max_val=100, default=50)
dynamic_df = df[df["Electric Range"] > threshold]
text("## Dynamic Data View (Data with 'value' > Threshold)")
table(dynamic_df, title="Dynamic Data View")

# Create a scatter plot
fig = px.scatter(df, x='Make', y='Electric Range', text='Model',
                 title='Electric Range by Vehicle Make',
                 labels={'Make': 'Make', 'Electric Range': 'Range (miles)'})

# Style the plot
fig.update_traces(textposition='top center', marker=dict(size=10, color='lightblue'))
fig.update_layout(template='plotly_white')

# 5. Show the plot
plotly(fig)

# 6. Show the data table
table(df)