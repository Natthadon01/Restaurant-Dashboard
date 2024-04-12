import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("https://raw.githubusercontent.com/Natthadon01/test/main/test_data_clean.csv")

#Page Setup
st.set_page_config(
    page_title="Restaurant Dashboard",
    page_icon= ':hamburger:',
    layout="wide")

st.title("Restaurant Dashboard")
col1, col2 = st.columns(2)

# Clean Data
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Create Month Name
df["Month Name"] = df["Date"].dt.month_name()\
                             .map(lambda x: x[:3]\
                             .upper())

Month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

ftrend = df[df["Category"] == "food"]\
            .groupby(["Month Name","Menu"])["Price"]\
            .agg("count")\
            .reset_index()\
            .rename(columns={'Price':'Quantity'})

# Sort Values
ftrend["Month Name"] = pd.Categorical(ftrend["Month Name"], categories=Month, ordered=True)
ftrend.sort_values("Month Name", inplace=True)

#Create Chart 1
chart1 = go.Figure()

for menu, color in zip(ftrend['Menu'].unique(), px.colors.qualitative.Plotly):
        data = ftrend[ftrend['Menu'] == menu]
        
        # Add Line Chart
        chart1.add_trace(go.Scatter(x=data['Month Name'], 
                                 y=data['Quantity'], 
                                 mode='lines', 
                                 name=menu,
                                 line=dict(color=color)))
        # Update layout
        chart1.update_layout(title='Trend of Food Products Sales',
                     xaxis_title='',
                     yaxis_title='Quantity',
                     yaxis=dict(range=[0, max(ftrend['Quantity']) + (max(ftrend['Quantity'])*0.5) ]))

with col1: 
     st.plotly_chart(chart1, use_container_width= True)

## Chart 2
dtrend = df[df["Category"] == "drink"]\
        .groupby(["Month Name","Menu"])["Price"]\
        .agg("count").reset_index()\
        .rename(columns={'Price':'Quantity'})

# Sort data
dtrend["Month Name"] = pd.Categorical(dtrend["Month Name"], categories=Month, ordered=True)
dtrend.sort_values("Month Name", inplace=True)

#Create Chart 2
chart2 = go.Figure()

for menu, color in zip(dtrend['Menu'].unique(), px.colors.qualitative.Plotly):
    data = dtrend[dtrend['Menu'] == menu]
    # Add Line Chart
    chart2.add_trace(go.Scatter(x=data['Month Name'], 
                                 y=data['Quantity'], 
                                 mode='lines', 
                                 name=menu,
                                 line=dict(color=color)))

    # Update layout
    chart2.update_layout(title='Trend of Beverage Products Sales',
                        xaxis_title='',
                        yaxis_title='Quantity',
                        yaxis=dict(range=[0, max(dtrend['Quantity']) + (max(dtrend['Quantity'])*0.5)]))

with col2 :
    st.plotly_chart(chart2, use_container_width= True)

# Chart 3

fsales = df.query("Category == 'food'")\
        .groupby("Menu")["Price"]\
        .agg(["sum","count"])\
        .rename(columns= {'sum':'Sales','count':'Quantity'})\
        .sort_values(by='Sales', ascending= False)\
        .round().reset_index()

fsales["Data label"] = (fsales["Sales"]/1000).round(decimals = 1).astype(str) + "K"

# Create Chart 3
chart3 = go.Figure()

# Add bar chart
chart3.add_trace(go.Bar(x=fsales['Menu'],
                           y=fsales['Sales'],
                           name = 'Total Sales',
                           text=fsales["Data label"],
                           hoverinfo='text',
                           marker=dict(color=px.colors.qualitative.Plotly)))

# Add line chart
chart3.add_trace(go.Scatter( x=fsales['Menu'],
                                  y=fsales['Quantity'],
                                  mode = "lines",
                                  name = "Total Quantity",
                                  yaxis = 'y2',
                                  hoverinfo = 'y',
                                  line=dict(color='red')))

# Setting layout
chart3.update_layout(title='Food Products Sales',
                     yaxis_title='Sales',
                     xaxis_title='',
                     yaxis=dict(range=[0, max(fsales['Sales'])+(max(fsales['Sales'])*0.1)],
                                showgrid=False),  
                     yaxis2 = dict(title = "Quantity",
                                 showgrid=False,
                                 overlaying='y', 
                                 side='right', 
                                 position=1,
                                 range=[0, max(fsales['Quantity']) + (max(fsales['Quantity'])*0.5)]),
                     legend=dict(x=1.05, 
                                 y=1.0, 
                                 xanchor='left', 
                                 yanchor='top'))

with col1:
     st.plotly_chart(chart3, use_container_width= True)

# Chart 4

