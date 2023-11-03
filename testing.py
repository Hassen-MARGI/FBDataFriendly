import pandas as pd
df=pd.read_csv("data.csv")
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.expand_frame_repr', False)  # Prevent line-wrapping

print(df.to_string(index=False))
