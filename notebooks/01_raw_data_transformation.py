import pandas as pd
import os
import missingno as msno
import matplotlib.pyplot as plt
import re

    
os.chdir(r'data')

file_name = r'01_Raw\01_DataCompetencySurvey.csv'

df = pd.read_csv(file_name)

df.info()

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
df.info()
#bars indicating amount of missing values in each column
os.chdir(r'..\figures')
msno.bar(df, figsize=(20, 12), fontsize=10)
plt.title('Missing Values Bar Chart', fontsize=14)  # Adjust the plot title font size

# Save the figure with the specified size and layout adjustments
plt.savefig('01_missing_val_bar_chart.png')
plt.show()

#matrix indicating missing values (white) in dataset
msno.matrix(df, figsize=(20, 12), fontsize=10)
plt.title('Missing Values Matrix Chart', fontsize=14)
plt.savefig('01_missing_val_matrix_chart.png')
plt.show()
#heatmap indicating correlation between missing values between columns
msno.heatmap(df, figsize=(20, 12), fontsize=10)
plt.title('Missing Values Heatmap Chart', fontsize=14)
plt.savefig('01_missing_val_heatmap_chart.png')
plt.show()



#filtering necessary rows
filtered_df = df[df.iloc[:, 7].str.contains("Chcę uczestniczyć", na=False)]


columns_to_drop = filtered_df.columns[1:6]
filtered_df = filtered_df.drop(columns_to_drop, axis=1)


os.chdir(r'..\data')
new_file_path = r'01_Raw\01_SelectedFeatures.csv'
filtered_df.to_csv(new_file_path, index=False)
print("File created succesfully")