dsales = df.query("Category == 'drink'")\
           .groupby("Menu")["Price"]\
           .agg(["sum",'count'])\
           .rename(columns = {"sum":"Sales","count":"Quantity"})\
           .sort_values(by='Sales', ascending=False)\
           .round().reset_index()

dsales["Data label"] = (dsales["Sales"]/1000).round(decimals = 1).astype(str) + "K"

# Create Chart
chart4 = go.Figure()

# Add bar chart
chart4.add_trace(go.Bar(x=dsales['Menu'],
                            y=dsales['Sales'],
                            name = 'Total Sales',
                            text=dsales['Data label'],
                            hoverinfo='text',
                            marker=dict(color=px.colors.qualitative.Plotly)))
# Add line chart
chart4.add_trace(go.Scatter(x=dsales['Menu'],
                                  y=dsales['Quantity'],
                                  mode = "lines",
                                  name = "Total Quantity",
                                  yaxis = 'y2',
                                  line=dict(color='red')))

# Setting layout
chart4.update_layout(title = 'Beverage Products Sales',
                     yaxis_title = 'Sales',
                     xaxis_title ='',
                     yaxis = dict(range=[0, max(dsales['Sales']) + (max(dsales['Sales'])*0.1)],
                                showgrid=False),  
                     yaxis2 = dict(title = "Quantity",
                                    showgrid=False,
                                    overlaying='y', 
                                    side='right', 
                                    position=1,
                                    range=[0, max(dsales['Quantity']) + (max(dsales['Quantity'])*0.5)]),
                     legend = dict(x=1.05, 
                                 y=1.0, 
                                 xanchor='left', 
                                 yanchor='top'))

with col2 :
     st.plotly_chart(chart4, use_container_width= True)

# Chart 5
Opened_day = df.groupby("Day Of Week")["Date"].nunique().reset_index(name= 'Day')

sum_sales = df[["Category","Day Of Week","Price"]]\
            .groupby(["Day Of Week",'Category'])["Price"]\
            .agg(["sum",'count'])\
            .rename(columns={'sum':'Total Sales','count':'Total Quantity'})\
            .round().reset_index()

sales_data = pd.merge(sum_sales, Opened_day, on="Day Of Week")

# Create new column
sales_data["Avg Quantity"] = (sales_data["Total Quantity"] / sales_data["Day"]).round()
sales_data["Avg Sales"] = (sales_data["Total Sales"] / sales_data["Day"]).round()

# Sort the data
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

sales_data["Day Of Week"] = pd.Categorical(sales_data["Day Of Week"], 
                                            categories=day_order, 
                                            ordered=True)

sales_data.sort_values("Day Of Week", inplace=True)
sales_data = sales_data.reset_index().drop(columns= 'index')

# Create Chart 5
chart5 = go.Figure()

for category in sales_data['Category'].unique():
    subset = sales_data[sales_data['Category'] == category]
    
    # Add bar chart
    chart5.add_trace(go.Bar(x=subset['Day Of Week'],
                            y=subset['Avg Quantity'],
                            name=category,
                            text=subset['Avg Quantity'],
                            marker=dict(color=subset['Category'].map({'food': '#FDC060', 'drink': '#497AF6'}))))

    # Setting layout
    chart5.update_layout(title='Average Orders by Day',
                         xaxis_title='',
                         yaxis_title='Orders',
                         yaxis=dict(showgrid=False),
                         barmode = 'stack',
                         legend=dict(x=1.05,
                                     y=1.0,
                                     xanchor='left',
                                     yanchor='top'))

with col1 :
     st.plotly_chart(chart5, use_container_width= True)

# Chart 6
Opened_Day = df["Date"].nunique()

time_orders = df[["Category","Order Hour","Price"]]\
                .groupby(["Order Hour","Category"])['Price']\
                .agg(["sum",'count'])\
                .rename(columns= {'sum':'Total Sales','count':'Total Quantity'})\
                .sort_values(by = 'Order Hour')\
                .round()\
                .reset_index()

# Create new columns
time_orders["Avg Quantity"] = (time_orders["Total Quantity"]/Opened_Day).round()
time_orders["Avg Sales"] = (time_orders["Total Sales"]/Opened_Day).round(decimals= 2)

# Create Chart 6
chart6 = go.Figure()

for category in time_orders['Category'].unique():
     subset = time_orders[time_orders['Category'] == category]
     
     # Add bar chart
     chart6.add_trace(go.Bar(x=subset['Order Hour'], 
                             y=subset['Avg Quantity'], 
                             name=category,
                             yaxis='y',
                             text= subset['Avg Quantity'],
                             marker=dict(color=subset['Category'].map({'food': '#FDC060', 'drink': '#497AF6'}))))
     
     # Setting layout
     chart6.update_layout(title='Average Orders by Time',
                          xaxis_title='Time',
                          yaxis_title='Orders',
                          barmode = 'stack',
                          yaxis=dict(showgrid=False,
                                     range = [0,max(time_orders['Avg Quantity'])*2]),
                                     legend=dict(x=1.05,
                                                 y=1.0,
                                                 xanchor='left',
                                                 yanchor='top'))

