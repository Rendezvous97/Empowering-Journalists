# -*- coding: utf-8 -*-
#Importing required libraries
import os
import io
import sys
from bs4 import BeautifulSoup
import requests
import array as arr
import six as six
import gensim

from google.cloud import vision
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

print("--------------------------------------------------------------------------------")
print("----- Welcome to the journalists' tool for checking image title relevance ------")
print("--------------------------------------------------------------------------------")
print("Please give the system a minute to import the required files...")
print("--------------------------------------------------------------------------------")

#Path to the api key to use google Vision and Language API
credential_path = "<ENTER FULL PATH TO THE API KEY JSON FILE>"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

#Title that is associated to the image in question
given_title = "<ENTER THE ASSOCIATED TITLE>"

#Full Path to the image in question
image_path = "<ENTER FULL PATH TO THE IMAGE>"

#Examples
#given_title = "PM is most followed leader on instagram."
#image_path = "/Users/apple/Desktop/Modi3.jpg"

# given_title = "Footage shows missing Saudi journalist Jamal Khashogg."
# image_path = "/Users/apple/Desktop/embassy.jpg"

#Loading the google text corpus trained on word2vec
model = gensim.models.KeyedVectors.load_word2vec_format('/Users/apple/Desktop/GoogleNews-vectors-negative300.bin.gz', binary=True, limit = 500000)

#Credible list of URLs - can be chnged by user
credible = ['economictimes.', 'huffingtonpost.', 'theprint.', 'thelogicalindian.', 'thequint.', 'altnews.', 'wsj.', 'nypost.', 'nytimes.', 'bbc.', 'reuters.', 'economist.', 'pbs.', 'aljazeera.', 'thewire.', 'theatlantic.', 'theguardian.', 'edition.cnn',
            'cnbc.', 'scroll.in', 'financialexpress.', 'npr.', 'usatoday.', 'snopes.', 'politifact.']


#---------------------#--------------------#---------------------#--------------------#
#Function for entity analysis of the titles
def entity_sentiment_text(text):
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detect and send native Python encoding to receive correct word offsets.
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    result = client.analyze_entity_sentiment(document, encoding)

    for entity in result.entities:
        print('Mentions: ')
        print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            #print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            #print(u'  Sentiment : {}'.format(mention.sentiment.score))
            #print(u'  Type : {}'.format(mention.type))
        print(u'Salience: {}'.format(entity.salience))
        #print(u'Sentiment: {}\n'.format(entity.sentiment))
        print("--------------------------------------------------------------------------------")

#---------------------#--------------------#---------------------#--------------------#
#Function for google's clous vision API
def detect_web(path):
    list = []
    i = 0
    """Detects web annotations given an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess for the image: {}'.format(label.label))
            print("--------------------------------------------------------------------------------")


    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('\n\tPage url   : {}'.format(page.url))
            list.append(page.url)

    if annotations.web_entities:
        print('\n{} Web entities found in the image: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

        for image in annotations.visually_similar_images:
            print('\tImage url    : {}'.format(image.url))
    print("--------------------------------------------------------------------------------")
    return(list)
#---------------------#--------------------#---------------------#--------------------#
#Function to check which URLs belong to credible news sources
def credible_list(list_of_page_urls):

    c_list = []

    c_length = len(credible)

    url_length = len(list_of_page_urls)

    f = [[0 for j in range(c_length)] for i in range(url_length)]
    for i in range(url_length):
        for j in range(c_length):
            f[i][j] = list_of_page_urls[i].find(credible[j])
            if((list_of_page_urls[i].find(credible[j])) > 0):
                c_list.append(list_of_page_urls[i])
    if c_list == []:
        print("No credible sources have used this image, please perform human verification.")
        print("--------------------------------------------------------------------------------")
        exit(1)
    return(c_list)
#---------------------#--------------------#---------------------#--------------------#
#Function to scrape titles off the given URLs
def titles(credible_from_url_list):

    title_list = []

    for urls in credible_from_url_list:
        if urls != []:
            r = requests.get(urls)
            html = r.content
            soup = BeautifulSoup(html, 'html.parser')
            title_list.append(soup.title.string)

    return(title_list)

#---------------------#--------------------#---------------------#--------------------#
#Function to print the scraped titles
def print_article_title(title_list):
    print("Credible article titles which use the same image: ")
    print("--------------------------------------------------------------------------------")
    for title in title_list:
        print(title)
        print("--------------------------------------------------------------------------------")
#---------------------#--------------------#---------------------#--------------------#
#Function to call google's language API for entity analysis
def entity_analysis(title_list):
    for title in title_list:
        entity_sentiment_text(title)

#---------------------#--------------------#---------------------#--------------------#
#Function to compute the WM distances between titles and associated title and the average distance
def wmdist(title_list):
    print("Word Mover's Distance for Titles:")
    print("--------------------------------------------------------------------------------")
    distances = []
    for title in title_list:
        dist = model.wmdistance(given_title, title) #determining WM distance
        distances.append(dist)
        #distance = model.WmdSimilarity(given_title, title)

    sum_dist = 0
    for distance in distances:
        sum_dist = sum_dist + distance
        print ('distance = %.3f' % distance)
        print("--------------------------------------------------------------------------------")

    avg_dist = sum_dist/len(distances)
    print("Average Distance: {}".format(avg_dist))
    print("--------------------------------------------------------------------------------")
    return(avg_dist)

#---------------------#--------------------#---------------------#--------------------#
#Function to decide whether human verification is required
def human_ver(avg_dist):
    if(avg_dist >= 1.0):
        print("The title and image are flagged. Please use human verification!")
        print("--------------------------------------------------------------------------------")

    else:
        print("The title associated with this image seems to be right. Human verification is NOT required.")
        print("--------------------------------------------------------------------------------")

#---------------------#--------------------#---------------------#--------------------#
#Main function to call the rest of the above functions
def main():
    list_of_page_urls = []
    credible_from_url_list = []
    title_list = []
    list_of_page_urls = detect_web(image_path)
    credible_from_url_list = credible_list(list_of_page_urls)
    title_list = titles(credible_from_url_list)
    print_article_title(title_list)
    entity_analysis(title_list)
    avg_dist = wmdist(title_list)
    human_ver(avg_dist)

#---------------------#--------------------#---------------------#--------------------#

if __name__ == "__main__":
    main()
