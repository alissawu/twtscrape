from tweety import Twitter
from datetime import datetime
import pytz
from tweety.filters import SearchFilters
import pandas as pd

# Paste your cookies here
cookies_value = """
guest_id=v1%3A172861076019299411; auth_token=d060335ccd7ab0a793466b2f173476afe512d0bd; ct0=88007d9a302646359445414c417b0052eb46ce47ae926bb2ddccf55a928185c0b6c0ec09b47914fa6339a2904acd3170908af4ff9553bfa101b686054144431c8760ee46ecaf613b0c570b42ee14c3c3; twid=u%3D1844554386065784841; personalization_id="v1_kjkPNVyMs+2CTLLqrKodzA==";
"""

# Initialize the Twitter session using cookies
app = Twitter("session_name")
app.load_cookies(cookies_value)

# Function to scrape tweets by hashtag and date range with debugging
def scrape_tweets_by_hashtag(hashtag, start_date, end_date, max_tweets=100):
    results = []
    tweets = app.search(hashtag, filter_=SearchFilters.Latest())  # Searching latest tweets
    
    print(f"\nSearching for tweets with hashtag: {hashtag}")
    print(f"Start Date (Paris TZ): {start_date}, End Date (Paris TZ): {end_date}")
    
    total_fetched = 0
    
    for tweet in tweets:
        tweet_date = tweet.date
        
        # Debug: Print the tweet's date
        print(f"Tweet found with date: {tweet_date} - Checking date range...")

        # Ensure comparison is between offset-aware datetimes
        if start_date <= tweet_date <= end_date:
            print(f"Tweet within date range: {tweet_date}")
            # Collect necessary details: username, display name, date, and tweet text
            tweet_data = {
                'Username': tweet.author.username,
                'Display Name': tweet.author.name,
                'Date': tweet.date,
                'Text': tweet.text
            }
            results.append(tweet_data)
            total_fetched += 1
            if len(results) >= max_tweets:
                break
    
    print(f"Total tweets fetched for hashtag '{hashtag}': {total_fetched}")
    return results

# Function to save tweets into an Excel file
def save_to_excel(tweet_data, filename):
    # Convert the list of tweets into a DataFrame
    df = pd.DataFrame(tweet_data)
    
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Saved {len(df)} tweets to {filename}")

# Set the hashtags and date ranges
hashtag_immigration = "#l’immigration"
hashtag_climate = "#changementclimatique"

# Define the Paris timezone
paris_tz = pytz.timezone('Europe/Paris')

# Define the date ranges in Paris timezone
start_date_2024 = paris_tz.localize(datetime(2024, 7, 1))
end_date_2024 = paris_tz.localize(datetime(2024, 8, 1))

start_date_2022 = paris_tz.localize(datetime(2022, 6, 1))
end_date_2022 = paris_tz.localize(datetime(2022, 7, 1))

# Scrape tweets for the required queries with debugging
immigration_tweets_2024 = scrape_tweets_by_hashtag(hashtag_immigration, start_date_2024, end_date_2024, max_tweets=100)
immigration_tweets_2022 = scrape_tweets_by_hashtag(hashtag_immigration, start_date_2022, end_date_2022, max_tweets=100)
climate_tweets_2024 = scrape_tweets_by_hashtag(hashtag_climate, start_date_2024, end_date_2024, max_tweets=100)

# Save the results to separate Excel files
save_to_excel(immigration_tweets_2024, 'immigration_tweets_2024.xlsx')
save_to_excel(immigration_tweets_2022, 'immigration_tweets_2022.xlsx')
save_to_excel(climate_tweets_2024, 'climate_tweets_2024.xlsx')
