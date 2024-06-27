def run():
        
    import pandas as pd
    import os
    import numpy as np

    #Defining root path
    repo_root = os.path.dirname(os.path.abspath(__name__))

    #Loading and reading the raw data
    data_dir = os.path.join(repo_root, 'data')
    file_name = os.path.join('02_Interim', '01_SelectedFeatures.csv')
    file_path = os.path.join(data_dir, file_name)
    df = pd.read_csv(file_path)

    df.info()

    #Choosing columns to drop and keep for easier splitting into two dataframes
    columns_to_drop = ['Masz jakiś pomysł na projekt data?', 'Sposób uczestnictwa',
                    'Dopisz inny obszar', 'Dopisz pominiętą branżę']
    columns_to_keep = ['ID', 'Masz jakiś pomysł na projekt data?', 'Sposób uczestnictwa',
                    'Dopisz inny obszar', 'Dopisz pominiętą branżę']

    #Creating two seperate df depending on data type
    quantative_df = df.drop(columns_to_drop, axis=1)
    qualitative_df = df[columns_to_keep]

    #Replacing entries with binary classification depending on respondent answer
    condition = (df['Sposób uczestnictwa'] == 'Chcę uczestniczyć w projekcie data i organizować "życie" Community')
    value_if_true = 1
    value_if_false = 0
    quantative_df['Organizowanie życia community'] = np.where(condition, value_if_true, value_if_false)

    #Switching 0 <-> 1 for logic reasons
    quantative_df.iloc[:, 1:-1] = quantative_df.iloc[:, 1:-1].replace({0: 1, 1: 0})

    #Replacing missing data
    qualitative_df = qualitative_df.replace('', 'Brak odpowiedzi')
    qualitative_df = qualitative_df.fillna('Brak odpowiedzi')

    #Creating files
    processed_dir = os.path.join(repo_root, 'data', '03_Processed')

    new_file_path = os.path.join(processed_dir, '02_ProcessedData_Quantative.csv')
    quantative_df.to_csv(new_file_path, index=False)

    new_file_path2 = os.path.join(processed_dir, '02_ProcessedData_Qualitative.csv')
    qualitative_df.to_csv(new_file_path2, index=False)