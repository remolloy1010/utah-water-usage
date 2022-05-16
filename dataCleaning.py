import pandas as pd
import numpy as np

exec(open('utils.py').read())

# Import state-wide data
state_MI_2015 = import_data("state", "2015")
state_MI_2016 = import_data("state", "2016")
state_MI_2017 = import_data("state", "2017")
state_MI_2018 = import_data("state", "2018")
state_MI_2019 = import_data("state", "2019")

# Import county-wide data
county_MI_2015 = import_data("county", "2015")
county_MI_2016 = import_data("county", "2016")
county_MI_2017 = import_data("county", "2017")
county_MI_2018 = import_data("county", "2018")
county_MI_2019 = import_data("county", "2019")

# Merge all state data to one dataframe
df_state = pd.concat([state_MI_2015, state_MI_2016, state_MI_2017, state_MI_2018, state_MI_2019])

# Get means
df_state_means = pd.DataFrame(df_state.describe().loc['mean']).transpose()

sum_pot = float(df_state_means['ResPotGPCD'] + df_state_means['ComPotGPCD'] + df_state_means['InsPotGPCD'] + df_state_means['IndPotGPCD'])
sum_sec = float(df_state_means['ResSecGPCD'] + df_state_means['ComSecGPCD'] + df_state_means['InsSecGPCD'] + df_state_means['IndSecGPCD'])

sum_res = float(df_state_means['ResPotGPCD'] + df_state_means['ResSecGPCD'])
sum_com = float(df_state_means['ComPotGPCD'] + df_state_means['ComSecGPCD'])
sum_ins = float(df_state_means['InsPotGPCD'] + df_state_means['InsSecGPCD'])
sum_ind = float(df_state_means['IndPotGPCD'] + df_state_means['IndSecGPCD'])

df_state_means = df_state_means.assign(Perc_ResPotGPCD = float(df_state_means['ResPotGPCD'] / sum_pot) * 100)
df_state_means = df_state_means.assign(Perc_ComPotGPCD = float(df_state_means['ComPotGPCD'] / sum_pot) * 100)
df_state_means = df_state_means.assign(Perc_InsPotGPCD = float(df_state_means['InsPotGPCD'] / sum_pot) * 100)
df_state_means = df_state_means.assign(Perc_IndPotGPCD = float(df_state_means['IndPotGPCD'] / sum_pot) * 100)
df_state_means = df_state_means.assign(Perc_ResSecGPCD = float(df_state_means['ResSecGPCD'] / sum_sec) * 100)
df_state_means = df_state_means.assign(Perc_ComSecGPCD = float(df_state_means['ComSecGPCD'] / sum_sec) * 100)
df_state_means = df_state_means.assign(Perc_InsSecGPCD = float(df_state_means['InsSecGPCD'] / sum_sec) * 100)
df_state_means = df_state_means.assign(Perc_IndSecGPCD = float(df_state_means['IndSecGPCD'] / sum_sec) * 100)

df_state_means = df_state_means.assign(Perc_PotResGPCD = float(df_state_means['ResPotGPCD'] / sum_res) * 100)
df_state_means = df_state_means.assign(Perc_SecResGPCD = float(df_state_means['ResSecGPCD'] / sum_res) * 100)

df_state_means = df_state_means.assign(Perc_PotComGPCD = float(df_state_means['ComPotGPCD'] / sum_com) * 100)
df_state_means = df_state_means.assign(Perc_SecComGPCD = float(df_state_means['ComSecGPCD'] / sum_com) * 100)

df_state_means = df_state_means.assign(Perc_PotInsGPCD = float(df_state_means['InsPotGPCD'] / sum_ins) * 100)
df_state_means = df_state_means.assign(Perc_SecInsGPCD = float(df_state_means['InsSecGPCD'] / sum_ins) * 100)

df_state_means = df_state_means.assign(Perc_PotIndGPCD = float(df_state_means['IndPotGPCD'] / sum_ind) * 100)
df_state_means = df_state_means.assign(Perc_SecIndGPCD = float(df_state_means['IndSecGPCD'] / sum_ind) * 100)

county_MI_2015 = add_stat_columns(county_MI_2015, state_MI_2015)
county_MI_2016 = add_stat_columns(county_MI_2016, state_MI_2016)
county_MI_2017 = add_stat_columns(county_MI_2017, state_MI_2017)
county_MI_2018 = add_stat_columns(county_MI_2018, state_MI_2018)
county_MI_2019 = add_stat_columns(county_MI_2019, state_MI_2019)