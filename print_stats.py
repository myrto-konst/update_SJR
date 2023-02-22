import pandas as pd
pd.set_option("display.max_columns", None)

rankings_2019 = pd.read_csv('./resources/scimagojr_2019.csv', sep=';')
rankings_2021 = pd.read_csv('./resources/scimagojr_2021.csv', sep=';')

rankings = {'2019': rankings_2019, '2021':rankings_2021}

def count_nulls(s):
    return (s.values == '-').sum()

basic_stats = {}
for year, df in rankings.items():
    basic_stats[year] = {
        'number_of_rows': df.shape[0],
        'number_of_unique_ISSNs':df['Issn'].nunique(),
        'number_of_unique_titles': df['Title'].nunique(),
        'number_of_unique_source_id': df['Sourceid'].nunique(),
        'null_ISSNs': count_nulls(df['Issn']),
        'null_titles': count_nulls(df['Title'])
    }

# print(basic_stats)

issns_in_2019_not_2021 = pd.Series(rankings_2019['Issn'].isin(rankings_2021['Issn']).values.astype(int), rankings_2019['Issn'].values)
# print(issns_in_2019_not_2021.loc[lambda x : x!=0])

for issn, value in issns_in_2019_not_2021.loc[lambda x : x!=0].iteritems():
    print(issn)
    row = rankings_2019.loc[rankings_2019['Issn'] == issn]
    if (row['SJR Best Quartile'] != '-').any():
        print('---------------------------------------------')
        print(row)
        print(rankings_2021.loc[rankings_2021['Issn'] == issn])
        print('---------------------------------------------')