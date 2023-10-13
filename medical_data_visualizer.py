import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['bmi'] = df['weight'] / ((df['height']/100)**2)
df.loc[df['bmi'] <= 25, 'overweight'] = 0
df.loc[df['bmi'] > 25, 'overweight'] = 1
df['overweight'] = df['overweight'].astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1




# Draw Categorical Plot
def draw_cat_plot():
  # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


  # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
  df_cat = df_cat.value_counts().sort_index().reset_index()
  df_cat.columns = ['cardio', 'variable', 'value', 'total']
    

  # Draw the catplot with 'sns.catplot()'
  # Get the figure for the output
  fig = sns.catplot(data=df_cat, x="variable", y="total", col="cardio", kind="bar", height=6, aspect=1, hue="value")

  fig=fig.figure
  # Do not modify the next two lines
  fig.savefig('catplot.png')
  return fig


# Draw Heat Map
def draw_heat_map():
  # Clean the data
  df_heat = df[df['ap_lo'] <= df['ap_hi']]
  df_heat = df_heat.drop(columns=['bmi'])

  df_heat = df_heat[df['height'] >= df['height'].quantile(0.025)]
  df_heat = df_heat[df['height'] <= df['height'].quantile(0.975)]
  df_heat = df_heat[df['weight'] >= df['weight'].quantile(0.025)]
  df_heat = df_heat[df['weight'] <= df['weight'].quantile(0.975)]

  print(df_heat.info())
    
  # Calculate the correlation matrix
  corr = df_heat.corr()

  # Generate a mask for the upper triangle
  mask = np.triu(np.ones_like(corr))
  #print(mask)
  #print(corr)


  # Set up the matplotlib figure
  fig, ax = plt.subplots(figsize=(9, 9))
  
  # Draw the heatmap with 'sns.heatmap()'
  sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values,
            mask=mask,
            annot=True,
            fmt='.1f',
            center=0
            )
  

  # Do not modify the next two lines
  fig.savefig('heatmap.png')
  return fig
