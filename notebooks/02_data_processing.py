import pandas as pd
import os
import numpy as np

#Finding file
os.chdir(r'data')
file_name = r'02_Interim\01_SelectedFeatures.csv'
df = pd.read_csv(file_name)
df.info()

#Choosing columns to drop and keep for easier splitting into two dataframes
columns_to_drop = ['Masz jakiś pomysł na projekt data? Napisz nam o tym.', 'W jaki sposób chcesz uczestniczyć w Community?',
                   'Dopisz inny obszar, który chcesz wykorzystać', 'Jeżeli pominięto branżę, na której się znasz dopisz ją']
columns_to_keep = ['ID', 'Masz jakiś pomysł na projekt data? Napisz nam o tym.', 'W jaki sposób chcesz uczestniczyć w Community?',
                   'Dopisz inny obszar, który chcesz wykorzystać', 'Jeżeli pominięto branżę, na której się znasz dopisz ją']

#Creating two seperate df depending on data type
quantative_df = df.drop(columns_to_drop, axis=1)
qualitative_df = df[columns_to_keep]

#Replacing entries with binary classification depending on respondent answer
condition = (df['W jaki sposób chcesz uczestniczyć w Community?'] == 'Chcę uczestniczyć w projekcie data i organizować "życie" Community')
value_if_true = 1
value_if_false = 0
quantative_df['Organizowanie życia community'] = np.where(condition, value_if_true, value_if_false)

#Replacing missing data
qualitative_df = qualitative_df.replace('', 'Brak odpowiedzi')
qualitative_df = qualitative_df.fillna('Brak odpowiedzi')

#Creating files
new_file_path1 = r'03_Processed\02_ProcessedData_Quantative.csv'
quantative_df.to_csv(new_file_path1, index=False)
print("File created succesfully")

new_file_path2 = r'03_Processed\02_ProcessedData_Qualitative.csv'
qualitative_df.to_csv(new_file_path2, index=False)
print("File created succesfully")