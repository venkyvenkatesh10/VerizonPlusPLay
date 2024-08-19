import pandas as pd

# Load the input files
subscribers_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\verizon1_plusplay_subscribers.csv'
bundles_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\Extra Benefit Bundles.txt'
output_file_path = r'C:\Users\venka\Desktop\Verizon Plus play\verizon_plusplay_bad_to_good_updated.csv'

# Load the Verizon subscribers data
subscribers_df = pd.read_csv(subscribers_file_path)

# Load the Extra Benefit Bundles
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
    bundles_info_dict[key] = "\n".join(bundles_info_dict[key])

# Function to categorize subscribers and assign benefits with a Highlighted column
def categorize_and_assign_benefits(row):
    if row['Days_Watched'] < 10:
        row['Customer_Type'] = 'Bad'
        row['Days_Watched'] = 11  # Increase days watched to convert the customer to "Good"
        for bundle, description in bundles_info_dict.items():
            if row['App Name'] in description:
                row['Perks'] = description
                row['Highlighted'] = f"Upgraded to Good Customer with {bundle}"
                break
        else:
            row['Perks'] = "Standard Perks"
            row['Highlighted'] = "Upgraded to Good Customer with Standard Perks"
    else:
        row['Customer_Type'] = 'Good'
        row['Highlighted'] = "Maintained as Good Customer"
    return row

# Apply the categorization and benefits function
subscribers_df = subscribers_df.apply(categorize_and_assign_benefits, axis=1)

# Select the required columns, excluding 'Category'
final_output = subscribers_df[['Subscriber_ID', 'App Name', 'Days_Watched', 'ZIP_Code', 'Verizon_Service', 'Customer_Type', 'Perks', 'URL', 'Highlighted']]

# Save the updated subscribers DataFrame back to a new CSV file
final_output.to_csv(output_file_path, index=False)

# Display the first 20 rows to verify
print(final_output.head(20))
