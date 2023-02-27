# import mysql.connector
import pandas as pd
import csv
from enum import Enum

# column names in the ranking dataframe
ranking_SJR = 'SJR'
ranking_SJR_quartile = 'SJR Best Quartile'
ranking_h_index = 'H index'
ranking_title = 'Title'
ranking_issn = 'Issn'

# keys in the ranking dictionary
dict_SJR = 'sjr'
dict_SJR_quartile = 'sjr_quartile'
dict_h_index = 'h_index'
dict_title = 'title'
dict_issn = 'issn'

# column names in the article dataframe
df_SJR = 'journal_scimago_score'
df_SJR_quartile = 'journal_scimago_quartile'
df_h_index = 'journal_scimago_hindex'
df_title = 'journal_title'
df_issn = 'journal_issn'

ranking_columns_to_dict = {
    ranking_SJR: dict_SJR,
    ranking_SJR_quartile: dict_SJR_quartile,
    ranking_h_index: dict_h_index,
    ranking_title: dict_title,
    ranking_issn: dict_issn,
}

class SJRYear(Enum):
    V_19 = 2019
    V_21 = 2021

    def get_filename(self):
        if self == SJRYear.V_19:
            return  './resources/scimagojr_2019.csv'
        elif self == SJRYear.V_21:
            return  './resources/scimagojr_2021.csv'
        
def null_check(x:any):
    if x == '' and x == ' ' and x == None:
        return 0
    
    return x

def null_check_columns(df:pd.DataFrame):
    df[ranking_SJR] = df[ranking_SJR].apply(null_check)
    df[ranking_SJR_quartile] = df[ranking_SJR_quartile].apply(lambda x: str(null_check(x)))
    df[ranking_h_index] = df[ranking_h_index].apply(null_check)
    df[ranking_title] = df[ranking_title].apply(lambda x: str(null_check(x)))

    return df

def expand_df_according_to_issn(df:pd.DataFrame):
    df[ranking_issn] = df[ranking_issn].str.split(', ')
    df = df.explode(ranking_issn)

    return df

def convert_rankings_to_dict(df:pd.DataFrame):
    df = df.rename(columns=ranking_columns_to_dict)

    return df.to_dict('list')

def get_SJR_rankings(ranking_filename:str):
    df = pd.read_csv(ranking_filename, sep=';')
    df = df[[ranking_SJR, ranking_SJR_quartile, ranking_h_index, ranking_title, ranking_issn]]
    df = null_check_columns(df)
    expanded_df = expand_df_according_to_issn(df)
    rankings_dict = convert_rankings_to_dict(expanded_df)

    return rankings_dict

def is_value_empty(x:str):
    if x == '0' or x == 'null' or x == '' or x == ' ' or x == None:
        return True
    
    return False

def null_check_title(article_journal_title:str, title_in_journal_data:str):
    if is_value_empty(article_journal_title):
        if title_in_journal_data != '0':
           return title_in_journal_data
        
    return article_journal_title

def rank_articles_journals(df:pd.DataFrame, journal_data:dict):
    updated_articles = {
        df_title: [],
        df_SJR: [],
        df_SJR_quartile: [],
        df_h_index: [],
    }
    for _, article in df.iterrows():
        issn = article[df_issn].replace('-', '').strip()
        if issn in journal_data[dict_issn]:
            issn_position = journal_data[dict_issn].index(issn)
            updated_articles[df_title].append(null_check_title(article[df_title], journal_data[dict_title][issn_position]))
            updated_articles[df_SJR].append(journal_data[dict_SJR][issn_position])
            updated_articles[df_SJR_quartile].append(journal_data[dict_SJR_quartile][issn_position])
            updated_articles[df_h_index].append(journal_data[dict_h_index][issn_position])
        
    pd.DataFrame(updated_articles).to_csv('./data/scimago_rank_data_2021_p3.csv', index=False)

def run(sjr_year:SJRYear):
    # does it make sense to only do this once and save the cleaned df?
    journal_data = get_SJR_rankings(sjr_year.get_filename())
    df = pd.read_csv('./data/scimago_rank_data.csv')

    rank_articles_journals(df, journal_data)

if __name__ == '__main__':
    # commented code for ADA 
    # start_time_all = time.time()

    # log_name = os.path.relpath(__file__, os.path.dirname(os.path.dirname(__file__)))
    # logger = get_ada_logger(log_name)
    # config = Config.get_instance()
    # logger.info(f"Start daily SJR Update..")

    run(SJRYear.V_21)
    # duration_all = "{:.2f}".format((time.time() - start_time_all)/60)

    # logger.info(config["global"]["logging"]["logging_messages"]["finish"])


    
# SCOPE QUERY
# "select article_uuid, journal_issn, journal_title from metadata where operation_type IN ( 'ADD', 'METAONLY', 'ONHOLD' ) and journal_scimago_hindex IS NULL and batch_gen='{}'".format(args.batch_generation)

# UPDATE QUERY
# "UPDATE metadata SET journal_title = %s, journal_scimago_score = %s, journal_scimago_hindex = %s, journal_scimago_quartile = %s WHERE article_uuid = %s "