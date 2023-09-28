# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 00:07:42 2020

@author: diego
"""
import pandas as pd


def read_and_process_data():
    '''

    Returns
    -------
    None.

    '''
    geomet = pd.read_stata("data/IfoGAME_balanced_panel.dta")
    econ_freedom = read_fraser_institute_data()
    ef_expanded = add_years(econ_freedom)
    ef_expanded = interpolate_fraser_data(ef_expanded)
    merged = geomet.merge(ef_expanded, how='left')
    merged.to_csv('data/econ_freedom_and_geomet.csv', index=False)
    return merged


def read_fraser_institute_data():
    '''

    Returns
    -------
    econ_freedom : TYPE
        DESCRIPTION.

    '''
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


def interpolate_fraser_data(df):
    '''
    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    df.sort_values(['iso', 'year'], ascending=[True, True], inplace=True)
    df = df.reset_index().drop(columns=['index'])
    df = df.groupby('iso').apply(lambda group: group.interpolate
                                 (limit_area='inside'))
    return df


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
        df = add_entries_for_country(df, iso, dct[iso])
    return df


def add_entries_for_country(df, iso_code, country_name):
    '''
    Adds years in between.

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    iso_code : TYPE
        DESCRIPTION.
    country_name : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''
    for i in range(1971, 2000):
        if i % 5 != 0:
            df = df.append({"year": i, "iso": iso_code, "country": country_name
                            }, ignore_index=True)
    return df
# Change made on 2024-06-26 18:27:17.991120
# Change made on 2024-06-26 18:27:20.431760
# Change made on 2024-06-26 18:27:22.130779
# Change made on 2024-06-26 18:27:23.749913
# Change made on 2024-06-26 18:27:25.427363
# Change made on 2024-06-26 18:27:27.112277
# Change made on 2024-06-26 18:27:28.954193
# Change made on 2024-06-26 18:27:30.692932
# Change made on 2024-06-26 18:27:32.508953
# Change made on 2024-06-26 18:27:34.519786
# Change made on 2024-06-26 18:27:36.345516
# Change made on 2024-06-26 18:27:38.114656
# Change made on 2024-06-26 18:27:39.867115
# Change made on 2024-06-26 18:27:41.572281
# Change made on 2024-06-26 18:27:43.272541
# Change made on 2024-06-26 18:27:44.933646
# Change made on 2024-06-26 18:27:46.706615
# Change made on 2024-06-26 18:27:48.417094
# Change made on 2024-06-26 18:27:50.307696
# Change made on 2024-06-26 18:27:52.149935
# Change made on 2024-06-26 18:27:53.840890
# Change made on 2024-06-26 18:27:56.437305
# Change made on 2024-06-26 18:27:58.322661
# Change made on 2024-06-26 18:28:00.029213
# Change made on 2024-06-26 18:28:01.737369
# Change made on 2024-06-26 18:28:03.619272
# Change made on 2024-06-26 18:28:05.457449
# Change made on 2024-06-26 18:28:07.108778
# Change made on 2024-06-26 18:28:08.762049
# Change made on 2024-06-26 18:28:10.480890
# Change made on 2024-06-26 18:28:12.170962
# Change made on 2024-06-26 18:28:14.033780
# Change made on 2024-06-26 18:28:15.825555
# Change made on 2024-06-26 18:28:17.650161
# Change made on 2024-06-26 18:28:19.552287
# Change made on 2024-06-26 18:28:21.211761
# Change made on 2024-06-26 18:28:23.245619
# Change made on 2024-06-26 18:28:24.978659
# Change made on 2024-06-26 18:28:26.693344
# Change made on 2024-06-26 18:28:28.427330
# Change made on 2024-06-26 18:28:30.259328
# Change made on 2024-06-26 18:28:32.045682
# Change made on 2024-06-26 18:28:33.832285
# Change made on 2024-06-26 18:28:35.554176
# Change made on 2024-06-26 18:28:37.190480
# Change made on 2024-06-26 18:28:38.931007
# Change made on 2024-06-26 18:28:40.734342
# Change made on 2024-06-26 18:28:42.506412
# Change made on 2024-06-26 18:28:44.408292
# Change made on 2024-06-26 18:28:46.025394
# Change made on 2024-06-26 18:28:47.864309
# Change made on 2024-06-26 18:28:49.548524
# Change made on 2024-06-26 18:28:51.235094
# Change made on 2024-06-26 18:28:52.927031
# Change made on 2024-06-26 18:28:54.606538
# Change made on 2024-06-26 18:28:56.255388
# Change made on 2024-06-26 18:28:57.857623
# Change made on 2024-06-26 18:28:59.716315
# Change made on 2024-06-26 18:29:01.396279
# Change made on 2024-06-26 18:29:03.145895
# Change made on 2024-06-26 18:29:04.928015
# Change made on 2024-06-26 18:29:06.589380
# Change made on 2024-06-26 18:29:08.364057
# Change made on 2024-06-26 18:29:10.037888
# Change made on 2024-06-26 18:29:11.734658
# Change made on 2024-06-26 18:29:13.487566
# Change made on 2024-06-26 18:29:15.260343
# Change made on 2024-06-26 18:29:16.958621
# Change made on 2024-06-26 18:29:18.615855
# Change made on 2024-06-26 18:29:20.245541
# Change made on 2024-06-26 18:29:21.931014
# Change made on 2024-06-26 18:29:23.650381
# Change made on 2024-06-26 18:29:25.302927
# Change made on 2024-06-26 18:29:26.978615
# Change made on 2024-06-26 18:29:28.667696
# Change made on 2024-06-26 18:29:30.342597
# Change made on 2024-06-26 18:29:32.165595
# Change made on 2024-06-26 18:29:33.793420
# Change made on 2024-06-26 18:29:35.496277
# Change made on 2024-06-26 18:29:37.110294
# Change made on 2024-06-26 18:29:38.812036
# Change made on 2024-06-26 18:29:40.651778
# Change made on 2024-06-26 18:29:42.387838
# Change made on 2024-06-26 18:29:45.667270
# Change made on 2024-06-26 18:29:47.615007
# Change made on 2024-06-26 18:29:49.285044
# Change made on 2024-06-26 18:29:50.975773
# Change made on 2024-06-26 18:29:52.632834
# Change made on 2024-06-26 18:29:54.391254
# Change made on 2024-06-26 18:29:56.160359
# Change made on 2024-06-26 18:29:57.852722
# Change made on 2024-06-26 18:29:59.694967
# Change made on 2024-06-26 18:30:01.413249
# Change made on 2024-06-26 18:30:03.333811
# Change made on 2024-06-26 18:30:05.172324
# Change made on 2024-06-26 18:30:07.066032
# Change made on 2024-06-26 18:30:08.921405
# Change made on 2024-06-26 18:30:10.598257
# Change made on 2024-06-26 18:30:12.307765
# Change made on 2024-06-26 18:30:14.236318
# Change made on 2024-06-26 18:30:16.014158
# Change made on 2024-06-26 18:30:17.986512
# Change made on 2024-06-26 18:30:19.964307
# Change made on 2024-06-26 18:30:21.622018
# Change made on 2024-06-26 18:30:23.416191
# Change made on 2024-06-26 18:30:25.121501
# Change made on 2024-06-26 18:30:26.904290
# Change made on 2024-06-26 18:30:28.610005
# Change made on 2024-06-26 18:30:30.362092
# Change made on 2024-06-26 18:30:32.000722
# Change made on 2024-06-26 18:30:33.770073
# Change made on 2024-06-26 18:30:35.465298
# Change made on 2024-06-26 18:30:37.167617
# Change made on 2024-06-26 18:30:38.973456
# Change made on 2024-06-26 18:30:40.721994
# Change made on 2024-06-26 18:30:42.573873
# Change made on 2024-06-26 18:30:45.200110
# Change made on 2024-06-26 18:30:46.868321
# Change made on 2024-06-26 18:30:48.508338
# Change made on 2024-06-26 18:30:50.199346
# Change made on 2024-06-26 18:30:51.966484
# Change made on 2024-06-26 18:30:53.630078
# Change made on 2024-06-26 18:30:55.341298
# Change made on 2024-06-26 18:30:57.068719
# Change made on 2024-06-26 18:30:58.807380
