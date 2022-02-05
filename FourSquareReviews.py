### Notes:
## 1) function textToSentiment: is used to convert text to sentiment. 
##        where polarity is a score that varies between -1 to +1 . 
##        Here -1 is negative, +1 is positive, 0 is neutral, also if empty in reviews then will show neutral

## 2) function main i.e. timer request function is used to set the timestamp and converts into required format
## 3) getting data from endpoint url and extracting place_name from each url and passing it to outscrapper 
##    function using node.js 
## 4) function reviewDataInformation: is used to get all the information of the review data,
##    using required parameters and appending it to listdata variable.

#imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from datetime import date
import math
from textblob import TextBlob
import json
import azure.functions as func

# yesterday's timestamp - from current date time till previous mentioned date. 
yesterday_timestamp = int((datetime.now() - timedelta(1)).timestamp())

# function to extract all the required information 
def reviewDataInformation(site_id,latestdate):
    listdata= [] # empty list

    #key="one" if key in mydict: print("Key exists") else: print("Key does not exist")
    r =  requests.get('https://apps.apple.com/us/app/foursquare-city-guide/id306934924')
    #r =  requests.get('https://docs.microsoft.com/en-us/azure/cosmos-db/sql/create-sql-api-python')

    r.status_code

    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup)
    #type(soup)
    for divs in soup:
        divs= soup.findAll('div',class_='we-customer-review lockup')
        print(divs)

    # divs= soup.findAll('div',class_='we-customer-review lockup')
    # print(divs)

    len(divs)

    reviews=[]
    for div in divs:
        reviews.append(div.find('p').text)
        reviews.append(div.find('figure'))

    print(reviews[:])
    reviewobject = {}
    reviewobject['review_title'] = pd.DataFrame(np.array(reviews), columns=['review_title'])
    print(reviewobject['review_title'])
    reviewobject['review_text'] = pd.DataFrame(np.array(reviews), columns=['review_text'])
    print(reviewobject['review_text'])
    reviewobject['review_link'] = pd.DataFrame(np.array(reviews), columns=['review_link'])
    print(reviewobject['review_link'])
    reviewobject['review_rating'] = pd.DataFrame(np.array(reviews), columns=['review_rating'])
    print(reviewobject['review_rating'])
    reviewobject['date_submitted'] = datetime.fromtimestamp(pd.DataFrame(np.array(reviews), columns=['date_submitted'])).isoformat()
    print(reviewobject['date_submitted'])
    reviewobject['review_sentiment'] = textToSentiment(pd.DataFrame(np.array(reviews), columns=['review_sentiment']))
    listdata.append(reviewobject)
    print('\n')
            #print(listdata)
    return(listdata)

    # if "reviews" in reviews[0]:
        
    #     print('Total number of Foursquare reviews present are:',reviews[0]['reviews'],'\n')

    #     for i in range(0,len(reviews[0]['reviews_data']),1):
    #         reviewobject = {}
    #         print(i)
    #         reviewobject['reviewTitle'] =reviews[0]['reviews_data'][i]['author_title']
    #         print('Name:', reviewobject['reviewTitle'])
    #         reviewobject['reviewText'] =reviews[0]['reviews_data'][i]['review_text']
    #         #print('Review:',reviewobject['reviewText'])
    #         reviewobject['reviewLink'] =reviews[0]['reviews_data'][i]['review_link']
    #         #print('Review Link:',reviewobject['reviewLink'])
    #         reviewobject['reviewRating'] =str(reviews[0]['reviews_data'][i]['review_rating'])
    #         #print('Rating:',reviewobject['reviewRating'])
    #         reviewobject['reviewSubmittedDate'] =datetime.fromtimestamp(reviews[0]['reviews_data'][i]['review_timestamp']).isoformat()
    #         print(reviews[0]['reviews_data'][i]['review_timestamp'])
    #         print('Review Date:',reviewobject['reviewSubmittedDate'])
    #         reviewobject['sentiment'] = textToSentiment(reviews[0]['reviews_data'][i]['review_text'])
    #         #Review_sentiment = 'textToSentiment'
    #         listdata.append(reviewobject)
    #         print('\n')
    #         #print(listdata)
    #     return(listdata)
    # else:
    #     print("No Reviews were found yesterday")  
    #     return([])

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

results=[p for p in g_text if p["reviewSiteid"] == 7] 
for result in results  :
    p_url = result["url"]
    print(p_url)
    site_id = (p_url.split('/')[-1])
    print("Site Id:",site_id)

listdata= [] # empty list

## This url is used to get the client id 
url = f'https://surveyedapi.azurewebsites.net/api/Reviews/{result["clientId"]}/7'
## ApiKey to access above url 
my_headers = {'Content-type': 'application/http','ApiKey' : 'rtDe4#434dr5643eDssdr'} 

getting_data = requests.get(url, headers=my_headers) # url and headers extraction
#print(getting_data.text)

g_text=json.loads(getting_data.text) # client existing review list in the database
len_of_reviews = len(g_text["reviewsList"])
print(g_text['reviewsList'][0]["reviewSubmittedDate"]) # first date in the database without sorting 
#g_text["reviewsList"].sort(key=lambda item:datetime.strptime(item["reviewSubmittedDate"],"%Y-%m-%dT%H:%M:%S"), reverse=True)
#latest_date = g_text["reviewsList"].map(key=lambda item:print(item['reviewTitle']))

latestdate = g_text['reviewsList'][0]["reviewSubmittedDate"] # latest date in the database after sorting
print(latestdate)
#latestdate_timestamp = math.floor(datetime.timestamp(datetime.strptime(latestdate,"%Y-%m-%dT%H:%M:%S")))
#print(latestdate_timestamp)
if len_of_reviews==0:
    listdata = reviewDataInformation(True,site_id)  
else:
    listdata = reviewDataInformation(False,site_id)  

newdata = {
            "clientId": result["clientId"],
            #"clientId": 'lxvHfNEqiXYXW1y7OU5Vvje8GAQ2',
            "reviewSiteId": 7,
            "reviews": listdata,
            }
if len(listdata) > 0:
    # post request
    url2 = 'https://surveyedapi.azurewebsites.net/api/Reviews'   
    my_headers = {'Content-type': 'application/json','ApiKey' : 'rtDe4#434dr5643eDssdr'}
    x = requests.post(url2, headers=my_headers, json=newdata)
    print(x.text)  
else:
    print("Nothing to post")

today = date.today()
print("Todays Date:",today)





## Actual foursqaure raw code:
# r =  requests.get('https://apps.apple.com/us/app/foursquare-city-guide/id306934924')
# #r =  requests.get('https://docs.microsoft.com/en-us/azure/cosmos-db/sql/create-sql-api-python')

# r.status_code

# soup = BeautifulSoup(r.text, 'html.parser')
# #print(soup)
# #type(soup)
# for divs in soup:
#     divs= soup.findAll('div',class_='we-customer-review lockup')
#     print(divs)

# # divs= soup.findAll('div',class_='we-customer-review lockup')
# # print(divs)

# len(divs)

# reviews=[]
# for div in divs:
#     reviews.append(div.find('p').text)

# print(reviews[:])
# df =pd.DataFrame(np.array(reviews), columns=['review'])
# print(df)
    


