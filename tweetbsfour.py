import requests
import pandas as pd
from bs4 import BeautifulSoup

# Create session and update cookies
def create_authenticated_session():
    session = requests.Session()

    # Add cookies to session (use your latest cookies)
    cookies = {
        "auth_token": "d060335ccd7ab0a793466b2f173476afe512d0bd",
        "ct0": "88007d9a302646359445414c417b0052eb46ce47ae926bb2ddccf55a928185c0b6c0ec09b47914fa6339a2904acd3170908af4ff9553bfa101b686054144431c8760ee46ecaf613b0c570b42ee14c3c3",
        "guest_id": "v1%3A172861076019299411",
        "personalization_id": "v1_p9xf84iALllUfv8ZdWKYaw=="
    }

    session.cookies.update(cookies)

    # Set headers, including User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8'
    }

    session.headers.update(headers)

    return session


# Function to search tweets and parse results
def search_tweets(session, query, start_date, end_date):
    url = f"https://twitter.com/search?f=live&lang=fr&q={query}+since%3A{start_date}+until%3A{end_date}&src=spelling_expansion_revert_click"

    # Send a request to search page
    response = session.get(url)
    print(response.content)

    
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract tweet details (username, display name, date, text)
        tweets_data = []
        for tweet_div in soup.find_all('div', {'data-testid': 'tweet'}):
            try:
                username = tweet_div.find('a')['href'].split('/')[-1]
                display_name = tweet_div.find('span', {'class': 'css-901oao'}).get_text()
                date = tweet_div.find('time')['datetime']
                tweet_text = tweet_div.find('div', {'lang': 'fr'}).get_text()  # Assumed language is French

                tweets_data.append({
                    'Username': username,
                    'Display Name': display_name,
                    'Date': date,
                    'Text': tweet_text
                })
            except AttributeError:
                continue  # Skip if tweet format is different or missing fields

        return tweets_data

    else:
        raise Exception(f"Error retrieving data: Status code {response.status_code}")


# Save tweets to Excel
def save_tweets_to_excel(tweets, filename):
    df = pd.DataFrame(tweets)
    df.to_excel(filename, index=False)


# Main function to scrape and save tweets
def main():
    session = create_authenticated_session()

    # Search for first hashtag
    query1 = "%23l%27immigration lang:fr"
    immigration_tweets = search_tweets(session, query1, "2022-06-01", "2022-07-01")
    save_tweets_to_excel(immigration_tweets, "immigration_tweets_2022.xlsx")

    # Search for second hashtag
    query2 = "%23changementclimatique lang:fr"
    climate_tweets = search_tweets(session, query2, "2024-07-01", "2024-08-01")
    save_tweets_to_excel(climate_tweets, "climate_tweets_2024.xlsx")


if __name__ == "__main__":
    main()
