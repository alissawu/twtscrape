import asyncio
import pandas as pd
from datetime import datetime
from twscrape import API, gather
import pytz
import time

# Smaller-scale, only for the immigration hashtag 

# French timezone
france_tz = pytz.timezone('Europe/Paris')

async def fetch_tweets_by_hashtag(hashtag, limit, start_date, end_date):
    api = API()  # API instance

    # add acc w/cookies instance, user/pswd/email login
    cookies = "guest_id=172757573503598008; night_mode=2; gt=1840212128994615502; kdt=x3AOtVmlMQYQCUKf0HqHbxGtPhWhg4jDQeFR8BO8; auth_token=2268217e2ff2437081866d5ef8d38242616711c1; ct0=d357c325aedb16204d8cd501990ca7f7225c32e8badeee06998a149fad0a5e13cbb52c0ca7f81e5ad48c453200c75fd0b4902c0e48307da9a5c2e291ad1c6eced33266700a13c9c53c1dd82d85635c4c; att=1-BFvSlu546WDcAj7BE9pwG3qoAzRS6Mr6RIwvwgW9; twid=u%3D1840202902104690688"
    await api.pool.add_account(
        username="allieeroux", 
        password="40R\\4abt*sl5", 
        email="allieeroux@gmail.com", 
        email_password="MfI#u8]1x2W2", 
        cookies=cookies
    )

    collected_tweets = []
    total_tweets_collected = 0

    while total_tweets_collected < limit:
        # Fetch a batch of tweets
        async for tweet in api.search(f'#{hashtag}', limit=limit, kv={"product": "Latest"}):
            tweet_date = tweet.date.astimezone(france_tz)

            # Debugging print with formatted output
            print(f"Found tweet:\n"
                  f"Username: {tweet.user.username}\n"
                  f"Author: {tweet.user.displayname}\n"
                  f"Date: {tweet_date}\n"
                  f"Tweet text: {tweet.rawContent}\n"
                  f"{'-'*40}")

            # Filter tweets within date range
            if start_date <= tweet_date <= end_date:
                collected_tweets.append({
                    "username": tweet.user.username,
                    "author_name": tweet.user.displayname,
                    "date": tweet_date,
                    "tweet_text": tweet.rawContent
                })

            # Stop if we’ve collected enough tweets
            if len(collected_tweets) >= limit:
                break
        
        total_tweets_collected = len(collected_tweets)
        
        # Print the progress
        print(f"Collected {total_tweets_collected}/{limit} tweets so far.")

        # Delay between API calls to avoid rate limiting (1 request per second)
        time.sleep(1)

    return collected_tweets

def run_tweet_scraper(hashtag, limit=100):
    # July 1, 2024 - August 1, 2024
    start_date = france_tz.localize(datetime(2024, 7, 1))
    end_date = france_tz.localize(datetime(2024, 8, 1))

    # Get tweets using asyncio
    tweets = asyncio.run(fetch_tweets_by_hashtag(hashtag, limit, start_date, end_date))

    # Save to Excel
    if tweets:
        df = pd.DataFrame(tweets)
        df.to_excel("tweets_limmigration.xlsx", index=False)
        print(f"Saved {len(tweets)} tweets to tweets_limmigration.xlsx")
    else:
        print("No tweets found in the specified date range.")

if __name__ == "__main__":
    run_tweet_scraper("l%27immigration")
