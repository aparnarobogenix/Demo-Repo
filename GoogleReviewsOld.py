#import datetime
import logging
import http,urllib.request
import requests
import azure.functions as func
import json
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
import os
from moviepy.editor import *


#def main(mytimer: func.TimerRequest) -> None:
    #utc_timestamp = datetime.datetime.utcnow().replace(
        #tzinfo=datetime.timezone.utc).isoformat()
#url = 'https://surveyedapi.azurewebsites.net/api/Global/AllClientReviewSites'
url = 'https://www.google.com/search?q=lunchwale&sxsrf=AOaemvLZ-sHMANKVxRc8JO-tRR_6VMMOPQ%3A1641899181625&ei=rWTdYd7XJaGYseMPp5qWsA0&ved=0ahUKEwie4uiLx6n1AhUhTGwGHSeNBdYQ4dUDCA4&uact=5&oq=lunchwale&gs_lcp=Cgdnd3Mtd2l6EANKBAhBGABKBAhGGABQAFgAYABoAHAAeACAAQCIAQCSAQCYAQA&sclient=gws-wiz#lrd=0x864c297af83ebf71:0xcf21960db30c0a12,1,,,'
my_headers = {'Content-type': 'application/http','ApiKey' : 'rtDe4#434dr5643eDssdr'}


getting_data = requests.get(url, headers=my_headers)
#print(getting_data.text)
output = BeautifulSoup(getting_data.text, 'html.parser')
print(output)

g_text=json.loads(getting_data.text)

results=[p for p in g_text if p["reviewSiteid"] == 7] 
for result in results  :
    print(result["url"])
    data = urllib.request.urlopen(result["url"]).read()
    #output = http.loads(data)
    #print(output)

    textSentiment=''
    text = ''

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    
    extractedURL =req_body["url"]
    extractedText=req_body['text']
    outputSentiment ="Nothing"

    def textToSentiment(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        #polarity is a score that varies between 1 to +1 . Even polarity can be returend if we really want.
        outputSentiment ="nothing"
        if(polarity < -0.1):
            outputSentiment ="negative"
        elif(-0.1<=polarity<=0.1):
            outputSentiment ="neutral"
        elif(polarity>0.1):
            outputSentiment ="positive"
        print("output sentiment = "+str(outputSentiment))
        return(outputSentiment) 

    try:
        textSentiment = textToSentiment(extractedText)

    except:
        textSentiment = "Error in getting text TextSentiment"

    #reviewlist = output['reviews']
    listdata = []

    r =  requests.get(result["url"])
    #d=data.decode('utf-8')
    #print(d)
    output = BeautifulSoup(r.text, 'html.parser')
    #print(output.text)
    type(output)

    divs1= output.findAll('div',class_='P5Bobd')
    #print(divs1) # title
    
    divs2= output.findAll('div',class_='Jtu6Td')
    #print(divs) # text

    divs3= output.findAll('div',class_='review-score-container')
    #print(divs3) # rating

    divs4= output.findAll('div',class_='dehysf lTi8oc')
    #print(divs4) # time or date

    divs5= output.findAll('div',class_='TSUbDb')
    #print(divs5) # reviewer or user 

    for i in range(10):
        print(divs1[i]) 


    reviews=[]

    for div in divs:
        reviews.append(div.find('p').text)
    print(reviews)
    #reviewlist = output[reviews]
    #print(reviewlist)

    listdata = []
    reviewlist = reviews
    #reviewlist=[]

    for review in reviewlist:
        reviewobject = {}
        reviewobject['reviewTitle'] = review['div1']
        reviewobject['reviewText'] = review['review']
        reviewobject['reviewLink'] = result["url"]
        reviewobject['reviewRating'] = str(review['div3'])
        # reviewobject['reviewSubmittedDate'] = datetime.fromtimestamp(review['timestamp_created']).strftime('%Y-%m-%dT%H:%M:%SZ')
        reviewobject['reviewSubmittedDate'] = 'div4'
        reviewobject['reviewSubmittedBy'] = str(review['div5'])
        reviewobject['sentiment'] = "outputSentiment"
        listdata.append(reviewobject)
        newdata = {
            "clientId": "iyRNsSqQEeSx7bGyHGusMvBOL3t1",
            "reviewSiteId": 7,
            #"reviews": listdata,
            "reviewLink":result["url"],
            }

        url = 'https://surveyedapi.azurewebsites.net/api/Reviews'
        my_headers = {'Content-type': 'application/http','ApiKey' : 'rtDe4#434dr5643eDssdr'}
        x = requests.post(url, headers=my_headers, http=newdata)
        
#    if mytimer.past_due:
#        logging.info('The timer is past due!')

#    logging.info('Python timer trigger function ran at %s', utc_timestamp)



## from selenium import webdriver


## chromedrive_path = './chromedriver' # use the path to the driver you downloaded from previous steps
## driver = webdriver.Chrome(chromedrive_path)
