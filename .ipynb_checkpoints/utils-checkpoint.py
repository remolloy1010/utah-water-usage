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
    
def plot_avg_by_type(df_mean, title):
    
    import plotly.express as px

    df_means_t = df_mean.transpose().iloc[33:]
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