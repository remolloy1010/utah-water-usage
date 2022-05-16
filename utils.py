import pandas as pd
import numpy as np

# Constants:
color1 = '#9BC6AF' #pale green
color2 = '#B02D3A' #dark peach
color3 = '#CB7969' #peach

# Import Municipality and Industrial data for each year per county or state-wide
def import_data(region, year):
    df = pd.read_csv("./data/" + year + "_MI_" + region + ".csv")
    return df


def format_table(df, title):
    
    import plotly.graph_objects as go

    if 'NAME' in df.columns:
        name = 'NAME'
        new_name = 'COUNTY'
    elif 'STATE' in df.columns:
        name = 'STATE'
        new_name = 'STATE'
        
    df_table = df[['Year', 
                   name,
                   'TotalGPCD', 
                   'TotPotGPCD', 
                   'ResPotGPCD', 
                   'ComPotGPCD',
                   'InsPotGPCD',
                   'IndPotGPCD',
                   'TotSecGPCD',
                   'ResSecGPCD',
                   'ComSecGPCD',
                   'InsSecGPCD',
                   'IndSecGPCD'
                  ]].rename(columns={'TotalGPCD':'Total GPCD',
                                     name:new_name,
                                     'TotPotGPCD':'Total Potable GPCD',
                                     'ResPotGPCD':'Residential Potable GPCD',
                                     'ComPotGPCD':'Commercial Potable GPCD',
                                     'InsPotGPCD':'Institutional Potable GPCD',
                                     'IndPotGPCD':'Industrial Potable GPCD',
                                     'TotSecGPCD':'Total Secondary GPCD',
                                     'ResSecGPCD':'Residential Secondary GPCD',
                                     'ComSecGPCD':'Commercial Secondary GPCD',
                                     'InsSecGPCD':'Institutional Secondary GPCD',
                                     'IndSecGPCD':'Industrial Secondary GPCD',

        })

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df_table.columns),
                    align='center'),
        cells=dict(values=df_table.transpose(),
                   align='center'))
    ])

    fig.update_layout(
        title=title,
    )

    return fig.show()

def plot_state_totals(df, color1, color2, color3):
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name="Total GPCD",
        x=df['Year'], 
        y=df['TotalGPCD'], 
    #     fill='tozeroy',
        text='Total GPCD',
        marker=dict(color=color2)
    )) 

    fig.add_trace(go.Scatter(
        name="Potable GPCD",
        x=df['Year'], 
        y=df['TotPotGPCD'],
    #     fill='tozeroy',
        text='Potable GPCD',
        marker=dict(color=color1)
    )) 

    fig.add_trace(go.Scatter(
        name="Secondary GPCD",
        x=df['Year'], 
        y=df['TotSecGPCD'],
    #     fill='tozeroy',
        text='Secondary GPCD',
        marker=dict(color=color3)
    )) 

    # Add axis labels, title, etc.
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = df['Year'],
            ticktext = df['Year']
        ),
        title="Overall Utah State-wide Water Usage Between 2015-2019",
        xaxis_title="Year",
        yaxis_title="Gallons per capita per day (GPCD)",
    )

    fig.show()
    
