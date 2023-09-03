import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import random

_csv_dir = '.../mosquitos_data.csv' 
df = pd.read_csv(_csv_dir)
df.head()


boxprops = dict(linestyle='--', linewidth=0)
medianprops = dict(linestyle='-', linewidth=2.5, color='black')
fig, ax = plt.subplots()
sns.boxplot(x=df['Treatment'], y="Response", data=df, showfliers=True, boxprops=boxprops, 
            medianprops=medianprops, palette=['lightcoral','lightsteelblue'])
plt.xlabel('Treatment')
plt.ylabel('Number of Mosquitos')
plt.title('Mosquito Attractiveness for Beer and Water')


def calculate_infer_stats(df):
    '''

    '''
    #Identify treatment type
    treat_types = list(dict.fromkeys(list(df['Treatment'])))
    #Create an empty dictionary
    infer_stats_dct = {}
    for treat_type in treat_types:
        #Filter the dataframe by treatment type
        filtered_df = df.loc[df['Treatment'] == treat_type]
        #Use pandas to calculate all the statistics at once instead of breaking it up into multiple different lines
        infer_stats = filtered_df['Response'].describe()
        #Update the dictionary with the findings
        infer_stats_dct.update({
                                treat_type : infer_stats
                                })
    return infer_stats_dct

infer_stats_dct = calculate_infer_stats(df)
inf_stats = pd.DataFrame.from_dict(infer_stats_dct)
_ = [print(f'The mean, median, and standard deviation for {name} are\
           {inf_stats.loc["mean"][name]:.1f}, {inf_stats.loc["50%"][name]:.1f}, and\
           {inf_stats.loc["std"][name]:.1f}') for name in inf_stats.columns]

org_mean_dif = inf_stats.loc["mean"]['Beer'] - inf_stats.loc["mean"]['Water']

def permutation_test(stats,
                     data,
                     i = 50000,):
    '''

    '''
    #Pool all the data together
    p_data = np.array(data['Response'])
    #Identify the number of samples in each treatment group
    s_beer = int(stats.loc["count"]['Beer'])
    #Initialize samples
    p_group = []
    #Iterate
    for _ in range(i):
        random.shuffle(p_data)
        p_group.append(np.mean(p_data[0:s_beer]) - np.mean(p_data[s_beer:]))
    
    return p_group

i = 50000
p_group = permutation_test(inf_stats,df,i)

fig, ax = plt.subplots()    
sns.distplot(p_group, kde=True)
plt.axvline(org_mean_dif, color='r')
plt.ylabel('Probability Density')
plt.xlabel('Differences in Mean')
plt.title(f'Random Permutation Test ({i} iterations)')

prob = (len(np.where(list(map(abs, p_group)) >= org_mean_dif)[0])/len(p_group))*100
print(f'The probability of achieving the experimental outcome or greater is {prob}% with\
      {len(p_group)} iterations')













































