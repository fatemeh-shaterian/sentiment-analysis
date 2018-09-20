import glob, os
import csv
import unicodecsv as csv
import requests

class Issue:
    def __init__(self, issueId, senti_pos, senti_neg, reaction_pos, reaction_neg, like, dislike, laugh, hooray, confused, heart ):
        self.issueId = issueId
        self.senti_pos = senti_pos
        self.senti_neg = senti_neg
        self.like = like
        self.dislike = dislike
        self.laugh = laugh
        self.hooray = hooray
        self.confused = confused
        self.heart = heart
        self.reaction_pos = reaction_pos
        self.reaction_neg = reaction_neg

class User:
    def __init__(self, userid, issues):
        self.userid = userid
        #self.issues = [Issue]
        self.issues = []
    def addIssue(self, issue):
        self.issues.append(issue)


dirpath = "./senti-se-out"
os.chdir(dirpath)
#replace username and password field with valid username and password value
username = 'username'
password = 'pass'


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

#issues_list = []
all_users = []

for filename in glob.glob("*.txt"):
    print (filename + ' open')
    try:
        my_input_file = open(filename, "r", encoding='utf-8')
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    if not my_input_file.closed:
        text_list = []
        for line in my_input_file.readlines():
            line = line.split()
            userid = line[3]
            #print (userid)
            issueid = line[0]
            like = int(line[4])
            dislike = int(line[5])
            laugh = int(line[6])
            hooray = int(line[7])
            confused = int(line[8])
            heart = int(line[9])
            senti_pos = int(line[-2])
            senti_neg = int(line[-1])

            reaction_pos = like + laugh + hooray + heart
            reaction_neg = dislike + confused

            #issues_list.append(issueid, senti_pos, senti_neg, like, dislike, laugh, hooray, confused, heart, reaction_pos, reaction_neg)
            issue = Issue(issueid, senti_pos, senti_neg, reaction_pos, reaction_neg, like, dislike, laugh, hooray, confused, heart)
            index = 0
            for u in all_users:
                index += 1
                if (userid == u.userid):
                    u.addIssue(issue)
                    index = -1
                    break
            if (index == len(all_users)): #users not in all_users till now
                new_user = User(userid, [])
                new_user.addIssue(issue)
                i = new_user.issues[0]
                s = str(i.like)
                all_users.append((new_user))

        my_input_file.close()
        print(filename + ' close')

output1 = './out/AllUsers-issues'
output2 = './out/AllUsers-Polarity-Followers'
#output3 = './out/AllUsers-followers.csv'

with open(output1 + '.csv', 'wb') as csv_file1: # output1: All Users-All Isuues
    with open(output2 + '.csv', 'wb') as csv_file2:  # output2: All Users-Polarity
        writer1 = csv.writer(csv_file1, delimiter=",", encoding="utf8")
        writer1.writerow(['user', 'isslist'])

        writer2 = csv.writer(csv_file2, delimiter=",", encoding="utf8")
        writer2.writerow(['user', 'polarity' , 'follower_count'])


#        with open(output3, 'wb') as csv_file3:  # output3: All Users-Followers Count
#            writer3 = csv.writer(csv_file3, encoding='utf-8')
#           writer3.writerow(['user', 'followers_count'])

        i = 1
        for user in all_users:
            lst = []
            issuesid = ''

            total_pos = 0
            total_neg = 0

            for iss in user.issues:
                issuesid = issuesid + iss.issueId + ',' + str(iss.senti_pos) + ',' + str(iss.senti_neg) + ',' + str(iss.reaction_pos) + ',' + str(iss.reaction_neg) + ',' + str(iss.like) + ',' + str(iss.dislike) + ',' + str(iss.laugh) + ',' + str(iss.hooray) + ',' + str(iss.confused) + ',' + str(iss.heart) + '-' #for 1

                pos_bias = neg_bias = 0
                reaction_pos = iss.reaction_pos
                reaction_neg = iss.reaction_neg

                if (1 <= reaction_pos <=20):
                    pos_bias = 1
                if (21 <= reaction_pos <= 40):
                    pos_bias = 2
                if (41 <= reaction_pos <= 60):
                    pos_bias = 3
                if (61 <= reaction_pos <= 80):
                    pos_bias = 4
                if (81 <= reaction_pos):
                    pos_bias = 5

                if (1 <= reaction_neg <=20):
                    neg_bias = -1
                if (21 <= reaction_neg <= 40):
                    neg_bias = -2
                if (41 <= reaction_neg <= 60):
                    neg_bias = -3
                if (61 <= reaction_neg <= 80):
                    neg_bias = -4
                if (81 <= reaction_neg):
                    neg_bias = -5

                total_pos = total_pos + pos_bias + iss.senti_pos
                total_neg = total_neg + iss.senti_neg + neg_bias
                total = total_pos + total_neg

            ##################### Users and Followers  ####################
            follower_count = 0
            u = user.userid
            followers_url = "https://api.github.com/users/" + u

            r = requests.get(url=followers_url, auth=(username, password))

            followers_row = r.json()
            if 'message' in followers_row.keys():
                print ('error')
            else:
                follower_count = followers_row['followers']

                lst = [user.userid, issuesid]
                writer1.writerow(lst)

                lst2 = [user.userid, total, follower_count]
                writer2.writerow(lst2)
            print (str(i))
            #print(str(i) + ': ' + user.userid + ' followers: ' + str(follower_count))


            i += 1


    print(output2 +' File was Successfully created.')
print(output1 +' File was Successfully created.')


