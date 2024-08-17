import pandas as pd

# Load the original CSV file
df = pd.read_csv("verizon_subscribers.csv")

# Filter for Verizon Plus Play subscribers
plusplay_df = df[df['Verizon_Service'] == 'Verizon Plus Play']

# Filter for Verizon MyPlan subscribers
myplan_df = df[df['Verizon_Service'] == 'Verizon MyPlan']

# Save the filtered dataframes to separate CSV files
plusplay_df.to_csv("verizon_plusplay_subscribers.csv", index=False)
myplan_df.to_csv("verizon_myplan_subscribers.csv", index=False)

# Print a confirmation message
print("CSV files created: verizon_plusplay_subscribers.csv and verizon_myplan_subscribers.csv")
