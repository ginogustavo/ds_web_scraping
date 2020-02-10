#Read paginated search of restaurants from Yelp api_key
#Requires api_key

import io, time, json
import requests
from bs4 import BeautifulSoup

def retrieve_html(url):
    #r = requests.get(url, auth=('user', 'pass'))
    r = requests.get(url)
    return (r.status_code,r.text)

#print(retrieve_html('https://www.nytimes.com/2019/03/29/technology/youtube-online-extremism.html'))
#print(r.text)

def read_api_key(filepath):
    """
    Read the Yelp API Key from file.

    Args:
        filepath (string): File containing API Key
    Returns:
        api_key (string): The API Key
    """

    # feel free to modify this function if you are storing the API Key differently
    with open(filepath, 'r') as f:
        return f.read().replace('\n','')


def api_get_request(url, headers, url_params):
    http_method = 'GET'
    r = requests.request(http_method,url, headers=headers, params=url_params)
    #r = requests.get(url, headers=headers, params=url_params)
    #response = r.text
    #response = r.json()
    return r


def location_search_params(api_key, location, **kwargs):

    # What is the url endpoint for search?
    url = 'https://api.yelp.com/v3/businesses/search'

    # How is Authentication performed?
    headers = {'Authorization': 'Bearer %s' % api_key,}
    # SPACES in url is problematic. How should you handle location containing spaces?
    #url_params = [YOUR CODE HERE]

    url_params = {}
    url_params['location']=location.replace(' ', '+')
    for name, value in kwargs.items():
        url_params[name] = value

    return url, headers, url_params

def yelp_search(api_key, location, offset=0):
    url, headers, url_params = location_search_params(api_key, location, offset=0)

    response_json = api_get_request(url, headers, url_params).json()

    return response_json["total"], list(response_json["businesses"])


api_key = read_api_key('yelp_api_key.txt')
num_records, data = yelp_search(api_key, 'Chicago')
print(num_records)
#8500
print(len(data))
#20
print(list(map(lambda x: x['name'], data)))


# 4% credit
def paginated_restaurant_search_requests(api_key, location, total):
    # HINT: Use total, offset and limit for pagination
    # You can reuse function location_search_params(...)
    listRequest = []
    limit = 20
    numRequest =int(total/limit)+1
    offset = 0
    for i in range(numRequest):
        url, headers, url_params = location_search_params(api_key, location, offset=offset,limit=limit, categories="restaurants")
        singleTuple = (url, headers, url_params)
        listRequest.append(singleTuple)
        offset +=20

    return listRequest

# 3% credit
def all_restaurants(api_key, location):
    # What keyword arguments should you pass to get first page of restaurants in Yelp
    url, headers, url_params = location_search_params(api_key, location, offset=0, categories="restaurants" )
    response_json = api_get_request(url, headers, url_params).json()
    total_items = response_json["total"]

    tupleList = paginated_restaurant_search_requests(api_key, location, total_items)
    globalList = []
    for tup in tupleList:
        res = api_get_request(tup[0], tup[1], tup[2]).json()
        businessList = res.get('businesses') # The list from busines
        for bussiness in businessList:
            globalList.append(bussiness)     #Adding each bussines to the gloab

        time.sleep(0.5)

    all_restaurants_request = {"businesses": globalList}
    return list(all_restaurants_request["businesses"])

#response_json = api_get_request(url, headers, url_params)
#return response_json["total"], list(response_json["businesses"])

api_key = read_api_key('yelp_api_key.txt')
data = all_restaurants(api_key, 'Greektown, Chicago, IL')
print(len(data))
# 102
print(list(map(lambda x:x['name'], data)))


def parse_api_response(data):
    jsonDict = json.loads(data)
    listUrls = []
    for p in jsonDict['businesses']:
        listUrls.append(p['url'])
    return listUrls


url, headers, url_params = location_search_params(api_key, "Chicago", offset=0)
response_text = api_get_request(url, headers, url_params).text
parse_api_response(response_text)
# ['https://www.yelp.com/biz/girl-and-the-goat-chicago?adjust_creative=ioqEYAcUhZO272qCIvxcVA....',
#  'https://www.yelp.com/biz/wildberry-pancakes-and-cafe-chicago-2?adjust_creative=ioqEYAcUhZO272qCIvxcVA...',..]
