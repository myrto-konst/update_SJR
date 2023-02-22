# update_SJR
The script updateJournalImpactFactorData.py can be used to update the articles' journal ranking according to the SJR ranking. It has been verified for the 2019 and 2021 rankings, which you can find in the `./resources` folder.

## Running the updateJournalImpactFactorData.py script
In order to run this script, you need to specify 5 arguments:
* __batch generation__: This is the batch generation of the articles in the database that you wish to update. Use tag `-b`.
* __database name__: This is the database name you wish to connect to. Use tag `-d`.
* __database username__: This is the username for the database you wish to connect to. Use tag `-u`.
* __database password__: This is the password for the database you wish to connect to. Use tag `-p`.
* __resource file__: This is the resource file you wish to use to update your articles' journal ranking. Use tag `-r`.

Format of execution:
```
python updateJournalImpactFactorData.py -b <batch_gen> -d <db_name> -u <username> -p <password> -r <ranking_resource>
```
Example execution:
```
python updateJournalImpactFactorData.py -b 20220211 -d causaly_db -u username -p pswrd -r resources/scimagojr_2019.csv
```

The script will then fetch the articles of batch generation `<batch_gen>` and it will use the rankings in `<ranking_resource>` to rank each article's journal. The fields it will update accordingly are: `journal_title`,`journal_scimago_score`, `journal_scimago_hindex` and ` journal_scimago_quartile`.

## Running the updateJournalImpactFactorDataFORTESTING.py script
This script is for testing locally. 
It takes the data in `data/scimago_rank_data.csv` as an input and it currently outputs a file in  `data/scimago_rank_data_2021.csv` with the updated rankings according to the 2021 ranking created by Scimago. If you with to test a different ranking, add the ranking in the resources folder, change the `filename` variable to point to it, and lastly change the output folder on line 59 to the year of the ranking you are testing.