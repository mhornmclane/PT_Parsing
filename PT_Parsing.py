#PT_Parsing

import pandas as pd
from os import listdir
from os.path import isfile, join, basename
import math

#setup params
flowrate_bounds = (28,32)
mA_bounds = (1000, 3000)
PSI_targets = (14, 1000, 3000, 5000, 7000, 9000)
PSI_range = (-250, 250)
results = {}


folder = r'C:\Workspace\DataWork\Pressure_Test_Parsing\Good'

file_list = [f for f in listdir(folder) if isfile(join(folder, f))]

#one off
# filename = r'C:\Workspace\DataWork\Pressure_Test_Parsing\Good\14599-01.csv'

with open('results.csv', 'w') as results_out:
    # print("Pump,Flow,mA,PSI")
    results_out.write("Pump,Avg_Flow,Avg_mA,Avg_PSI,Nominal_PSI\n")
    for file in file_list:
        filename = join(folder,file)
        df = pd.read_csv(filename, header=None, usecols=[5,9,10],names=["Flowrate","mA","PSI"])

        pump_id = basename(filename).split('.')[0]

        results[pump_id] = {}
        # for PSI in PSI_targets:
        #     results[pump_id][PSI] = ''
            
        # print(results)

        cleaned_df = df.loc[(df['mA'] < mA_bounds[1]) & (df['mA'] > mA_bounds[0]) & (df['Flowrate'] < flowrate_bounds[1]) & (df['Flowrate'] > flowrate_bounds[0])]
        for PSI in PSI_targets:
            min_pressure = PSI + PSI_range[0]
            max_pressure = PSI + PSI_range[1]
            this_df = cleaned_df.loc[(df['PSI'] < max_pressure) & (df['PSI'] > min_pressure)]
            avg_flowrate = this_df['Flowrate'].mean()
            avg_mA = this_df['mA'].mean()
            avg_PSI = this_df['PSI'].mean()
            # print(f"{pump_id},{avg_flowrate:.1f},{avg_mA:.0f},{avg_PSI:.0f},{PSI}")
            results_out.write(f"{pump_id},{avg_flowrate:.1f},{avg_mA:.0f},{avg_PSI:.0f},{PSI}\n")
            results[pump_id][PSI] = {"avg" : avg_mA}
            results[pump_id][PSI]["delta"] = avg_mA - results[pump_id][PSI_targets[0]]['avg']


with open("summary.csv", 'w') as summary_out:
    summary_out.write("PSI, Avg_Delta, Min_Delta, Max_Delta\n")
    for PSI in PSI_targets:
        average_sum = 0
        count = 0
        max = 0
        min = 9999
        for ID in results:
            this_delta = results[ID][PSI]['delta']
            if(not math.isnan(this_delta)):
                average_sum += this_delta
                count += 1
                if this_delta < min: min = this_delta
                if this_delta > max: max = this_delta
        average = average_sum/count
        summary_out.write(f"{PSI},{average},{min},{max}\n")
