import pandas as pd
import csv

def set_dataset():
    """
    目的変数: 
        y   10aあたり収穫量
    説明変数: 
        x1  年平均気温
        x2  年間の17度以下の日数
        x3  年間の30度以上の日数
        x4  7月~8月の平均気温
        x5  7月~8月の日平均気温が17度以下の日数
        x6  7月~8月の日平均気温が25度以上の日数
        x7  7月~8月の日最高気温が17度以下の日数
        x8  7月~8月の日最高気温が25度以上の日数
        x9  6月~9月の平均気温
        x10 6月~9月の日平均気温が17度以下の日数
        x11 6月~9月の日平均気温が25度以上の日数
        x12 年度（技術進歩を考慮）
        x13 都道府県
        x14 7月~8月の平均降水量
        x15 6月~9月の平均降水量
    """
    columns=['y', 'x1', 'x2', 'x3', 'x12']
    df = pd.DataFrame(columns=columns)
    df_future = pd.DataFrame(columns=columns)


    """
    Dataset(1):
        米の作付面積及び収穫量 
        政府統計名	作物統計調査	
        詳細
        提供統計名	作物統計調査	
        提供分類1	作況調査(水陸稲、麦類、豆類、かんしょ、飼料作物、工芸農作物)	
        提供分類2	長期累年	
        調査年月	2020年
        https://www.stat.go.jp/library/faq/faq07/faq07a05.html
        https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00500215&tstat=000001013427&cycle=0&year=20200&month=0&tclass1=000001032288&tclass2=000001034728&tclass3val=0
    
    Dataset(2):
        https://www.data.jma.go.jp/gmd/risk/obsdl/
    """
    d1_path = './data/d1/{}.xls'
    d2_path = './data/d2/{}.csv'
    d3_path = './data/d3/{}.csv'
    for e in ['toyama_f002c-001-001-027-000', 'akita_f002c-001-001-016-000', 'hukusima_f002c-001-001-018-000', 'nigata_f002c-001-001-026-000', 'yamagata_f002c-001-001-017-000', 'iwate_f002c-001-001-014-000', 'miyagi_f002c-001-001-015-000']:
        # 収穫量の前処理
        book = pd.ExcelFile(d1_path.format(e))
        sheet_name = book.sheet_names
        sheet_df = book.parse(sheet_name[0], skiprows=6, names = range(0,19))
        col_y = sheet_df[16].tolist() # 10aあたり収穫量
        col_x12 = [year[-5:-1] for year in sheet_df[0].tolist()] # year
        #print(sheet_df, col_x12, col_y)

        # 天気の前処理
        col_x1 = {}
        col_x4 = {}
        col_x9 = {}
        pref = e.split('_')[0]
        with open(d2_path.format(pref), encoding='cp932', newline='') as f:
            csvreader = csv.reader(f)
            for i, row in enumerate(csvreader):
                if i<5:
                    continue
                t = row[0].split('/')
                year = int(t[0])
                month = int(t[1])
                avg_tmp = float(row[1])

                # col_x1
                if year not in col_x1:
                    col_x1[year] = {'avg_tmp': avg_tmp, 'count': 1}
                else:
                    col_x1[year]['avg_tmp'] += avg_tmp
                    col_x1[year]['count'] += 1
                # col_x4
                if 7 <= month <= 8:
                    if year not in col_x4:
                        col_x4[year] = {'avg_tmp': avg_tmp, 'count': 1}
                    else:
                        col_x4[year]['avg_tmp'] += avg_tmp
                        col_x4[year]['count'] += 1
                # col_x9
                if 6 <= month <= 9:
                    if year not in col_x9:
                        col_x9[year] = {'avg_tmp': avg_tmp, 'count': 1}
                    else:
                        col_x9[year]['avg_tmp'] += avg_tmp
                        col_x9[year]['count'] += 1

        col_x1 = {k: round(col_x1[k]['avg_tmp']/col_x1[k]['count'],2) for k in col_x1}
        col_x4 = {k: round(col_x4[k]['avg_tmp']/col_x4[k]['count'],2) for k in col_x4}
        col_x9 = {k: round(col_x9[k]['avg_tmp']/col_x9[k]['count'],2) for k in col_x9}
        #print(col_x1, col_x4, col_x9)
        #exit()

        # 降水量の前処理
        col_x14 = {}
        col_x15 = {}
        col_x16 = {}
        pref = e.split('_')[0]
        with open(d3_path.format(pref), encoding='cp932', newline='') as f:
            csvreader = csv.reader(f)
            for i, row in enumerate(csvreader):
                if i<5:
                    continue
                t = row[0].split('/')
                year = int(t[0])
                month = int(t[1])
                wea = float(row[1])

                # col_x14
                if 7 <= month <= 8:
                    if year not in col_x14:
                        col_x14[year] = {'wea': wea, 'count': 1}
                    else:
                        col_x14[year]['wea'] += wea
                        col_x14[year]['count'] += 1
                # col_x15
                if 6 <= month <= 9:
                    if year not in col_x15:
                        col_x15[year] = {'wea': wea, 'count': 1}
                    else:
                        col_x15[year]['wea'] += wea
                        col_x15[year]['count'] += 1
                # col_x16
                if 4 <= month <= 11:
                    if year not in col_x16:
                        col_x16[year] = {'wea': wea, 'count': 1}
                    else:
                        col_x16[year]['wea'] += wea
                        col_x16[year]['count'] += 1 

        col_x14 = {k: round(col_x14[k]['wea']/col_x14[k]['count'],2) for k in col_x14}
        col_x15 = {k: round(col_x15[k]['wea']/col_x15[k]['count'],2) for k in col_x15}
        col_x16 = {k: round(col_x16[k]['wea']/col_x16[k]['count'],2) for k in col_x16}
        #print(col_x14, col_x15)

        for i in range(len(col_y)):
            #if not 2000 < int(col_x12[i]) < 2010:
            #    continue
            df = df.append({
                'y': col_y[i],
                'x1': col_x1[int(col_x12[i])],
                'x2': 100,
                'x3': 50,
                'x4': col_x4[int(col_x12[i])],
                'x9': col_x9[int(col_x12[i])],
                'x12': col_x12[i],
                'x14': col_x14[int(col_x12[i])],
                'x15': col_x15[int(col_x12[i])],
                'x16': col_x16[int(col_x12[i])]
            }, ignore_index=True)
        #print(df)

    for x16 in range(11):
        x16 = 50 + x16*25
        for x9 in range(13):
            x9 = 19 + x9/2
            for x12 in range(6):
                x12 = 2020+(x12*20)
                #x12 = 2010
                df_future = df_future.append({'x9': x9, 'x16': x16, 'x12': x12}, ignore_index=True)
    
    for i in columns:
        df[i] = pd.to_numeric(df[i])
        df_future[i] = pd.to_numeric(df_future[i])
    
    return df, df_future