import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

#Reading file
os.chdir(r'data')
file_name = r'03_Processed\02_ProcessedData_Quantative.csv'
df = pd.read_csv(file_name)
df.info()

#Selecting all columns but ID and Organising community life 
columns = df.columns[1:-1]

#Creating a stacked bar chart for the distribution of ratings for each skill
ratings_distribution = df[columns].apply(pd.Series.value_counts).transpose()

#Sorting the DataFrame by the highest number of 4s, then 3s, then 2s, then 1s, then 0s
sort_order = [4, 3, 2, 1, 0]
ratings_distribution = ratings_distribution.sort_values(by=sort_order, ascending=False)

#Plotting the stacked bar chart
ax = ratings_distribution.plot(kind='bar', stacked=True, title='Distribution of Ratings for Each Skill', figsize=(12, 8))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
ratings_distribution.plot(kind='bar', stacked=True, title='Distribution of Ratings for Each Skill', figsize=(12, 8))
plt.xlabel('Skills')
plt.ylabel('Count')
plt.legend(title='Rating')

#Saving the chart
os.chdir('..')
plt.savefig(r'figures\03_survey_answer_distrtibution.png', bbox_inches='tight')
plt.show()


#Creating a correlation matrix heatmap
correlation = df.corr()
plt.figure(figsize = (12,8))
plt.rcParams.update({'font.size': 8})
mask = np.triu(np.ones_like(correlation, dtype=bool))
sns.heatmap(correlation, cmap= 'coolwarm', vmin=-1, vmax=1, center=0, annot= True, mask=mask, fmt='.2f')
plt.subplots_adjust(bottom=0.2)
plt.show()