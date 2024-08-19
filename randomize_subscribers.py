import pandas as pd
import random

# Load the input files
bundles_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\Regular Bundles.txt'
plusplay_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\verizon_plusplay_urls.csv'
subscribers_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\verizon_subscribers.csv'

# Load the Verizon PlusPlay URLs and Subscribers data
plusplay_df = pd.read_csv(plusplay_file_path)
subscribers_df = pd.read_csv(subscribers_file_path)

# Load the Regular Bundles
with open(bundles_file_path, 'r') as file:
    bundles_info = file.read()

# Process bundles into a dictionary
bundles_info_dict = {}
current_bundle = ""
for line in bundles_info.splitlines():
    if line.startswith("Bundle"):
        current_bundle = line.split(":")[0].strip()
        bundles_info_dict[current_bundle] = [line]
    elif current_bundle and line.strip():
        bundles_info_dict[current_bundle].append(line.strip())

# Convert the bundle list into a single string with newlines
for key in bundles_info_dict.keys():
    bundles_info_dict[key] = "\\n".join(bundles_info_dict[key])

# Rename 'Channel' to 'App Name' in the subscriber data
subscribers_df.rename(columns={'Channel': 'App Name'}, inplace=True)

# Check if 'URL' is in verizon_plusplay_urls.csv and use a suitable column from verizon_subscribers.csv
if 'URL' in plusplay_df.columns:
    # Perform the merge on 'App Name' and 'URL'
    merged_df = pd.merge(subscribers_df, plusplay_df, how='left', on=['App Name'])

    # Include the 'URL' column in the final output
    merged_df['URL'] = merged_df['URL']

    # Function to replace the Perks based on bundles
    def update_perks(app_name, current_perks):
        for bundle, description in bundles_info_dict.items():
            if app_name in description:
                return description if current_perks == "Standard Perks" else current_perks
        return current_perks

    # Apply the update perks function
    merged_df['Perks'] = merged_df.apply(lambda row: update_perks(row['App Name'], row['Perks']), axis=1)

    # Save the updated subscribers DataFrame to a new file
    output_csv_path = r'C:\Users\venka\Desktop\Verizon Plus play\randomize_subscriber.csv'
    merged_df.to_csv(output_csv_path, index=False)

    print(f"Changes have been saved to: {output_csv_path}")
else:
    print("The 'URL' column is missing in verizon_plusplay_urls.csv. Please check your CSV file.")