# need to add new columns to original dataframe
# required additional data cleaning since 2018 and 2019 were missing secondary type columns (only provide total secondary GPCD)
def add_stat_columns(df_county, df_state, color_true=color3, color_false=color1):
    
    import numpy as np
    df_county = df_county.assign(Utah_TotalGPCD = df_state['TotalGPCD'][0])
    df_county = df_county.assign(Mean_TotalGPCD = df_county['TotalGPCD'].describe()['mean'])
    df_county = df_county.assign(Median_TotalGPCD = df_county['TotalGPCD'].describe()['50%'])
    
    df_county = df_county.assign(Utah_TotPotGPCD = df_state['TotPotGPCD'][0])
    df_county = df_county.assign(Mean_TotPotGPCD = df_county['TotPotGPCD'].describe()['mean'])
    df_county = df_county.assign(Median_TotPotGPCD = df_county['TotPotGPCD'].describe()['50%'])
    
    df_county = df_county.assign(Utah_TotSecGPCD = df_state['TotSecGPCD'][0])
    df_county = df_county.assign(Mean_TotSecGPCD = df_county['TotSecGPCD'].describe()['mean'])
    df_county = df_county.assign(Median_TotSecGPCD = df_county['TotSecGPCD'].describe()['50%'])
    
    df_county = df_county.assign(Mean_ResPotGPCD = df_county['ResPotGPCD'].describe()['mean'])
    df_county = df_county.assign(Mean_ComPotGPCD = df_county['ComPotGPCD'].describe()['mean'])
    df_county = df_county.assign(Mean_InsPotGPCD = df_county['InsPotGPCD'].describe()['mean'])
    df_county = df_county.assign(Mean_IndPotGPCD = df_county['IndPotGPCD'].describe()['mean'])

    if 'ResSecGPCD' in df_county.columns:
        df_county = df_county.assign(Mean_ResSecGPCD = df_county['ResSecGPCD'].describe()['mean'])
    if 'ComSecGPCD' in df_county.columns:
        df_county = df_county.assign(Mean_ComSecGPCD = df_county['ComSecGPCD'].describe()['mean'])
    if 'InsSecGPCD' in df_county.columns:
        df_county = df_county.assign(Mean_InsSecGPCD = df_county['InsSecGPCD'].describe()['mean'])
    if 'IndSecGPCD' in df_county.columns:
        df_county = df_county.assign(Mean_IndSecGPCD = df_county['IndSecGPCD'].describe()['mean'])
    
    df_county = df_county.assign(color = np.where(df_county['NAME'] == 'SALT LAKE', color_true, color_false))
    return df_county



def plot_avg_property_type(df_mean, title):
    
    import plotly.express as px

    df_means_t = df_mean.transpose().iloc[33:41]
    df_means_t = df_means_t.assign(pot_or_sec = ['Potable','Potable','Potable','Potable','Secondary','Secondary', 'Secondary', 'Secondary'])
    df_means_t = df_means_t.assign(property_type = ['Residential', 'Commercial', 'Institutional', 'Industrial', 'Residential', 'Commercial', 'Institutional', 'Industrial'])  

    fig = px.bar(df_means_t, 
                 x="mean", 
                 y="pot_or_sec", 
                 color="property_type", 
                 title="Wide-Form Input",
                 orientation='h')
    # Add axis labels, title, etc.
    fig.update_layout(
        title=title,
        xaxis_title="Average % of GPCD Water Usage",
        yaxis_title="Type of Water Usage",
        legend_title="Property Type"
    )
    
    return fig.show()

def plot_avg_water_type(df_mean, title):
    
    import plotly.express as px

    df_means_t = df_mean.transpose().iloc[41:]
    df_means_t = df_means_t.assign(pot_or_sec = ['Potable', 'Secondary', 'Potable', 'Secondary', 'Potable', 'Secondary', 'Potable', 'Secondary'])
    df_means_t = df_means_t.assign(property_type = ['Residential', 'Residential', 'Commercial', 'Commercial', 'Institutional', 'Institutional', 'Industrial', 'Industrial'])

    fig = px.bar(df_means_t, 
                 x="mean", 
                 y="property_type", 
                 color='pot_or_sec', 
                 title="Wide-Form Input",
                 orientation='h')
    # Add axis labels, title, etc.
    fig.update_layout(
        title=title,
        xaxis_title='Average % of GPCD Water Usage',
        yaxis_title="Property Type",
        legend_title="Property Type"
    )
    
    return fig.show()

