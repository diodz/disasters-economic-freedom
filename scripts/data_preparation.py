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
# Change made on 2024-06-26 18:31:00.586945
# Change made on 2024-06-26 18:31:02.303066
# Change made on 2024-06-26 18:31:04.211211
# Change made on 2024-06-26 18:31:05.937571
# Change made on 2024-06-26 18:31:07.673415
# Change made on 2024-06-26 18:31:09.351099
# Change made on 2024-06-26 18:31:11.065562
# Change made on 2024-06-26 18:31:12.772670
# Change made on 2024-06-26 18:31:14.436787
# Change made on 2024-06-26 18:31:16.163605
# Change made on 2024-06-26 18:31:17.941145
# Change made on 2024-06-26 18:31:19.697324
# Change made on 2024-06-26 18:31:21.410999
# Change made on 2024-06-26 18:31:23.302588
# Change made on 2024-06-26 18:31:24.980251
# Change made on 2024-06-26 18:31:26.692290
# Change made on 2024-06-26 18:31:29.129331
# Change made on 2024-06-26 18:31:30.904302
# Change made on 2024-06-26 18:31:32.580280
# Change made on 2024-06-26 18:31:34.302586
# Change made on 2024-06-26 18:31:36.059373
# Change made on 2024-06-26 18:31:37.832199
# Change made on 2024-06-26 18:31:39.722556
# Change made on 2024-06-26 18:31:41.460286
# Change made on 2024-06-26 18:31:43.139032
# Change made on 2024-06-26 18:31:44.876349
# Change made on 2024-06-26 18:31:46.566458
# Change made on 2024-06-26 18:31:48.286667
# Change made on 2024-06-26 18:31:50.065234
# Change made on 2024-06-26 18:31:51.752278
# Change made on 2024-06-26 18:31:53.425516
# Change made on 2024-06-26 18:31:55.087289
# Change made on 2024-06-26 18:31:56.766918
# Change made on 2024-06-26 18:31:58.579197
# Change made on 2024-06-26 18:32:00.268441
# Change made on 2024-06-26 18:32:01.992294
# Change made on 2024-06-26 18:32:03.772522
# Change made on 2024-06-26 18:32:05.480270
# Change made on 2024-06-26 18:32:07.140939
# Change made on 2024-06-26 18:32:08.808969
# Change made on 2024-06-26 18:32:10.525928
# Change made on 2024-06-26 18:32:12.172995
# Change made on 2024-06-26 18:32:13.938342
# Change made on 2024-06-26 18:32:15.654784
# Change made on 2024-06-26 18:32:17.372328
# Change made on 2024-06-26 18:32:19.093700
# Change made on 2024-06-26 18:32:21.077093
# Change made on 2024-06-26 18:32:22.808989
# Change made on 2024-06-26 18:32:24.502432
# Change made on 2024-06-26 18:32:26.260305
# Change made on 2024-06-26 18:32:27.965024
# Change made on 2024-06-26 18:32:29.615083
# Change made on 2024-06-26 18:32:31.247030
# Change made on 2024-06-26 18:32:32.999483
# Change made on 2024-06-26 18:32:34.782629
# Change made on 2024-06-26 18:32:36.457700
# Change made on 2024-06-26 18:32:38.285157
# Change made on 2024-06-26 18:32:39.983518
# Change made on 2024-06-26 18:32:41.684292
# Change made on 2024-06-26 18:32:43.468579
# Change made on 2024-06-26 18:32:45.122761
# Change made on 2024-06-26 18:32:46.816711
# Change made on 2024-06-26 18:32:48.455228
# Change made on 2024-06-26 18:32:50.065775
# Change made on 2024-06-26 18:32:51.763648
# Change made on 2024-06-26 18:32:53.362682
# Change made on 2024-06-26 18:32:55.038542
# Change made on 2024-06-26 18:32:56.744856
# Change made on 2024-06-26 18:32:58.411553
# Change made on 2024-06-26 18:33:00.122927
# Change made on 2024-06-26 18:33:01.862554
# Change made on 2024-06-26 18:33:04.614353
# Change made on 2024-06-26 18:33:06.488817
# Change made on 2024-06-26 18:33:08.204305
# Change made on 2024-06-26 18:33:09.959335
# Change made on 2024-06-26 18:33:11.583639
# Change made on 2024-06-26 18:33:13.350390
# Change made on 2024-06-26 18:33:14.982172
# Change made on 2024-06-26 18:33:16.738299
# Change made on 2024-06-26 18:33:18.497766
# Change made on 2024-06-26 18:33:20.126590
# Change made on 2024-06-26 18:33:21.810338
# Change made on 2024-06-26 18:33:23.534890
# Change made on 2024-06-26 18:33:25.185158
# Change made on 2024-06-26 18:33:26.866007
# Change made on 2024-06-26 18:33:28.507530
# Change made on 2024-06-26 18:33:30.165197
# Change made on 2024-06-26 18:33:31.814327
# Change made on 2024-06-26 18:33:33.476351
# Change made on 2024-06-26 18:33:35.317482
# Change made on 2024-06-26 18:33:37.061942
# Change made on 2024-06-26 18:33:38.842025
# Change made on 2024-06-26 18:33:40.609591
# Change made on 2024-06-26 18:33:42.259402
# Change made on 2024-06-26 18:33:44.145975
# Change made on 2024-06-26 18:33:45.895325
# Change made on 2024-06-26 18:33:47.601864
# Change made on 2024-06-26 18:33:49.368332
# Change made on 2024-06-26 18:33:51.132817
# Change made on 2024-06-26 18:33:52.840584
# Change made on 2024-06-26 18:33:54.534216
# Change made on 2024-06-26 18:33:56.216248
# Change made on 2024-06-26 18:33:57.866685
# Change made on 2024-06-26 18:33:59.614695
# Change made on 2024-06-26 18:34:01.221451
# Change made on 2024-06-26 18:34:03.104222
# Change made on 2024-06-26 18:34:04.975373
# Change made on 2024-06-26 18:34:06.681358
# Change made on 2024-06-26 18:34:08.427215
# Change made on 2024-06-26 18:34:10.117937
# Change made on 2024-06-26 18:34:11.829912
# Change made on 2024-06-26 18:34:13.513697
# Change made on 2024-06-26 18:34:15.277256
# Change made on 2024-06-26 18:34:16.996665
# Change made on 2024-06-26 18:34:18.706012
# Change made on 2024-06-26 18:34:20.356649
# Change made on 2024-06-26 18:34:22.104256
# Change made on 2024-06-26 18:34:23.861773
# Change made on 2024-06-26 18:34:25.659881
