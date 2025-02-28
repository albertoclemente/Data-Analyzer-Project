"""
This script imports a CSV file and provides basic analysis including dataset overview,
column names, data types, basic statistics, and a summary of missing values.
"""

import pandas as pd


def import_csv():
    try:
        user_input = input("Please enter the path to the CSV file you want to analyze: ")
        if not user_input:
            print("Error: No file path provided.")
            return None
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")
        return None
    try:
        df = pd.read_csv(user_input, encoding='utf-8')
    except FileNotFoundError:
        print("Error: The file was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        return None
    except pd.errors.DtypeWarning:
        print("Warning: Columns have mixed types.")
    except UnicodeDecodeError:
        print("Error: The file contains invalid characters.")
        return None
    return df

def calculate_missing_values(df):
    # Count of missing values in each column
    missing_values_count = df.isnull().sum()
    
    # Filter out columns with at least one missing value
    filtered_values = missing_values_count[missing_values_count >0]
    
    # Store the number of rows in a variable
    total_rows = df.shape[0]
    
    missing_df = filtered_values.to_frame(name="Missing Values")
    missing_df["Percentage Missing (%)"] = round ((filtered_values / total_rows) * 100,1)
    missing_df.sort_values(by="Percentage Missing (%)",
                           inplace=True,
                           ascending=False)
    return missing_df

def analyze_data(df):
    print("===Number of rows and columns===")
    print(f"Number of rows: {len(df)} - This represents the total number of data entries in the dataset.")
    print(f"Number of columns: {len(df.columns)} - This represents the total number of features or attributes in the dataset.")
    print("\n=== Column Names ===")
    df_list = df.columns.to_list()
    df_columns = pd.DataFrame(df_list)
    print(df_columns)
    print("\n\n=== Data Types ===")
    print(df.dtypes)
    print("\n\n===Basic Statistics===")
    select_categorical = df.select_dtypes(include = ['object','category'])
    describe_categorical = select_categorical.describe(include=['object','category'])
    print(df.describe())
    print("\n")
    print(describe_categorical)
    print("\n\n=== Missing Values Summary ===")
    missing_df = calculate_missing_values(df)
    if not missing_df.empty:
        print(missing_df)
    else:
        print("No missing values found in the dataset.")

if __name__ == "__main__":
    imported_data = import_csv()
    if imported_data is not None:
        analyze_data(imported_data)

