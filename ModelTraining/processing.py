import pandas as pd

csv_file_path = '../WikiScraping/quests_data.csv'
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"Failed to load the file at: {csv_file_path}")


# Print the first few rows of the DataFrame
print(df.head())

# Get a summary of the DataFrame to check for missing values and data types
print(df.info())


# Drop rows with any missing values if necessary
df = df.dropna()

# Remove any duplicate entries
df = df.drop_duplicates()

