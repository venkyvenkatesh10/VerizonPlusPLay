import pandas as pd
import random

# Load the input files
plusplay_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\verizon_plusplay_urls.csv'
subscribers_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\randomize_subscriber.csv'
bundles_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\Regular Bundles.txt'

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

# Remove duplicate URLs to avoid repetition and extract app names
plusplay_df_unique = plusplay_df.drop_duplicates(subset=['URL'])

# Randomly assign different app names and URLs to each subscriber
random_assignments = [random.choice(plusplay_df_unique[['App Name', 'URL']].values.tolist()) for _ in range(len(subscribers_df))]

# Create a new DataFrame with the random assignments
random_df = pd.DataFrame(random_assignments, columns=['App Name', 'URL'])

# Update the subscribers DataFrame with the new app names and URLs
subscribers_df['App Name'] = random_df['App Name']
subscribers_df['URL'] = random_df['URL']

# Function to replace "Standard Perks" with the relevant bundle information
def update_perks(app_name, current_perks):
    for bundle, description in bundles_info_dict.items():
        if app_name in description:
            return description if current_perks == "Standard Perks" else current_perks
    return current_perks

# Apply the update perks function
subscribers_df['Perks'] = subscribers_df.apply(lambda row: update_perks(row['App Name'], row['Perks']), axis=1)

# Remove the 'Category_y' column if it exists
if 'Category_y' in subscribers_df.columns:
    subscribers_df.drop(columns=['Category_y'], inplace=True)

# Save the updated subscribers DataFrame back to the original file
output_csv_path = r'C:\Users\venka\Desktop\Verizon Plus play\updated_randomize_subscriber_no_category_y.csv'
subscribers_df.to_csv(output_csv_path, index=False)

print(f"Changes have been saved to: {output_csv_path}")
