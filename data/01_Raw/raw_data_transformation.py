import pandas as pd

file_name = '01_DataCompetencySurvey.csv'

df = pd.read_csv(file_name)

#filtering necessary rows
filtered_df = df[df.iloc[:, 7].str.contains("Chcę uczestniczyć", na=False)]

#renumbering of ID column
filtered_df.reset_index(drop=True, inplace=True)
filtered_df.index += 1 
filtered_df = filtered_df.drop(filtered_df.columns[0], axis=1)
filtered_df.insert(0, 'ID', filtered_df.index)

print(filtered_df)