from preswald import text, plotly, connect, get_df, table, query, slider, separator, topbar, checkbox, alert, sidebar
import pandas as pd
import plotly.express as px
import logging

topbar()

text("# Welcome to Electric Vehicle Population Data!")
text("This is an application that filters Electric Vehicles based on their range per charge in miles.")

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Load the CSV
connect()
df = get_df('evpd_csv')
df.columns = [
    "VIN", "County", "City", "State", "Postal Code", "Model Year", "Make", "Model", 
    "Electric Vehicle Type", "Clean Alternative Fuel Vehicle (CAFV) Eligibility", 
    "Electric Range", "Base MSRP", "Legislative District", "DOL Vehicle ID", 
    "Vehicle Location", "Electric Utility", "2020 Census Tract"
]

# Optional: Checkbox to show/hide preview
if checkbox("Show full vehicle data preview table"):
    table(df[["Model", "Model Year", "VIN", "Electric Range"]], title="Vehicle Data Preview", limit=100)

separator()

# Sidebar slider for threshold
sidebar()
threshold = slider(
    label="Electric Range Threshold",
    min_val=0,
    max_val=100,
    step=5,
    default=50,
    size=1.0
)


separator()

# SQL query using threshold
sql = f"SELECT \"Model\", \"Electric Range\" FROM evpd_csv WHERE \"Electric Range\" > {threshold}"
filtered_df = query(sql, "evpd_csv")

# Highlight results
alert(f"⚡ {len(filtered_df)} vehicles have an electric range over {threshold} miles.")

text(f"## Model and Range of Electric Cars over {threshold} Mile Threshold")
table(filtered_df, title=f"Filtered Data")

# Additional pandas filter for visualization
dynamic_df = df[df["Electric Range"] > threshold]

separator()
text(f"## Vehicle Scatter Plot by Make and Electric Range")
fig = px.scatter(
    dynamic_df, x='Make', y='Electric Range', text='Model',
    labels={'Make': 'Make', 'Electric Range': 'Range (miles)'}
)
fig.update_traces(textposition='top center', marker=dict(size=10, color='lightblue'))
fig.update_layout(template='plotly_white')
plotly(fig)
