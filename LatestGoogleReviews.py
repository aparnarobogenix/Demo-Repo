### Notes:
## 1) function textToSentiment: is used to convert text to sentiment. 
##        where polarity is a score that varies between -1 to +1 . 
##        Here -1 is negative, +1 is positive, 0 is neutral, also if empty in reviews then will show neutral

## 2) function main i.e. timer request function is used to set the timestamp and converts into required format
## 3) getting data from endpoint url and extracting place_id from each url and passing it to outscrapper function
## 4) Using outscrapper api client key access and should use extracted place_id from previous step 
## 5) function reviewDataInformation: is used to get all the information of the review data,
##    using required parameters and appending it to listdata variable.

## Required Installations:
## pip install google-maps-reviews - allows fetching Google Maps reviews from any place
## pip install google-services-api - allows using Outscraper's services and Outscraper's API.

# Required Imports
from outscraper import ApiClient
from textblob import TextBlob
import pandas as pd
from googleapiclient import sample_tools
import requests
import azure.functions as func
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from datetime import date
import math

# yesterday's timestamp - from current date time till previous mentioned date. 
yesterday_timestamp = int((datetime.now() - timedelta(1)).timestamp())


def reviewDataInformation(condition,p_id,latestdate):
    #place_name = 'Lunchwale.co'
    #place_name = place_name
    listdata= [] # empty list
    # OutScrapper api key
    api_client = ApiClient(api_key='Z29vZ2xlLW9hdXRoMnwxMDkyMjAxMTIzNzE2MzA3ODgzNDl8MGQ2NDA4ZWU4YQ')
    if condition: 
        reviews_response = api_client.google_maps_business_reviews(
        p_id, reviewsLimit=100,language='en')
    else:
        reviews_response = api_client.google_maps_business_reviews(
        p_id, sort='newest', cutoff=latestdate, language='en')
        # reviews_response = api_client.google_maps_business_reviews(
        # p_id, sort='newest', cutoff=yesterday_timestamp, language='en')

    print(reviews_response)
    print(len(reviews_response[0]['reviews_data']))

    #key="one" if key in mydict: print("Key exists") else: print("Key does not exist")
    if "reviews" in reviews_response[0]:
        
        print('Total number of Google map reviews present are:',reviews_response[0]['reviews'],'\n')

        for i in range(0,len(reviews_response[0]['reviews_data']),1):
            reviewobject = {}
            print(i)
            reviewobject['reviewTitle'] =reviews_response[0]['reviews_data'][i]['author_title']
            print('Name:', reviewobject['reviewTitle'])
            reviewobject['reviewText'] =reviews_response[0]['reviews_data'][i]['review_text']
            #print('Review:',reviewobject['reviewText'])
            reviewobject['reviewLink'] =reviews_response[0]['reviews_data'][i]['review_link']
            #print('Review Link:',reviewobject['reviewLink'])
            reviewobject['reviewRating'] =str(reviews_response[0]['reviews_data'][i]['review_rating'])
            #print('Rating:',reviewobject['reviewRating'])
            reviewobject['reviewSubmittedDate'] =datetime.fromtimestamp(reviews_response[0]['reviews_data'][i]['review_timestamp']).isoformat()
            print(reviews_response[0]['reviews_data'][i]['review_timestamp'])
            print('Review Date:',reviewobject['reviewSubmittedDate'])
            reviewobject['sentiment'] = textToSentiment(reviews_response[0]['reviews_data'][i]['review_text'])
            #Review_sentiment = 'textToSentiment'
            listdata.append(reviewobject)
            print('\n')
            #print(listdata)
        return(listdata)
    else:
        print("No Reviews were found yesterday")  
        return([])

## function used to convert text to sentiment
textSentiment=''
text = ''
def textToSentiment(review_text):
    if review_text is not None:
        blob = TextBlob(review_text)
        polarity = blob.sentiment.polarity
##polarity is a score that varies between -1 to +1 . Even polarity can be returend if we really want.
        outputSentiment ="nothing"
        if(polarity < -0.1):
            outputSentiment ="negative"
        elif(-0.1<=polarity<=0.1):
            outputSentiment ="neutral"
        elif(polarity>0.1):
            outputSentiment ="positive"
        print("output sentiment = "+str(outputSentiment))
        return(outputSentiment) 
    else:
        return("neutral")
    try:
        textSentiment = textToSentiment(Review_text)

    except:
        textSentiment = "Error in getting text TextSentiment"  

## Timer Request function:
def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

## url is used to get all review sites using end point url from surveyed.
url = 'https://surveyedapi.azurewebsites.net/api/Global/AllClientReviewSites'
## ApiKey to access above url 
my_headers = {'Content-type': 'application/http','ApiKey' : 'rtDe4#434dr5643eDssdr'} 

getting_data = requests.get(url, headers=my_headers) # url and headers extraction
print(getting_data.text)

g_text=json.loads(getting_data.text) # clientId and review url we are getting

results=[p for p in g_text if p["reviewSiteid"] == 1] 
for result in results  :
    p_url = result["url"]
    print(p_url)
    p_id = (p_url.split('=')[-1])
    print("Place Id:",p_id)
        
    ##To print the total number of reviews present in the google map reviews
    #print('Total number of Google map reviews present are:',reviews_response[0]['reviews'],'\n')

    listdata= [] # empty list

    ## This url is used to get the client id 
    url = f'https://surveyedapi.azurewebsites.net/api/Reviews/{result["clientId"]}/1'
    ## ApiKey to access above url 
    my_headers = {'Content-type': 'application/http','ApiKey' : 'rtDe4#434dr5643eDssdr'} 

    getting_data = requests.get(url, headers=my_headers) # url and headers extraction
    #print(getting_data.text)

    g_text=json.loads(getting_data.text) # client existing review list in the database
    len_of_reviews = len(g_text["reviewsList"])
    print(g_text['reviewsList'][0]["reviewSubmittedDate"]) # first date in the database without sorting 
    g_text["reviewsList"].sort(key=lambda item:datetime.strptime(item["reviewSubmittedDate"],"%Y-%m-%dT%H:%M:%S"), reverse=True)
    #latest_date = g_text["reviewsList"].map(key=lambda item:print(item['reviewTitle']))

    latestdate = g_text['reviewsList'][0]["reviewSubmittedDate"] # latest date in the database after sorting
    print(latestdate)
    latestdate_timestamp = math.floor(datetime.timestamp(datetime.strptime(latestdate,"%Y-%m-%dT%H:%M:%S")))
    print(latestdate_timestamp)
    if len_of_reviews==0:
        listdata = reviewDataInformation(True,p_id)  
    else:
        listdata = reviewDataInformation(False,p_id, latestdate_timestamp)  

    newdata = {
                "clientId": result["clientId"],
                #"clientId": 'lxvHfNEqiXYXW1y7OU5Vvje8GAQ2',
                "reviewSiteId": 1,
                "reviews": listdata,
                }
    # if len(listdata) > 0:
    #     # post request
    #     url2 = 'https://surveyedapi.azurewebsites.net/api/Reviews'   
    #     my_headers = {'Content-type': 'application/json','ApiKey' : 'rtDe4#434dr5643eDssdr'}
    #     x = requests.post(url2, headers=my_headers, json=newdata)
    #     print(x.text)  
    # else:
    #     print("Nothing to post")

today = date.today()
print("Todays Date:",today)

