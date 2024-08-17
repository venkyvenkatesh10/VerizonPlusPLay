import random
import pandas as pd
import uuid

# Define channels and subscriptions with categories
channels = [
    {"name": "Netflix", "price": 22.99, "category": "TV & Movies"},
    {"name": "Peacock", "price": 79.99, "category": "TV & Movies"},
    {"name": "Paramount+", "price": 11.99, "category": "TV & Movies"},
    {"name": "STARZ", "price": 10.99, "category": "TV & Movies"},
    {"name": "AMC+", "price": 4.99, "category": "TV & Movies"},
    {"name": "BET+", "price": 5.99, "category": "Music & Audio"},
    {"name": "ViX Premium", "price": 6.99, "category": "Lifestyle"},
    {"name": "NFL Sunday Ticket", "price": 349.00, "category": "Sports"},
    {"name": "HISTORY Vault", "price": 4.99, "category": "TV & Movies"},
    {"name": "FlixLatino", "price": 3.99, "category": "TV & Movies"},
]

# Define the ZIP codes
zip_codes = [
    "75001", "75201", "75202", "75203", "75204", "75205", "75206", "75207",
    "75208", "75209", "75210", "75211", "75212", "75214", "75215", "75216",
    "75217", "75218", "75219", "75220", "75223", "75224", "75225", "75226",
    "75227", "75228", "75229", "75230", "75231", "75232", "75233", "75234",
    "75235", "75236", "75237", "75238", "75240", "75241", "75243", "75244",
    "75246", "75247", "75248", "75249", "75251", "75252", "75253", "75254",
    "75287"
]

# Generate random subscribers
def generate_subscribers(num):
    subscribers = []
    for i in range(num):
        chosen_channel = random.choice(channels)
        verizon_service = "Verizon MyPlan"  # Focus only on Verizon MyPlan
        subscriber = {
            "Subscriber_ID": str(uuid.uuid4()),  # Generates a unique subscriber ID
            "Channel": chosen_channel["name"],
            "Category": chosen_channel["category"],
            "Days_Watched": random.randint(0, 30),
            "ZIP_Code": random.choice(zip_codes),
            "Verizon_Service": verizon_service,
            "Highlighted": ""  # Empty by default
        }
        subscribers.append(subscriber)
    return pd.DataFrame(subscribers)

# Categorize subscribers as Good or Bad
def categorize_subscribers(df):
    df['Customer_Type'] = df['Days_Watched'].apply(lambda x: 'Good' if x > 10 else 'Bad')
    return df

# Create perks based on customer type and channels
def apply_perks(df):
    perks = []
    for _, row in df.iterrows():
        if row['Customer_Type'] == 'Good':
            if row['Channel'] == 'Netflix' and row['Days_Watched'] > 10:
                perks.append("15% off on Netflix next month")
            elif row['Channel'] == 'NFL Sunday Ticket' and row['Days_Watched'] > 10:
                perks.append("Free month of STARZ")
            else:
                perks.append("Standard Perks")
        elif row['Verizon_Service'] == 'Verizon MyPlan' and row['Customer_Type'] == 'Bad':
            perks.append("Discount on next month's subscription")
        else:
            perks.append("No Perks")
    df['Perks'] = perks
    return df

# Main execution
subscribers_df = generate_subscribers(10000)  # Generate data for 10,000 subscribers
categorized_df = categorize_subscribers(subscribers_df)
final_df = apply_perks(categorized_df)

# Increase days watched for bad Verizon MyPlan subscribers and highlight them
final_df.loc[(final_df['Verizon_Service'] == 'Verizon MyPlan') & (final_df['Customer_Type'] == 'Bad'), 'Days_Watched'] += 5
final_df.loc[(final_df['Verizon_Service'] == 'Verizon MyPlan') & (final_df['Customer_Type'] == 'Bad'), 'Highlighted'] = "Increased Days & Updated Perks"

# Re-categorize subscribers as Good or Bad based on the new days watched
final_df['Customer_Type'] = final_df['Days_Watched'].apply(lambda x: 'Good' if x > 10 else 'Bad')

# Save the updated data to a new CSV file
final_df.to_csv("Updatedperks_myPlan.csv", index=False)

# Analyze the changes for Verizon MyPlan
bad_to_good_myplan = final_df[(final_df['Verizon_Service'] == 'Verizon MyPlan') & (final_df['Customer_Type'] == 'Good')]
print(f"Number of Verizon MyPlan subscribers who moved from Bad to Good: {len(bad_to_good_myplan)}")

# Optional: Save a separate CSV for those who moved from Bad to Good
bad_to_good_myplan.to_csv("verizon_myplan_bad_to_good.csv", index=False)

# Display the first few rows to verify changes
print(final_df.head(20))
