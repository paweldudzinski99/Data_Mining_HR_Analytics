import pandas as pd
import os
import missingno as msno 
import matplotlib.pyplot as plt
import re

#Defining root path
repo_root = os.path.dirname(os.path.abspath(__name__))

#Loading and reading the raw data
data_dir = os.path.join(repo_root, 'data')
file_name = os.path.join('01_Raw', 'DataCompetencySurvey.csv')
file_path = os.path.join(data_dir, file_name)
df = pd.read_csv(file_path)

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
        elif 'Nawiązywanie Relacji' in col or 'Promocja w' in col :
            renamed_columns.append(col.replace('Nawiązywanie Relacji', 'Relacje').replace('Promocja w', '').replace('Współpraca z', '').strip())
        else:
            renamed_columns.append(col.strip())
        
    return renamed_columns

df.columns = rename_columns(df.columns)

df.rename(columns={'Masz jakiś pomysł na projekt data? Napisz nam o tym. Jeżeli to nie ten moment, pozostaw puste pole.': 'Masz jakiś pomysł na projekt data?',
        'Jeżeli jest obszar, na którym się znasz i chcesz go wykorzystać, dopisz go': 'Dopisz inny obszar',
        'W jaki sposób chcesz uczestniczyć w Community?': 'Sposób uczestnictwa',
        'Jeżeli pominięto branżę, na której się znasz dopisz ją':'Dopisz pominiętą branżę'},
        inplace=True)


#See updated columns info
print(df.info())

#Bar chart indicating amount of missing values in each column
figures_dir = os.path.join(repo_root, 'figures')
msno.bar(df, figsize=(20, 12), fontsize=10)
plt.title('Missing Values Bar Chart / Wykres brakujących wartości', fontsize=14)
plt.subplots_adjust(bottom=0.3)
save_path = os.path.join(figures_dir, '01_missing_val_bar_chart.png')
plt.savefig(save_path)
plt.show()

#Matrix indicating missing values (white) in dataset
msno.matrix(df, figsize=(20, 12), color=(0.196, 0.537, 0.855), fontsize=10)
plt.text(-0.15, 1.1, 'Missing value = white', fontsize=12, transform=plt.gca().transAxes,
        verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5'), fontweight='bold')
plt.title('Missing Values Heatmap / Heatmapa brakujących wartości', fontsize=14)
plt.subplots_adjust(top=0.65)
save_path = os.path.join(figures_dir, '01_missing_val_heatmap.png')
plt.savefig(save_path)
plt.show()

#Filtering out necessary rows depending on respondent's desire to participate
filtered_df = df[df.iloc[:, 7].str.contains("Chcę uczestniczyć", na=False)]

#Filtering out unwanted columns with no value added (emails, time of survey, etc.)
columns_to_drop = filtered_df.columns[1:6]
filtered_df = filtered_df.drop(columns_to_drop, axis=1)

#Saving interim data
interim_dir = os.path.join(repo_root, 'data', '02_Interim')
new_file_path = os.path.join(interim_dir, '01_SelectedFeatures.csv')
filtered_df.to_csv(new_file_path, index=False)
print("File created succesfully")