import pandas as pd
import os

os.chdir(r'data')

file_name = r'01_Raw\01_DataCompetencySurvey.csv'

df = pd.read_csv(file_name)

#filtering necessary rows
filtered_df = df[df.iloc[:, 7].str.contains("Chcę uczestniczyć", na=False)]

#renumbering of ID column
filtered_df.reset_index(drop=True, inplace=True)
filtered_df.index += 1 
filtered_df = filtered_df.drop(filtered_df.columns[0], axis=1)
filtered_df.insert(0, 'ID', filtered_df.index)

columns_to_drop = filtered_df.columns[1:6]
filtered_df = filtered_df.drop(columns_to_drop, axis=1)

print(filtered_df)

new_file_path = r'02_Interim\01_SelectedFeatures.csv'
filtered_df.to_csv(new_file_path, index=False)
print("File created succesfully")