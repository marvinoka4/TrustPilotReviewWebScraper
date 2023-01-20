import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import time

# start time
then = time.time()

reviews = []
headings = []
stars = []
dates = []
reviewers = []

# Set number of pages to scrape
pages = np.arange(1, 80, 1)

# Create a loop to go over the reviews
for page in pages:
    page = requests.get("https://uk.trustpilot.com/review/car.co.uk" + "?page=" + str(page))

    soup = BeautifulSoup(page.text, "html.parser")
    # Set the tag we wish to start at
    review_div = soup.find_all('div', class_="styles_cardWrapper__LcCPA")
    review_div1 = soup.find_all('article', class_="paper_paper__1PY90 ")
    review_div2 = soup.find_all('section', class_="styles_reviewContentwrapper__zH_9M")
    review_div3 = soup.find_all('section', class_="styles_consumerDetailsWrapper__p2wdr")

    # loop to iterate through each reviews
    for container in review_div:
        # Get reviewer
        nv = container.find("span", {"class": "typography_heading-xxs__QKBS8 typography_appearance-default__AAY17"}).find_next(text=True).strip()
        reviewers.append(nv)

    for container in review_div2:
        # Get the body of the review
        nv = container.find_all('p', class_='typography_body-l__KUYFJ')
        review = container.p.text if len(nv) == True else '-'
        reviews.append(review)

        # Get the title of the review
        nv1 = container.find_all('h2', class_='typography_heading-s__f7029')
        heading = container.h2.text if len(nv1) == True else '-'
        headings.append(heading)

        # Get the star rating review given
        star = container.find("div", {"class": "star-rating_starRating__4rrcf"}).find('img').get('alt')
        stars.append(star)

        # Get the date
        date = container.find("div", {"class": "typography_body-m__xgxZ_"}).find('time').get('datetime')
        dates.append(date)


# Create a DataFrame using the data
TrustPilot = pd.DataFrame({'Title': headings, 'Body': reviews, 'Rating': stars, 'Date': dates, 'Name': reviewers})

# Clean the white space from data
TrustPilot['Name'] = TrustPilot['Name'].str.strip()
TrustPilot['Body'] = TrustPilot['Body'].str.strip()
TrustPilot['Title'] = TrustPilot['Title'].str.strip()
TrustPilot['Rating'] = TrustPilot['Rating'].str.strip()
TrustPilot['Date'] = TrustPilot['Date'].str.strip()
TrustPilot.to_csv('TrustPilot.csv', index=False)

# Read the csv file
data = pd.read_csv('TrustPilot.csv')

# Split date and time into separate columns
# new = data["Date"].str.split("T", n=1, expand=True)
# data["Date Posted"] = new[0]
# data["Time Posted"] = new[1]
# data.drop(columns=["Date"], inplace=True)
# new = data["Rating"].str.split(":", n=1, expand=True)

# Do what we've done with date to stars
# data["Stars"] = new[0]
# data["Rated"] = new[1]
# data.drop(columns=["Rating"], inplace=True)
# data['Time Posted'] = data['Time Posted'].map(lambda x: str(x)[:-4])
# data['Stars'] = data['Stars'].map(lambda x: str(x)[0:1])

# Arrange the columns order and save it as a csv
data = data[['Title', 'Body', 'Rating', 'Date', 'Name']]
data.to_csv('TrustPilot.csv', index=False)

# End time
now = time.time()
# Show how long the code took to complete
print("It took: ", now - then, "seconds")
