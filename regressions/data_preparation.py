# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 00:07:42 2020

@author: diego
"""
import pandas as pd


def read_fraser_institute_data():
    econ_freedom = pd.read_excel(
        "data/efw-2019-master-index-data-for-researchers.xlsx",
        sheet_name="EFW Panel Data 2019 Report",
        skiprows=2).drop(columns=['Unnamed: 0'])
    econ_freedom.rename(columns={"ISO_Code": "iso", "Year": "year",
                                 "1  Size of Government": "size_gov",
                                 "2  Legal System & Property Rights":
                                     "prop_rights",
                                 "3  Sound Money": "sound_money",
                                 "4  Freedom to trade internationally":
                                     "freedom_to_trade",
                                 "5  Regulation": "regulation",
                                 "Countries": "country"}, inplace=True)
    return econ_freedom

#%%

GeoMet = pd.read_stata("data/IfoGAME_balanced_panel.dta")
econ_freedom = read_fraser_institute_data()

df = add_years(econ_freedom)

merged = GeoMet.merge(econ_freedom, how='left')

#%%
def add_years(df):
    '''


    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''
    dct = {}
    df_aux = df[df['year'] == 1970]
    for row in df_aux.itertuples(index=False):
        dct[row[1]] = row[2]
    for iso in df['iso'].unique():
        df = df.append({"year": 1979, "iso": iso, "country": dct[iso]},
                       ignore_index=True)
        df = df.append({"year": 1978, "iso": iso, "country": dct[iso]},
                       ignore_index=True)
        df = df.append({"year": 1977, "iso": iso, "country": dct[iso]},
                       ignore_index=True)
        df = df.append({"year": 1976, "iso": iso, "country": dct[iso]},
                       ignore_index=True)
    return df

#%%
def fill_country_names(df):
    '''


    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    dct = {}
    df_aux = df[df['year' == 1970]]
    for row in df_aux.itertuples(index=False):
        dct[row[1]] = row[2]
    for iso in df['iso'].unique():

