from preswald import text, plotly, connect, get_df, table, query, slider, separator, topbar, checkbox, alert, sidebar, selectbox
import pandas as pd
import plotly.express as px
import logging

topbar()
sidebar(defaultopen=True)

# Title and Description
text("# Welcome to Electric Vehicle Population Data!")
text("This interactive web application provides insights into electric vehicle adoption across the U.S. "
     "by analyzing a curated dataset of electric vehicles. Users can explore EV models, manufacturers, and their electric ranges using both tabular and graphical views. The dataset originates from [Data.gov](https://catalog.data.gov/) "
     "and includes key details such as vehicle make, model, year, and electric range.")

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
df = get_df('evpd_csv') # Getting dataframe
df.columns = [
    "VIN", "County", "City", "State", "Postal Code", "Model Year", "Make", "Model", 
    "Electric Vehicle Type", "Clean Alternative Fuel Vehicle (CAFV) Eligibility", 
    "Electric Range", "Base MSRP", "Legislative District", "DOL Vehicle ID", 
    "Vehicle Location", "Electric Utility", "2020 Census Tract"
] # Dataframe Columns

# Checkbox to show/hide preview (full dataset)
if checkbox("Show Full Vehicle Data"):
    text("## Full Dataset: Electric Range by Model/Make (Table)")
    table(df[["Model", "Make", "Model Year", "VIN", "Electric Range"]], title="Vehicle Data Preview", limit=100)

    text("## Full Dataset: Electric Range by Make (Graph)")
    full_fig = px.scatter(
        df,
        x='Make',
        y='Electric Range',
        labels={'Make': 'Make', 'Electric Range': 'Range (miles)'}
    )
    full_fig.update_traces(textposition='top center', marker=dict(size=7.5, color='purple'))
    full_fig.update_layout(template='plotly_white')
    plotly(full_fig, size=0.5)

separator()

# Sidebar UI: threshold and brand select
text("## Filter Data by Make and Range")
text("Use the interactive filters below to explore electric vehicles by their brand and minimum electric range. "
     "Filtered results will update both the data table and the accompanying scatter plot in real time.")
# Threshold slider
threshold = slider(
    label="Electric Range Threshold",
    min_val=0,
    max_val=100,
    step=5,
    default=50,
    size=0.5
)

make_options = sorted(df["Make"].dropna().unique())
selected_make = selectbox("Filter by car brand", options=["All"] + make_options, size=0.5)

# Adjust SQL query based on selected make
if selected_make != "All":
    sql = f"""
    SELECT "Model", "Make", "Electric Range"
    FROM evpd_csv
    WHERE "Electric Range" > {threshold} AND "Make" = '{selected_make}'
    """
    filtered_df = query(sql, "evpd_csv")
    alert(f"⚡ {len(filtered_df)} {selected_make} vehicles have an electric range over {threshold} miles.")
else:
    sql = f"""
    SELECT "Model", "Make", "Electric Range"
    FROM evpd_csv
    WHERE "Electric Range" > {threshold}
    """
    filtered_df = query(sql, "evpd_csv")
    alert(f"⚡ {len(filtered_df)} vehicles have an electric range over {threshold} miles.")

# Table: Model and Range by Threshold
text(f"## Model and Range of Electric Cars over {threshold} Mile Threshold")
table(filtered_df, title=f"Filtered Data")

# Filter Pandas DataFrame for visualization
dynamic_df = df[df["Electric Range"] > threshold]
if selected_make != "All":
    dynamic_df = dynamic_df[dynamic_df["Make"] == selected_make]


# Plot: Electric Range by Make
text(f"## Vehicle Scatter Plot by Make and Electric Range")
fig = px.scatter(
    filtered_df, x='Make', y='Electric Range',
    labels={'Model': 'Model', 'Electric Range': 'Range (miles)'}
)
fig.update_traces(textposition='top center', marker=dict(size=10, color='purple'))
fig.update_layout(template='plotly_white')
plotly(fig)
