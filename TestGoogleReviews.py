import googlemaps 
import pandas as pd

gmaps = googlemaps.Client(key="AIzaSyDmPGBn_92E5YqUJyTST6RAT5cqrEaWeOE")

place_name = 'Lunchwale'

places_result = gmaps.places(place_name)
place_id = places_result['results']
place_id

#place_id = 'ChIJD8X-Hm8_TIYRqXnk-zs6xm8'
#print(place_id)
place = gmaps.place(place_id = place_id)

reviews = [] #empty list which will hold dictionaries of reviews

for i in range(len(place['result']['reviews'])):
    text = place['result']['reviews'][i]['text']
    rating = place['result']['reviews'][i]['rating']
    
    reviews.append({'rating':rating,
                   'text':text
                   }
                  )
    
df = pd.DataFrame(reviews)
df
    