with col2: 
     st.plotly_chart(chart6, use_container_width= True)

# Chart 7
fstandard = 10

df_kstaff = df[df["Category"] == "food"]\
                .groupby(["Day Of Week"])[["Waiting Time",'Kitchen Staff']]\
                .mean()\
                .reset_index()\
                .round()
# Sort data
df_kstaff["Day Of Week"] = pd.Categorical(df_kstaff["Day Of Week"],categories=day_order, ordered=True)
df_kstaff.sort_values("Day Of Week", inplace=True)
df_kstaff = df_kstaff.reset_index().drop(columns= 'index')

# Create Chart 7
chart7 = go.Figure()

# Add bar chart
chart7.add_trace(go.Bar(x=df_kstaff['Day Of Week'], 
                        y=df_kstaff['Kitchen Staff'], 
                        name='Avg Staff', 
                        yaxis='y', 
                        text= df_kstaff['Kitchen Staff']))

# Add line chart
chart7.add_trace(go.Scatter(x=df_kstaff['Day Of Week'], 
                            y=df_kstaff['Waiting Time'], 
                            mode='lines', 
                            name='Avg Waiting', 
                            yaxis='y2',
                            line=dict(color='red')))

# Add constant line
chart7.add_trace(go.Scatter(x=df_kstaff['Day Of Week'], 
                            y=[fstandard] * len(df_kstaff),  # Create a list of 10s with the same length as the data
                            mode='lines', 
                            name='Target Time', 
                            yaxis='y2',
                            line=dict(color='yellow', width=2, dash='dashdot')))

# Update layout
chart7.update_layout(title='Kitchen Staff Performance', 
                     xaxis_title='', 
                     yaxis_title='Number of Staff',
                     yaxis=dict(range=[0, max(df_kstaff['Kitchen Staff']) + 5],
                                showgrid=False),  
                     yaxis2=dict(title='Waiting Time (Minutes)',
                                 showgrid=False,
                                 overlaying='y', 
                                 side='right', 
                                 position=1,
                                 range=[0, max(df_kstaff['Waiting Time']) + 10]),
                     legend=dict(x=1.05, 
                                 y=1.0, 
                                 xanchor='left', 
                                 yanchor='top'))

with col1 : 
     st.plotly_chart(chart7, use_container_width= True)


##Chart 8 Drinks Manpower
dstandard = 5

df_dstaff = df[df["Category"] == "drink"]\
                .groupby(["Day Of Week"])[["Waiting Time",'Drinks Staff']]\
                .mean()\
                .reset_index()\
                .round()

# Sort data
df_dstaff["Day Of Week"] = pd.Categorical(df_dstaff["Day Of Week"], categories=day_order, ordered=True)
df_dstaff.sort_values("Day Of Week", inplace=True)
df_dstaff = df_dstaff.reset_index().drop(columns= 'index')

# Create Chart 8
chart8 = go.Figure()

# Add bar chart
chart8.add_trace(go.Bar(x=df_dstaff['Day Of Week'], 
                        y=df_dstaff['Drinks Staff'], 
                        name='Avg Staff', 
                        yaxis='y', 
                        text= df_dstaff['Drinks Staff']))

# Add line chart
chart8.add_trace(go.Scatter(x=df_dstaff['Day Of Week'], 
                            y=df_dstaff['Waiting Time'], 
                            mode='lines', 
                            name='Avg Waiting', 
                            yaxis='y2',
                            line=dict(color='red')))

# Add constant line
chart8.add_trace(go.Scatter(x=df_dstaff['Day Of Week'], 
                            y=[dstandard] * len(df_dstaff),  # Create a list of 10s with the same length as the data
                            mode='lines', 
                            name='Target Time', 
                            yaxis='y2',
                            line=dict(color='yellow', width=2, dash='dashdot')))

# Update layout
chart8.update_layout(title='Drink Staff Performance', 
                    xaxis_title='', 
                    yaxis_title='Number of Staff',
                    yaxis=dict(showgrid = False,
                                range=[0, max(df_dstaff['Drinks Staff'])+5]),
                    yaxis2=dict(title='Waiting Time (Minutes)',
                                showgrid = False, 
                                overlaying='y', 
                                side='right', 
                                position=1,
                                range=[0, max(df_dstaff['Waiting Time'])+10]),  # Set the range to start from 0
                    legend=dict(x=1.05, 
                                y=1.0, 
                                xanchor='left', 
                                yanchor='top'))

with col2: st.plotly_chart(chart8, use_container_width= True)