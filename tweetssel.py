from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up Safari browser
options = webdriver.SafariOptions()
driver = webdriver.Safari(options=options)

# Open Twitter and set cookies
driver.get('https://X.com')

# Safari cookies session
cookies = [
    {"name": "auth_token", "value": "e6f0347763e3d8ee4e43ca613f2aa57dd5531b3d"},
    {"name": "ct0", "value": "c3fa4588456bbfee4782d2c24ef13da6fd173c99d7f29267e33ba42201e5a0e767b3aa4d0b42094da836bfecb3fda41a8223f2d2ffb8d16b8b979f60c045f3b24963d9f731aba86499d403506a49844b"},
    {"name": "guest_id", "value": "172861465098416293"},
    {"name": "personalization_id", "value": "v1_lBSVJboGj8Xt5KQcTgdgig=="}
]

# Adding cookies to the browser
for cookie in cookies:
    driver.add_cookie(cookie)

# Refresh the page after setting cookies to load the authenticated session
driver.refresh()

# Function to perform the search and scroll
def search_and_scrape(hashtag, start_date, end_date, tweet_limit):
    # Open Twitter search page with the hashtag and date range
    search_url = f'https://X.com/search?q=%23{hashtag}+since%3A{start_date}+until%3A{end_date}&f=live'
    driver.get(search_url)
    
    tweets = []
    
    # Start scrolling and collecting tweets
    for _ in range(50):  # Adjust this number to scroll more/less
        # Let the page load
        time.sleep(2)
        
        # Find all tweet elements
        tweet_elements = driver.find_elements(By.CSS_SELECTOR, 'article')
        
        for tweet in tweet_elements:
            try:
                username = tweet.find_element(By.CSS_SELECTOR, 'div[role="link"] span').text
                display_name = tweet.find_element(By.CSS_SELECTOR, 'div[role="link"] div span span').text
                tweet_date = tweet.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
                raw_text = tweet.find_element(By.CSS_SELECTOR, 'div[lang]').text
                
                # Append tweet data
                tweets.append({
                    'username': username,
                    'display_name': display_name,
                    'date': tweet_date,
                    'text': raw_text
                })

                # Stop if we have reached the tweet limit
                if len(tweets) >= tweet_limit:
                    return tweets
            
            except Exception as e:
                print("Error parsing tweet:", e)
        
        # Scroll down
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    return tweets

# Scrape data for #l’immigration
immigration_tweets = search_and_scrape('l'immigration', '2022-06-01', '2022-07-01', 100)

# Scrape data for #changementclimatique
climate_tweets = search_and_scrape('changementclimatique', '2024-07-01', '2024-08-01', 100)

# Print the results
print(f"Collected {len(immigration_tweets)} tweets for #l'immigration")
print(f"Collected {len(climate_tweets)} tweets for #changementclimatique")

# Optional: Save the results to a CSV
import pandas as pd

# Save immigration tweets
df_immigration = pd.DataFrame(immigration_tweets)
df_immigration.to_csv('immigration_tweets.csv', index=False)

# Save climate tweets
df_climate = pd.DataFrame(climate_tweets)
df_climate.to_csv('climate_tweets.csv', index=False)

# Close the browser when done
driver.quit()
