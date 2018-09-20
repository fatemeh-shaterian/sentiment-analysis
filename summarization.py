# from https://code.luasoftware.com/tutorials/python/python-read-json-file-and-convert-to-csv/
# in console: pip install unicodecsv==0.14.1
# pip install requests
# https://www.geeksforgeeks.org/get-post-requests-using-python/

import json
import requests
import unicodecsv as csv
import urllib
import re



class JsonObj:
    def __init__(self, issueId, issue_number, url, user, like, dislike, laugh, hooray, confused, heart, body):
        self.issueId = issueId
        self.issue_number = issue_number
        self.url = url
        self.user = user
        self.like = like
        self.dislike = dislike
        self.laugh = laugh
        self.hooray = hooray
        self.confused = confused
        self.heart = heart
        self.body = body



#replace username and password field with valid username and password value
username = 'username'
password = 'password'
files = ['Automattic_wp-calypso_issues', 'dotnet_corefx_issues' , 'explosion_spaCy_issues' , 'facebook_create-react-app_issues' , 'FortAwesome_Font-Awesome_issues' , 'GoogleChrome_puppeteer_issues' , 'ionic-team_ionic_issues' , 'kubernetes_kubernetes_issues' , 'rails_rails_issues' , 'signalapp_Signal-Android_issues' , 'TryGhost_Ghost_issues' ,'zdotnet_coreclr_issues' , 'zmaterial-components_material-components-web_issues', 'zMicrosoft_vscode_issues', 'ztensorflow_tensorflow_issues', 'ztwbs_bootstrap_issues']
#files = [ 'GoogleChrome_puppeteer_issues' ]

############### A Function for Writing Output to Text File  #################
def writetotxtfile(input, output):
    try:
        my_input_file = open(input ,"r", encoding='utf-8')
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    if not my_input_file.closed:
        text_list = []
        for line in my_input_file.readlines():
            line = line.split(",", 20)
            text_list.append(" ".join(line))
        my_input_file.close()

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




##################### Main  ####################
def main ():
    with open(inputFile + '.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    summaryFile = './summary/'+ inputFile + '_sammary.json'
    summary_data = ''
    body = ''
    for row in data:
        issueId = row['id']
        issueNo = row['number']
        user = row['user']['login']
        url = row['url']
        body = row['body']

        bodystr = []
        str1 = " "
        #print (body)
        if (body is not None):
            #str(body)
            body2 = body.split("\r\n")
            for line in body2:
                #print (str1)
                #ips = [line.split("\n")[0]]
                str1 = str1 + str(line)
                #bodystr.extend(ips)
                #str1 = str1 + str(bodystr)
            body = str1 + " "
            str1 = " "
            body2 = body.split("\n")
            for line in body2:
                str1 = str1 + str(line)
        body = str1
        print (body)



        #print (bodystr)
        #body = str(bodystr).replace("['", " ")
        #ips = [line.split("\n")[0] for line in body.split("\r\n")]
        #print(ips)


        #from functools import partial
        #from operator import is_not
        #b1 = str(body)

        #b = b1.split("\n")
        #ips = [line.split("\n")[0] for line in b]
        #a = str(ips)
        #a.replace("\n", ' ')
        #print (a + '------')
        #body = a

        #urls = re.findall('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?\S', body)
        #for u in urls:
            #print (u)
            #body.replace(u , ' ')


        #b = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?\S', ' ', body)
        #print (b)
      #  body = re.sub(r'http:\\*/\\*/.*?\s', ' ', body)
       # body = re.sub(r'https:\\*/\\*/.*', ' ', body)
        #body = re.sub(r'http:\\*/\\*/.*', ' ', body)
        if 'reactions' not in row:
            continue
        like = row['reactions']['+1']
        dislike = row['reactions']['-1']
        laugh = row['reactions']['laugh']
        hooray = row['reactions']['hooray']
        confused = row['reactions']['confused']
        heart = row['reactions']['heart']
        row = [issueId, issueNo, url, user, like, dislike,laugh, hooray,confused,heart, body]

        if not (like is 0 and dislike is 0 and laugh is 0 and hooray is 0 and confused is 0 and heart is 0):
            if (True):#(like + dislike + laugh + hooray + confused + heart) >= 10 ) :
                jsonObj = JsonObj(issueId, issueNo, url, user, like, dislike,laugh, hooray,confused,heart, body)
                #s = json.dump(jsonObj)
                summary_data = summary_data + json.dumps(jsonObj.__dict__) + ','

    summary_data = summary_data[:-1]  #remove , from end of file

    try:
       my_output_file = open(summaryFile, "w", encoding='utf-8')
    except IOError as e:
       print("I/O error({0}): {1}".format(e.errno, e.strerror))

    if not my_output_file.closed:
          my_output_file.write('[' + summary_data + ']')
          print(inputFile +'_summary.json File was Successfully created.')
          my_output_file.close()


for inputFile in files :
    main()
