import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

#Defining root path
repo_root = os.path.dirname(os.path.abspath(__name__))

#Loading and reading the raw data
data_dir = os.path.join(repo_root, 'data')
file_name = os.path.join('03_Processed', '02_ProcessedData_Quantative.csv')
file_path = os.path.join(data_dir, file_name)
df = pd.read_csv(file_path)
df.info()

#Selecting all columns but ID and Organising community life 
columns = df.columns[1:-1]

#Creating a stacked bar chart for the distribution of ratings for each skill
ratings_distribution = df[columns].apply(pd.Series.value_counts).transpose()

#Sorting the DataFrame by the highest number of 4s, then 3s, then 2s, then 1s, then 0s
sort_order = [4, 3, 2, 1, 0]
ratings_distribution = ratings_distribution.sort_values(by=sort_order, ascending=False)
#Reversing the order of the rows for ease of reading the chart
ratings_distribution = ratings_distribution.iloc[::-1]


#Defining figures directory
figures_dir = os.path.join(repo_root, 'figures')

#Plotting the stacked bar chart
blue_palette = sns.color_palette("pastel", 5)
ax = ratings_distribution.plot(kind='barh', stacked=True, title='Distribution of Ratings for Each Skill', 
                               color=blue_palette, figsize=(12, 8))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.xlabel('Skills')
plt.ylabel('Count')
plt.legend(title='Rating', loc='upper left', bbox_to_anchor=(1, 1))

legend_labels = ['Mentor', 'Kompetenty', 'Zainteresowany', 'Niezainteresowany', 'Nieświadomy']
legend_patches = [plt.Rectangle((0,0),1,1,fc=color) for color in blue_palette[::-1]]
plt.legend(legend_patches, legend_labels, title='Rating', loc='upper left', bbox_to_anchor=(1, 1))

#Saving the chart
save_path = os.path.join(figures_dir, '03_survey_answer_distrtibution.png')
plt.savefig(save_path, bbox_inches='tight')
plt.show()

#Creating spearman rank correlation matrix
correlation_df = df[columns]
correlation = correlation_df.corr(method='spearman')
plt.figure(figsize = (16,12), dpi= 100)
plt.title('Spearman rank correlation matrix')
plt.rcParams.update({'font.size': 8})
mask = np.triu(np.ones_like(correlation, dtype=bool))
sns.heatmap(correlation, cmap= 'coolwarm', vmin=-1, vmax=1, center=0, annot=True, mask=mask, fmt='.2f')
plt.subplots_adjust(bottom=0.2)

#Saving the chart
save_path = os.path.join(figures_dir, '03_spearman_rank_correlation_matrix.png')
plt.savefig(save_path, bbox_inches='tight')
plt.show()