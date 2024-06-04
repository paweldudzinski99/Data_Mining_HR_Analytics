import pandas as pd
import os
import missingno as msno 
import matplotlib.pyplot as plt
import re

#Loading and reading the raw data
os.chdir(r'data')
file_name = r'01_Raw\01_DataCompetencySurvey.csv'
df = pd.read_csv(file_name)

#See column data types and non-null row count 
print(df.info())

#Cleaning up column names
def rename_columns(columns):
    renamed_columns = []
    for col in columns:
        if ':' in col:
            prefix, suffix = col.split(':', 1)
            if prefix.strip() in ['CLI', 'Front End'] or col.endswith(':'):
                renamed_columns.append(prefix.strip())
            else:
                renamed_columns.append(suffix.replace('(Clustering, Regression, Classification)','').strip())
        elif '(' in col:
            renamed_columns.append(re.sub(r'\([^)]*\)', '', col).strip())
        elif 'Nawiązywanie Relacji' in col or 'Promocja w' in col or 'Współpraca z' in col or 'Pozyskiwanie' in col:
            renamed_columns.append(col.replace('Nawiązywanie Relacji', 'Relacje').replace('Promocja w', '').replace('Współpraca z', '').replace('Pozyskiwanie', '').strip())
        else:
            renamed_columns.append(col.strip())
        
    return renamed_columns

df.columns = rename_columns(df.columns)

df.rename(columns={'Masz jakiś pomysł na projekt data? Napisz nam o tym. Jeżeli to nie ten moment, pozostaw puste pole.': 'Masz jakiś pomysł na projekt data? Napisz nam o tym.',
          'Jeżeli jest obszar, na którym się znasz i chcesz go wykorzystać, dopisz go': 'Dopisz inny obszar, który chcesz wykorzystać'},
          inplace=True)
#See updated columns info
print(df.info())

#Bar chart indicating amount of missing values in each column
os.chdir(r'..\figures')
msno.bar(df, figsize=(20, 12), fontsize=10)
plt.title('Missing Values Bar Chart', fontsize=14)
plt.subplots_adjust(bottom=0.3)
plt.savefig('01_missing_val_bar_chart.png')
plt.show()

#Matrix indicating missing values (white) in dataset
msno.matrix(df, figsize=(20, 12), color=(0.196, 0.537, 0.855), fontsize=10)
plt.text(-0.15, 1.1, 'Missing value = white', fontsize=12, transform=plt.gca().transAxes,
         verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5'), fontweight='bold')
plt.title('Missing Values Matrix Chart', fontsize=14)
plt.subplots_adjust(top=0.65)
plt.savefig('01_missing_val_matrix_chart.png')
plt.show()

#Heatmap indicating correlation between missing values between columns
msno.heatmap(df, figsize=(20, 12), fontsize=10)
plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate labels 45 degrees and align right
plt.yticks(rotation=0, fontsize=10)  # Keep y-axis labels horizontal
plt.title('Missing Values Heatmap Chart', fontsize=14)
plt.subplots_adjust(left=0.5, bottom=0.3)
plt.savefig('01_missing_val_heatmap_chart.png')
plt.show()

#Filtering necessary rows depending on respondent's desire to participate
filtered_df = df[df.iloc[:, 7].str.contains("Chcę uczestniczyć", na=False)]

#Filtering out unwanted columns with no value added (emails, time of survey, etc.)
columns_to_drop = filtered_df.columns[1:6]
filtered_df = filtered_df.drop(columns_to_drop, axis=1)

#Saving interim data
os.chdir(r'..\data')
new_file_path = r'02_Interim\01_SelectedFeatures.csv'
filtered_df.to_csv(new_file_path, index=False)
print("File created succesfully")