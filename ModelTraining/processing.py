import pandas as pd

csv_file_path = '../quests_data.csv'
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"Failed to load the file at: {csv_file_path}")

print(df.head())
print(df.info())
df.fillna('None', inplace=True)

df = df.applymap(lambda s: s.lower() if type(s) == str else s)

print(df.head())

df.to_csv('cleaned_quests_data.csv', index=False)

