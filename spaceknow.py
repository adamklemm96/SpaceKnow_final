import os
import json
import pandas as pd
from spaceknow import request_api
from spaceknow import workdir


def create_list(sep, data):
    data = [x.split(sep) for x in data]

    return data


def procces_json(italyZinc):
    """
    italyZinc is in json input data needs to be separated
    output:
    returns a list 
    """
    italyZinc = json.loads(italyZinc)

    time_dic = italyZinc['dimension']['time']['category']['index']
    values_dic = italyZinc['value']

    # Switch values_dic in time dic key <> value
    time_dic = {y: x for x, y in time_dic.items()}
    # Convert index to int
    values_dic = {int(x): y for x, y in values_dic.items()}

    # Join two dictionaries based on a key value
    italyZinc_dict = {}
    for key in (time_dic.keys() | values_dic.keys()):
        if key in time_dic:
            italyZinc_dict.setdefault(key, []).append(time_dic[key])
        if key in values_dic:
            italyZinc_dict.setdefault(key, []).append(values_dic[key])

    return italyZinc_dict.values()


def finalize(df, area, dataset_name):
    """ 
    This func set date as an index and sorts its values
    Add additional columns to make it clear where data comes from
    """

    # Add headers
    header = ['Date', 'OBS_Value']
    df.columns = header

    # Convert str(Date) to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Set date as index and sort descending
    df = df.set_index('Date').sort_index(ascending=False)

    # Add columns
    df.insert(0, 'Area', area)
    df.insert(1, 'DataSeries', dataset_name)

    return df


def italyRetail(path):
    italyRetail = request_api.get_italyRetail()
    italyRetail = create_list(',', italyRetail)
    italyRetail_df = pd.DataFrame(italyRetail[1:])[[8, 9]].dropna()
    italyRetail_df = finalize(italyRetail_df, 'IT', 'Retail_Trade')

    return italyRetail_df


def germanyRetail(path):
    germanyRetail = request_api.get_germanyRetail()
    germanyRetail = create_list(';', germanyRetail)
    germanyRetail_df = pd.DataFrame(germanyRetail[2:])[[0, 5]].dropna()
    # Trim 01/ as it later behaves as a month and not a day in finalize()
    germanyRetail_df[0] = germanyRetail_df[0].str.replace(
        '^01/', '', regex=True)
    germanyRetail_df[5] = germanyRetail_df[5].str.replace(',', '.')
    germanyRetail_df[5] = germanyRetail_df[5].astype(float)
    germanyRetail_df = finalize(germanyRetail_df, 'GE', 'Retail_Trade')

    return germanyRetail_df


def italyZinc(path):
    italyZinc = request_api.get_italyZinc()
    italyZinc = procces_json(italyZinc)
    italyZinc_df = pd.DataFrame(italyZinc).dropna()
    italyZinc_df[0] = italyZinc_df[0].str.replace('M', '-')
    italyZinc_df = finalize(italyZinc_df, 'IT', 'Lead_zinc_tin_prod')

    return italyZinc_df


# output
path = workdir.create_directory()

# Create dataframe
italyZinc_df, italyRetail_df, germanyRetail_df = italyZinc(
    path), italyRetail(path), germanyRetail(path)

italyZinc_df.to_csv(f'{path}/ItalyZinc.csv')
italyRetail_df.to_csv(f'{path}/ItalyRetail.csv')
germanyRetail_df.to_csv(f'{path}/GermanyRetail.csv')
