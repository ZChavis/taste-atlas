from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import wikipedia
import urllib
import random


def binary_search(array, element): # function for binary search to increase search efficiency
    start = 0 # sets a value for where the binary search will start
    end = len(array) - 1 # sets a value for where the search will end -1 as the list is 0 indexed
    found = False # variable to hold whether the target value has been found
    while (start <= end and not found): # while the search is not at the end of the list and the target has not been found
        mid = (start + end) // 2 # find the middle and store it in a variable
        if element == array[mid]: # if the target is found
            found = True # set found to true
        else:
            if element < array[mid]: # if the target is less than the middle value
                end = mid - 1 # begin the search next time in the front half of the total list
            else:
                start = mid + 1 # otherwise begin the search next time in the back half of the list
    return found # return the value of found to say if the search was successful


url = "https://www.worldometers.info/geography/alphabetical-list-of-countries/" # url to scrape for the countries
url2 = "https://naturalhealthtechniques.com/list-of-meats-and-poultry/" # url to scrape for the meats


header = {
   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
   "X-Requested-With": "XMLHttpRequest" # spoofs browser info to access an "https" site
}


r = requests.get(url, headers = header) # use the country url and spoof browser info
r2 = requests.get(url2, headers = header) # use the meats url and spoof browser info


df = pd.read_html(r.text)[0] # read the first column of the table in the country url


meats = [] # sets list to hold the meats
data = BeautifulSoup(r2.text, 'html.parser') # uses BS to access the meats url
data1 = data.find('body').find('div') # start reading the meats url by finding the body and then the divs
for li in data1.find_all("li"): # find all of the 'li's in the divs
    meats.append(li.text) # add the text of each 'li' to the list
del meats[:6] # cleans some unnecessary elements that were read from the front of the list
del meats[-5:] # cleans some unnecessary elements that were read from the back of the list
#following block is to further clean some unnecessary or verbose
meats.remove('Bone soup from allowable meats')
meats.append('Bone soup')
meats.remove('Buffalo, Bison')
meats.append('Buffalo')
meats.append('Bison')
meats.remove('Pork, Bacon')
meats.append('Bacon')


data_path = Path('C:\\Users\zrcha\OneDrive\Desktop\side_projects\_foodStuff') # sets the path of the target file
data_file = Path('herbs_n_spices2.json') # sets the name of the target file
data = pd.read_json(data_path / data_file, orient='index') # read the file and orients the output of the info
data.head() # prints first few rows of data frame
# print(data.index) # prints list of indices of data frame
herbs = data.loc['herbs'][0] # list of herbs
spices = data.loc['spices'][0] # list of spices
mixtures = data.loc['mixtures'][0] # list of mixtures


dataSet = herbs + spices + mixtures + meats # combines all lists into one large dataset


for i in range(len(dataSet)): # for loop to go through all values in the dataset
    dataSet[i] = dataSet[i].lower() # sets all elements in the dataset to lowercase for ease of searching
dataSet.sort() # sorts all elements in the dataset for ease of searching


crossOver = [] # creates list to hold any cross referenced values
testString = '' # creates variable to hold the string to search against the dataset elements


for country in df["Country"]: # for each value read from the country url
    country = re.sub("\([^)]*\)", "", country) # deletes parentheses and everything in between
    print(country) # print the country that is being referenced

    # following block of substitutions is to clean the data for properly searching
    # for each country using the wikipedia api
    country = re.sub("Chile", "Chilean", country)
    country = re.sub("China", "Chinese", country)
    country = re.sub("Equatorial ", "", country)
    country = re.sub("Iceland", "Icelandic", country)
    country = re.sub("Malawi", "Malawian", country)
    country = re.sub("Mali", "Malian", country)
    country = re.sub("Korea", "Korean", country)
    country = re.sub("South Africa", "South African", country)
    country = re.sub("Suriname", "Surinamese", country)

    if country == "Tonga": # if the country is Tonga, special cleaning has to be done
        testString = wikipedia.page("Culture of Tonga").content
        testString = testString.split() # splits the long string from wikipedia page into individual words and converts to a list
        for i in range(len(testString)): # for the length of the country's wikipedia content
            testString[i] = testString[i].lower() # convert to lowercase for ease of searching
            testString[i] = testString[i].replace(',', '') # clean the data of any commas
        for i in range(len(testString)): # for the length of the country's wikipedia content
            if binary_search(dataSet, testString[i]): # search each word of the wikipedia content through the dataset and if found
                tempValue = testString[i] # set a temp value to equal the cross referenced element
                crossOver.sort() # sorts all elements in the list for ease of searching
                if not binary_search(crossOver, tempValue):  # if the temp value is already in the list of cross referenced values
                    crossOver.append(tempValue)  # otherwise, add the new value into the list of cross referenced values
                else:
                    '' # do nothing

    else:
        testString = wikipedia.page(country + " cuisine").content # sets the info from the country's wikipedia page to a variable
        testString = testString.split() # splits the long string from wikipedia page into individual words and converts to a list
        for i in range(len(testString)): # for the length of the country's wikipedia content
            testString[i] = testString[i].lower() # convert to lowercase for ease of searching
            testString[i] = testString[i].replace(',', '') # clean the data of any commas
        for i in range(len(testString)): # for the length of the country's wikipedia content
            if binary_search(dataSet, testString[i]): # search each word of the wikipedia content through the dataset and if found
                tempValue = testString[i] # set a temp value to equal the cross referenced element
                crossOver.sort() # sorts all elements in the list for ease of searching
                if not binary_search(crossOver, tempValue): # if the temp value is already in the list of cross referenced values
                    crossOver.append(tempValue) # otherwise, add the new value into the list of cross referenced values
                else:
                    '' # do nothing

    print(crossOver) # print the crossover list for the current country
    print('')
    crossOver.clear() # clear the crossover list in preparation for the next country

