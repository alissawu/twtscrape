import snscrape.modules.twitter as sntwitter
import pandas as pd
import requests
from requests.cookies import RequestsCookieJar
import time

# Function to create a session with the cookies
def create_session_with_cookies():
    session = requests.Session()

    # Add the cookies you've extracted
    cookies = RequestsCookieJar()
    cookies.set("auth_token", "d060335ccd7ab0a793466b2f173476afe512d0bd")
    cookies.set("ct0", "88007d9a302646359445414c417b0052eb46ce47ae926bb2ddccf55a928185c0b6c0ec09b47914fa6339a2904acd3170908af4ff9553bfa101b686054144431c8760ee46ecaf613b0c570b42ee14c3c3")
    cookies.set("guest_id", "v1%3A172861076019299411")
    cookies.set("personalization_id", "v1_p9xf84iALllUfv8ZdWKYaw==")

    session.cookies.update(cookies)
    return session

# Function to scrape Twitter data using session with cookies
def scrape_twitter_data(query, start_date, end_date, tweet_limit):
    tweets = []
    scraper = sntwitter.TwitterSearchScraper(query)

    for tweet in scraper.get_items():
        tweet_data = {
            'date': tweet.date,
            'username': tweet.user.username,
            'display_name': tweet.user.displayname,
            'content': tweet.content
        }
        tweets.append(tweet_data)
        if len(tweets) >= tweet_limit:
            break
        # Sleep between requests to avoid hitting rate limits
        time.sleep(1)

    return pd.DataFrame(tweets)

# Example usage
if __name__ == "__main__":
    session = create_session_with_cookies()
    response = session.get('https://X.com/home')
    print(response.status_code)

    
    # First hashtag
    query1 = "#l'immigration since:2022-06-01 until:2022-07-01"
    immigration_df = scrape_twitter_data(query1, "2022-06-01", "2022-07-01", 100)
    immigration_df.to_excel("immigration_tweets_2022.xlsx", index=False)
    
    # Second hashtag
    query2 = "#changementclimatique since:2024-07-01 until:2024-08-01"
    climate_df = scrape_twitter_data(query2, "2024-07-01", "2024-08-01", 100)
    climate_df.to_excel("climate_tweets_2024.xlsx", index=False)
