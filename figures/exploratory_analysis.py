import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.chdir(r'data')
file_name = r'03_Processed\02_ProcessedData_Quantative.csv'
df = pd.read_csv(file_name)

#Select all columns but ID
columns = df.columns[1:]

# Create a stacked bar chart for the distribution of ratings for each skill
ratings_distribution = df[columns].apply(pd.Series.value_counts).transpose()

# Sort the DataFrame by the highest number of 4s, then 3s, then 2s, then 1s, then 0s
sort_order = [4, 3, 2, 1, 0]
ratings_distribution = ratings_distribution.sort_values(by=sort_order, ascending=False)

# Plot the stacked bar chart
ax = ratings_distribution.plot(kind='bar', stacked=True, title='Distribution of Ratings for Each Skill', figsize=(12, 8))

# Rotate the x-axis labels for better visibility
plt.xticks(rotation=45, ha='right')

# Adjust the layout to ensure everything fits without overlapping
plt.tight_layout()

# Plot the stacked bar chart
ratings_distribution.plot(kind='bar', stacked=True, title='Distribution of Ratings for Each Skill', figsize=(12, 8))
plt.xlabel('Skills')
plt.ylabel('Count')
plt.legend(title='Rating')

os.chdir('..')
plt.savefig(r'figures\survey_answer_distrtibution.png', bbox_inches='tight')

plt.show()