# Plot bar chart of Total, Potable or Secondary Water Usage in GPCD per county (select year)
def GPCD_per_county_barchart(df_2015, df_2016, df_2017, df_2018, df_2019, title, bar_var, bar_var_txt, ref_var, ref_var_txt):
    
    import plotly.graph_objects as go

    fig = go.Figure(go.Bar(
        x=df_2015['NAME'], 
        y=df_2015[bar_var], 
        name=bar_var_txt,
        marker=dict(color = df_2015['color'])
    ))

    fig.add_trace(go.Scatter(
        x=df_2015['NAME'], 
        y=df_2015[ref_var], 
        name=ref_var_txt,
        marker=dict(color = df_2015['color'])

    ))

    # Add axis labels, title, etc.
    fig.update_layout(
        barmode='stack', 
        xaxis={'categoryorder':'total descending', 'tickangle':45},
        title=title,
        xaxis_title="County Name",
        yaxis_title="Gallons per capita per day (GPCD)",
    )

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{
                            'x':[df_2015['NAME'], df_2015['NAME']],
                            'y':[df_2015[bar_var], df_2015[ref_var]],
                            'marker':dict(color = df_2015['color'])
                        }],
                        label="2015",
                        method="restyle"
                    ),
                    dict(
                        args=[{
                            'x':[df_2016['NAME'], df_2016['NAME']],
                            'y':[df_2016[bar_var], df_2016[ref_var]],
                            'marker':dict(color = df_2016['color'])
                        }],
                        label="2016",
                        method="restyle"
                    ),
                    dict(
                        args=[{
                            'x':[df_2017['NAME'], df_2017['NAME']],
                            'y':[df_2017[bar_var], df_2017[ref_var]],
                            'marker':dict(color = df_2017['color'])
                        }],
                        label="2017",
                        method="restyle"
                    ),
                    dict(
                        args=[{
                            'x':[df_2018['NAME'], df_2018['NAME']],
                            'y':[df_2018[bar_var], df_2018[ref_var]],
                            'marker':dict(color = df_2018['color'])
                        }],
                        label="2018",
                        method="restyle"
                    ),
                    dict(
                        args=[{
                            'x':[df_2019['NAME'], df_2019['NAME']],
                            'y':[df_2019[bar_var], df_2019[ref_var]],
                            'marker':dict(color = df_2019['color'])
                        }],
                        label="2019",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.2,
                yanchor="top"
            ),
        ]
    )

    # Add annotation
    fig.update_layout(
        annotations=[
            dict(text="Select year:", showarrow=False,
            x=0, y=1.15, yref="paper", align="left")
        ]
    )

    return fig.show()

# Plot Potable and Secondary Water per Property Type per County
def plot_pot_sec_per_county_per_type(df_2015, df_2016, df_2017, property_type, pot_var, sec_var):
    
    if(property_type == "Residential"):
        pot_var = 'ResPotGPCD'
        sec_var = 'ResSecGPCD'
    elif(property_type == "Commercial"):
        pot_var = 'ComPotGPCD'
        sec_var = 'ComSecGPCD'
    elif(property_type == "Industrial"):
        pot_var = 'IndPotGPCD'
        sec_var = 'IndSecGPCD'
    elif(property_type == "Institutional"):
        pot_var = 'InsPotGPCD'
        sec_var = 'InsSecGPCD'
        

    import plotly.graph_objects as go

    fig = go.Figure(go.Bar(
        x=df_2015['NAME'], 
        y=df_2015[pot_var], 
        name=property_type + ' Potable GPCD'
    ))

    fig.add_trace(go.Bar(
        x=df_2015['NAME'], 
        y=df_2015[sec_var], 
        name=property_type + ' Secondary GPCD'
    ))


    # Add axis labels, title, etc.
    fig.update_layout(
        barmode='stack', 
        xaxis={'categoryorder':'total descending', 'tickangle':45},
        title=property_type + " Potable and Secondary Water Usage Per County",
        xaxis_title="County Name",
        yaxis_title="Gallons per capita per day (GPCD)",
    )

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{
                            'x':[df_2015['NAME'],df_2015['NAME']],
                            'y':[df_2015[pot_var],df_2015[sec_var]]}],
                        label="2015",
                        method="restyle"
                    ),
                    dict(
                        args=[{
                            'x':[df_2016['NAME'],df_2016['NAME']],
                            'y':[df_2016[pot_var],df_2016[sec_var]]}],
                        label="2016",
                        method="restyle"
                    ),
                    dict(
                        args=[{
                            'x':[df_2016['NAME'],df_2016['NAME']],
                            'y':[df_2016[pot_var],df_2016[sec_var]]}],
                        label="2017",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.2,
                yanchor="top"
            ),
        ]
    )

    # Add annotation
    fig.update_layout(
        annotations=[
            dict(text="Select year:", showarrow=False,
            x=0, y=1.15, yref="paper", align="left")
        ]
    )

    fig.show()