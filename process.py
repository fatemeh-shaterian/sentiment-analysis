# from https://code.luasoftware.com/tutorials/python/python-read-json-file-and-convert-to-csv/
# in console: pip install unicodecsv==0.14.1
# pip install requests
# https://www.geeksforgeeks.org/get-post-requests-using-python/

import json
import requests
import unicodecsv as csv
import urllib
import re
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#from wordcloud import WordCloud
#from textblob import TextBlob
#import HTMLParser
from string import punctuation
#HTML_parser = HTMLParser.HTMLParser()
import itertools
#filename = 'TryGhost_Ghost_issues_sammary'

username = 'zkasiri'
password = 'zhr15489'
files = [ 'zdotnet_coreclr_issues_sammary', 'zmaterial-components_material-components-web_issues_sammary', 'zMicrosoft_vscode_issues_sammary', 'ztensorflow_tensorflow_issues_sammary', 'ztwbs_bootstrap_issues_sammary']
#files = ['Automattic_wp-calypso_issues_sammary', 'dotnet_corefx_issues_sammary' , 'explosion_spaCy_issues_sammary' , 'facebook_create-react-app_issues_sammary' , 'FortAwesome_Font-Awesome_issues_sammary' , 'GoogleChrome_puppeteer_issues_sammary' , 'ionic-team_ionic_issues_sammary' , 'kubernetes_kubernetes_issues_sammary' , 'rails_rails_issues_sammary' , 'signalapp_Signal-Android_issues_sammary' , 'TryGhost_Ghost_issues_sammary', 'zdotnet_coreclr_issues_sammary' , 'zmaterial-components_material-components-web_issues_sammary', 'zMicrosoft_vscode_issues_sammary', 'ztensorflow_tensorflow_issues_sammary', 'ztwbs_bootstrap_issues_sammary']
#files = [ 'GoogleChrome_puppeteer_issues_sammary']
############### A Function for Writing Output to Text File  #################
def writetotxtfile(input, output):
    try:
        my_input_file = open(input ,"r", encoding='utf-8')
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    if not my_input_file.closed:
        text_list = []
        ind = 0
        for line in my_input_file.readlines():
            ind += 1
            line = line.split(",", 20)
            text_list.append(" ".join(line))
        my_input_file.close()
        print(ind)

    try:
        my_output_file = open(output, "w", encoding='utf-8')
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    if not my_output_file.closed:
        for line in text_list:
            my_output_file.write("  " + line)
        print(output + ' File Successfully written.')
        my_output_file.close()
##################### End Function  #######################

def remove_num(text):
    text = ''.join([i for i in text if not i.isdigit()])
    return text

#def removeHTML(text):
    #return HTML_parser.unescape(text)

def remove_punct(text):
    text = ' '.join(word.strip(punctuation) for word in text.split() if word.strip(punctuation))
    return text

def remove_extra_space(text):
    word_list = text.split()
    text = ' '.join(word_list)
    return text

def decode(text):
    text = text.encode('ascii','ignore')
    return text

def remove_iter(text):
    text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
    return text

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def main():
    with open(inputFile,encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    ##################### Issues and Reactions  ####################
    ReactionsOutCSV = './process/' + filename + '.process.csv'
    current_users = []
    with open(ReactionsOutCSV, 'wb') as csv_file:
        writer = csv.writer(csv_file, encoding="utf8")
        writer.writerow(['issueId', 'issue_number', 'url', 'user', 'like', 'dislike','laugh','hooray','confused','heart','body'])
        ind2 = 1
        for row in data:
            issueId = row['issueId']
            issueNo = row['issue_number']
            user = row['user']
            if user not in current_users:
                current_users.append (user)

            url = row['url']
            body = row['body']
            body = re.sub(r'https:\\*/\\*/.*?\s', ' ', body)
            body = re.sub(r'http:\\*/\\*/.*?\s', ' ', body)
            body = re.sub(r'https:\\*/\\*/.*', ' ', body)
            body = re.sub(r'http:\\*/\\*/.*', ' ', body)
            body = re.sub(r'^https?:\/\/.*[\r\n]*', '', body, flags=re.MULTILINE)
            #body = re.sub(r'^#?', '', body, flags=re.MULTILINE)
            body = remove_num(body)
            #body = removeHTML(body)
            body = remove_punct(body)
            body = re.sub('[\[\]`]', ' ', body)
            # remove html and other kind of tags
            body = strip_tags(body)
            cleaner = re.compile('\*\*')
            body = re.sub(cleaner,' ', body)
            #body = re.sub('^<*>', ' ', body)
            #body = re.sub('^ *\/* ', ' ', body)

            body = remove_extra_space(body)
            body = re.sub('[\"\']', '', body)
            body = decode (body)
            body = body.decode ('UTF-8')
            # remove enter
            body = body.rstrip()
            body = body.lower()
            #body = re.sub('[\"\']', ' ', body)
            #body = re.sub('[\'\"]', ' ', body)
            body = remove_extra_space(body)
            #body = remove_iter(body)

            like = row['like']
            dislike = row['dislike']
            laugh = row['laugh']
            hooray = row['hooray']
            confused = row['confused']
            heart = row['heart']
            if (body != '' and body != ' '):
                row = [issueId, issueNo, url, user, like, dislike, laugh, hooray, confused, heart, body]
                writer.writerow(row)
                print(row)
                ind2 +=1

        print(ind2)
        #print (summary_data)

    print(ReactionsOutCSV + ' File Successfully written.')
    print(ReactionsOutCSV)
    print( './process/' + filename + '.process.txt')
    writetotxtfile(ReactionsOutCSV, './process/' + filename + '.process.txt')

for filename in files :
    inputFile = './summary/' + filename + '.json'
    main()