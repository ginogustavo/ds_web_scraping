##Building Dict(json) from a file
import io, time, json
import requests
from bs4 import BeautifulSoup


def paginated_restaurant_search_requests():
    total = 4
    listRequest = []
    listTuple= ()
    limit = 20
    numRequest = 2#int(total/limit)+1
    offset = 1
    jsonf = {}

    for i in range(numRequest):
        filename ='business'+str(i)+'.json'
        print(filename)
        with open(filename) as json_file:
            response_json = json.load(json_file)

        newlist = list(response_json.items())
        jsonf = dict( list(jsonf.items()) + newlist )
        print(jsonf)
    return jsonf


def all_restaurants():
    total_items = 10000
    all_restaurants_request = paginated_restaurant_search_requests()
    return list(all_restaurants_request["businesses"])

#response_json = api_get_request(url, headers, url_params)
#return response_json["total"], list(response_json["businesses"])

data = all_restaurants()
print(len(data))
# 102
print(list(map(lambda x:x['name'], data)))
