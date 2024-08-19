import pandas as pd

# Mapping of app names to their categories
app_category_mapping = {
    "HBO": "Premium Channels",
    "Showtime": "Premium Channels",
    "Starz": "Premium Channels",
    "Cinemax": "Premium Channels",
    "ESPN": "Sports Channels",
    "NBC Sports": "Sports Channels",
    "Fox Sports": "Sports Channels",
    "CNN": "News Channels",
    "TNT": "Entertainment Channels",
    "AMC": "Entertainment Channels",
    "FX": "Entertainment Channels",
    "National Geographic": "Educational Channels",
    "Discovery Channel": "Educational Channels",
    "Cartoon Network": "Kids Channels",
    "Nickelodeon": "Kids Channels",
    "MTV": "Music and Culture Channels",
    "Bravo": "Lifestyle Channels",
    "Comedy Central": "Music and Culture Channels",
    "Food Network": "Lifestyle Channels",
    "HGTV": "Lifestyle Channels",
    "Netflix": "On-Demand Streaming Services",
    "Hulu": "On-Demand Streaming Services",
    "Disney+": "On-Demand Streaming Services",
    "Amazon Prime Video": "On-Demand Streaming Services",
    "Apple TV+": "On-Demand Streaming Services",
    "Peacock": "On-Demand Streaming Services",
    "Paramount+": "On-Demand Streaming Services",
    "HBO Max": "On-Demand Streaming Services",
    "Starz Play": "On-Demand Streaming Services",
    "Showtime Anytime": "On-Demand Streaming Services",
    "Discovery+": "On-Demand Streaming Services",
    "ESPN+": "Live TV Streaming Services",
    "YouTube TV": "Live TV Streaming Services",
    "Sling TV": "Live TV Streaming Services",
    "fuboTV": "Live TV Streaming Services"
}

# Path to the text file containing URLs
file_path = r"C:\Users\venka\Downloads\Url's.txt"

# Reading the URLs from the file
with open(file_path, 'r') as file:
    urls = file.readlines()

# Cleaning and preparing the URLs
urls = [url.strip() for url in urls if url.strip()]

# Creating a DataFrame to store the app names, categories, and URLs
output_data = []

for url in urls:
    for app, category in app_category_mapping.items():
        if app.lower().replace(" ", "") in url:
            output_data.append({"App Name": app, "Category": category, "URL": url})
            break

# Creating a DataFrame from the output data
output_df = pd.DataFrame(output_data)

# Path to save the output CSV file on the Desktop
output_csv_path = r"C:\Users\venka\Desktop\Verizon Plus play\verizon_plusplay_urls.csv"

# Saving the DataFrame to a CSV file
output_df.to_csv(output_csv_path, index=False)

print(f"CSV file saved to: {output_csv_path}")
