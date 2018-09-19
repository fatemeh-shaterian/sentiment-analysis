# this file take output of senti and give the result of comparison tools output and reactions
#this program also use process folder as input
import glob, os
import csv
import unicodecsv as csv
import re
import string


###################### function definition ############################
def writetotxtfile(input, output):
    try:
        my_input_file = open(input ,"r", encoding='utf-8')
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    if not my_input_file.closed:
        text_list = []
        for line in my_input_file.readlines():
            line = line.split(",", 20)
            text_list.append(line)
        my_input_file.close()

    try:
        my_output_file = open(output, "w", encoding='utf-8')
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    if not my_output_file.closed:
        for line in text_list:
            my_output_file.write(line)
        print(output + ' File Successfully written.')
        my_output_file.close()
##################### End Function  #######################

def main(i):
    print('in main')
    global files
    try:
        my_input_file = open(inputName ,"r", encoding='utf-8')
        my_input_file_reaction = open('../../process/' + files[i-1]+'.txt' ,"r", encoding='utf-8')
        print(files[i-1])
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    conflictNum = 0
    plusNum = 0
    negNum = 0
    khonsaNum = 0
    global totalConflict
    global totalPlus
    global totalKhonsa
    global totalNeg
    global writer1
    global writer2


    if not my_input_file.closed:
        text_list = []
        text_list2 = []
        rr = ''
        index = 0
        reaction_lines = my_input_file_reaction.readlines()
        print(i)
        for line in (my_input_file.readlines()):
            print(reaction_lines[index])
            print(index)
            print(i)
            print(files[i - 1])
            line = line.split()
            reaction_lines[index] = reaction_lines[index].split()
            print(reaction_lines[index])
            print(line)
            issueid = int((reaction_lines[index])[0])
            like = int((reaction_lines[index])[4])
            dislike = int((reaction_lines[index])[5])
            laugh = int((reaction_lines[index])[6])
            hooray = int((reaction_lines[index])[7])
            confused = int((reaction_lines[index])[8])
            heart = int((reaction_lines[index])[9])
            pos = int(line[-2])
            neg = int(line[-1])
            #print(issueid, like, dislike, laugh, hooray, confused, heart, pos, neg)

            #like = 1
            #horry = happy = 2
            #heart = 3
            #confused = -2
            #dislike = -3
            reaction_pos = (like * 1) + (laugh * 2) + (hooray * 2) + (heart * 3)
            reaction_neg = (dislike * 3) + (confused * 2)

            #reaction_pos = (like * 1) + (laugh * 1) + (hooray * 1) + (heart * 1)
            #reaction_neg = (dislike * 1) + (confused * 1)

            res = ""
            if (abs(neg) > pos and reaction_neg < reaction_pos):  # polarity -
                res = "Conflict"
                conflictNum +=1
                totalConflict += 1
            if (abs(neg) < pos and reaction_neg > reaction_pos):  # polarity +
                res = "Conflict"
                conflictNum += 1
                totalConflict += 1
            if (abs(neg) > pos and reaction_neg > reaction_pos):  # polarity -
                res = "-"
                negNum += 1
                totalNeg += 1
            if (abs(neg) < pos and reaction_neg < reaction_pos):  # polarity -
                res = "+"
                plusNum += 1
                totalPlus += 1
            if res == "":
                khonsaNum += 1
                totalKhonsa +=1
            #print(issueid , like, dislike, laugh, hooray, confused, heart, pos, neg, ' ---> ' + res)
            ln = str(issueid) + '\t' + res + '\n'
            rr = rr + ln

            text_list.append([issueid, res])
            text_list2.append([issueid, pos, neg, reaction_pos , reaction_neg ,(reaction_pos-reaction_neg)])
            #print (text_list)
            #print (rr)
            #text_list.append(" ".join(l))
            index +=1


        my_input_file.close()

        for line in text_list:
            writer1.writerow(line)

        for line in text_list2:
            writer2.writerow(line)

    print(output + ' File Successfully written.')
    print( 'conflict: ' + str(conflictNum))
    print( '+ : ' + str(plusNum))
    print( '- : ' + str(negNum))
    print( 'khonsa: ' + str(khonsaNum) )

    if not my_output_file.closed:
        my_output_file.write(inputName + ' results: ' + '\n')
        my_output_file.write('conflict: ' + str(conflictNum) + '\n')
        my_output_file.write('+ : ' + str(plusNum) + '\n')
        my_output_file.write('- : ' + str(negNum) + '\n')
        my_output_file.write('khonsa: ' + str(khonsaNum) + '\n')

### End of main function

print( ' start form here ...  ' )
totalConflict = 0
totalPlus = 0
totalNeg = 0
totalKhonsa = 0
fileName = './result/summary_result_v1.txt'

files = ['Automattic_wp-calypso_issues_sammary.process', 'dotnet_corefx_issues_sammary.process' , 'explosion_spaCy_issues_sammary.process' , 'facebook_create-react-app_issues_sammary.process' , 'FortAwesome_Font-Awesome_issues_sammary.process' , 'GoogleChrome_puppeteer_issues_sammary.process' , 'ionic-team_ionic_issues_sammary.process' , 'kubernetes_kubernetes_issues_sammary.process' , 'rails_rails_issues_sammary.process' , 'signalapp_Signal-Android_issues_sammary.process' , 'TryGhost_Ghost_issues_sammary.process' , 'zdotnet_coreclr_issues_sammary.process' , 'zmaterial-components_material-components-web_issues_sammary.process', 'zMicrosoft_vscode_issues_sammary.process', 'ztensorflow_tensorflow_issues_sammary.process', 'ztwbs_bootstrap_issues_sammary.process']

try:
    my_output_file = open(fileName, "w", encoding='utf-8')
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))


with open('./result/alloutput2' + '.csv', 'wb') as csv_file:
    writer2 = csv.writer(csv_file, delimiter=",", encoding="utf8")
    writer2.writerow(['issueId', 'pos', 'neg' , 'reaction_pos' , 'reaction_neg', 'reaction'])
    with open('./result/alloutput1' + '.csv', 'wb') as csv_file:
        writer1 = csv.writer(csv_file, delimiter=",", encoding="utf8")
        writer1.writerow(['issueId', 'result'])
        # you can chose end of range 12 or 17
        for i in range(1,17):
            output = './result/output'+ str(i)
            inputName = './senti/'+ str(i) + '.txt'
            print(inputName)
            main(i)

print('Total results: ')
print( 'conflict: ' + str(totalConflict))
print( '+ : ' + str(totalPlus))
print( '- : ' + str(totalNeg))
print( 'khonsa: ' + str(totalKhonsa) )
print ( '% = ' + str(totalConflict/(totalNeg+totalPlus+totalConflict)))

if not my_output_file.closed:
    my_output_file.write('#################################################\n')
    my_output_file.write('Total results: \n')
    my_output_file.write('conflict: ' + str(totalConflict) + '\n')
    my_output_file.write('+ : ' + str(totalPlus) + '\n')
    my_output_file.write('- : ' + str(totalNeg) + '\n')
    my_output_file.write('khonsa: ' + str(totalKhonsa) + '\n')
    my_output_file.close()





