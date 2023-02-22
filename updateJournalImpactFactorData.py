#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
import csv

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-b", "--batch-generation",
                    required = True,
                    help = "The batch generation from which this data came.")
# DB credentials
parser.add_argument("-u", "--user",
                    required = True,
                    help = "The username for the DB we're trying to connect to.")
parser.add_argument("-p", "--password",
                    required = True,
                    help = "The password for the DB we're trying to connect to.")
parser.add_argument("-d", "--database",
                    required = True,
                    help = "The name of the database we're trying to connect to.")

parser.add_argument("-r", "--resource-file",
                    required = True,
                    help = "The ranking resource filename we're going to use to rank the articles' journals.")


args = parser.parse_args()

dbconn = mysql.connector.connect(user=args.user, password=args.password, database=args.database)
cursor = dbconn.cursor(buffered=True)
cursor_2 = dbconn.cursor(buffered=True)

journal_data = {}
with open(args.resource_file, 'r') as my_file:
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

print len(journal_data)

cursor.execute("select article_uuid, journal_issn, journal_title from metadata where operation_type IN ( 'ADD', 'METAONLY', 'ONHOLD' ) and journal_scimago_hindex IS NULL and batch_gen='{}'".format(args.batch_generation))
print 'MySQL Scoping query complete'

hits = 0
total_counter = 0
for output in cursor:
    total_counter += 1
    article_uuid = output[0]
    journal_issn = output[1]
    journal_title = output[2]

    edited_issn = journal_issn.replace('-', '').strip()
    print edited_issn

    if edited_issn in journal_data:
        hits += 1

        journal_score = journal_data[edited_issn][0]
        journal_quartile = journal_data[edited_issn][1]
        journal_hindex = journal_data[edited_issn][2]
        journal_scimago_title = journal_data[edited_issn][3]

        if journal_title == '0' or journal_title == 'null' or journal_title == '' or journal_title == ' ' or journal_title == None:
            if journal_scimago_title != '0':
                journal_title = journal_scimago_title

        insert_text = (
            "UPDATE metadata SET journal_title = %s, journal_scimago_score = %s, journal_scimago_hindex = %s, journal_scimago_quartile = %s WHERE article_uuid = %s "
        )
        cursor_2.execute(insert_text, (journal_title, journal_score, journal_hindex, journal_quartile, article_uuid))

        if not total_counter % 25000:
            print journal_title, journal_score, journal_hindex, journal_quartile, article_uuid

        if not hits % 1000000:
            print 'COMITTING: ', total_counter
            dbconn.commit()


print total_counter
print hits
print 'COMMITTING FINAL'
dbconn.commit()
dbconn.close()
