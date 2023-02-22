#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv


filename = './resources/scimagojr_2021.csv'
data_filename = './data/scimago_rank_data.csv'

journal_data = {}
with open(filename, 'r') as my_file:
    reader = csv.reader(my_file, delimiter=';', quotechar='"')

    for idx, row in enumerate(reader):

        if idx == 0:
            scimago_issn_ind = row.index('Issn')
            scimago_score_ind = row.index('SJR')
            scimago_quartile_ind = row.index('SJR Best Quartile')
            scimago_hindex_ind = row.index('H index')
            scimago_jtitle_ind = row.index('Title')
            continue

        journal_score = row[scimago_score_ind].replace(',', '.')
        if journal_score != '' and journal_score != ' ' and journal_score != None:
            journal_score = float(journal_score)
        else:
            journal_score = 0

        journal_quartile = row[scimago_quartile_ind]
        journal_hindex = int(row[scimago_hindex_ind])
        journal_title = row[scimago_jtitle_ind]

        if journal_score == None or journal_score == '' or journal_score == ' ':
            journal_score = 0

        if journal_quartile == None or journal_quartile == '' or journal_quartile == ' ':
            journal_quartile = '0'

        if journal_hindex == None or journal_hindex == '' or journal_hindex == ' ':
            journal_hindex = 0

        if journal_title == None or journal_title == '' or journal_title == ' ':
            journal_title = '0'

        issns = row[scimago_issn_ind].split(', ')

        for issn in issns:
            issn = issn.strip()
            if issn not in journal_data:
                journal_data[issn] = [journal_score, journal_quartile, journal_hindex, journal_title]
            else:
                continue

print (len(journal_data))

hits = 0
total_counter = 0
with open('./data/scimango_rank_data_2021.csv', 'wb') as output:
    writerToOutput = csv.writer(output,
                               delimiter = ',')

    with open(data_filename, 'r') as my_file:
        reader = csv.reader(my_file, delimiter=',', quotechar='"')
    
        for idx, row in enumerate(reader):
            if idx == 0:
                writerToOutput.writerow([unicode(s).encode("utf-8") for s in row])
                continue
            
            total_counter += 1
            article_uuid = row[0]
            journal_issn = row[1]
            journal_title = row[2]

            edited_issn = journal_issn.replace('-', '').strip()
            print( edited_issn)

            if edited_issn in journal_data:
                hits += 1

                journal_score = journal_data[edited_issn][0]
                journal_quartile = journal_data[edited_issn][1]
                journal_hindex = journal_data[edited_issn][2]
                journal_scimago_title = journal_data[edited_issn][3]

                if journal_title == '0' or journal_title == 'null' or journal_title == '' or journal_title == ' ' or journal_title == None:
                    if journal_scimago_title != '0':
                        journal_title = journal_scimago_title

                journal_scimago_score = journal_score
                journal_scimago_hindex = journal_hindex
                journal_scimago_quartile = journal_quartile

                new_row = [article_uuid, journal_issn, journal_title, journal_scimago_score, journal_scimago_hindex, journal_scimago_quartile]
                writerToOutput.writerow([unicode(s).encode("utf-8") for s in new_row])

        

print(total_counter)
print (hits)

