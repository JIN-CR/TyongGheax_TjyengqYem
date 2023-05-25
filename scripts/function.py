import json
import re
import pandas as pd
# import os, sqlite3 # 已不再使用

def read_rules(path):
    """
    讀取 json 格式的修訂規則文件。(需要 json 庫。)
    """
    # import json
    with open(path, 'r', encoding='utf-8') as f:
        rules = json.loads(f.read())
    return rules

def adding(matched): 
    return str(
        '\n\n' + matched.group()[0] + " " + matched.group()[1:] + '\n'
    )

def formated_qieyun_text(path="./resource/raw/qieyun@0.13.4/qieyun@0.13.4.txt"):
    """
    讀取原始《切韻》數據。(需要 re 庫。)
    """
    with open(path, 'r', encoding='utf-8') as f:
        qieyun_text = f.read()
    # import re
    qieyun_text = re.sub("\|", "\n", qieyun_text)#;print(text)
    qieyun_text = re.sub(r'[a-z A-z 0-9]{3}[^a-z^A-z^0-9]{2}', adding, qieyun_text) # 劃分聲母、韻部
    return qieyun_text

def revise_qieyun(text, rules, path="./resource/coproducts/KuangxYonh.txt"):
    """
    依據修訂規則文件，格式化原始《切韻》數據。(需要 re 庫。)

    將格式化後的文件保存在指定路徑下。
    """
    # 無視重紐
    for symbol in rules["replace"]["DryungNriux"]["symbols"]: 
        for original, replace in rules["replace"]["DryungNriux"]["values"].items():
            text = re.sub(symbol+original, symbol+replace, text)
    # 眞(B)軫質合錯歸入諄準稕
    for original, replace in rules["replace"]["diffYonh"]["values"].items():
        text = re.sub(original, replace, text)
    # 文字及開合錯誤
    for original, replace in rules["replace"]["mistakes"]["values"].items():
        text = re.sub(original, replace, text)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("格式化的《廣韻》 txt 文件已創建。\n")

def create_sjengmux_json(rules, Alphabet_rules, path=None):
    """
    生成 "符號: {聲母:[音標, 音標拼音]} "格式的 json 數據。

    將 json 格式的數據保存在指定路徑下，默認不保存。
    """
    # 聲(母)，多 "知徹澄孃 "、 "云 "
    # 云, 以
    SJENGMUX = rules["SJENGMUX"]
    sjeng_info = rules["sjeng_info"]
    # print([k for k, v in sjeng.items()] == sjeng_list)
    sjeng_info_list = [{k: [v, Alphabet_rules[v]]} for k, v in sjeng_info.items()]
    sjeng = dict(zip(SJENGMUX, sjeng_info_list))
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(sjeng, indent=4, separators=(',', ': '), ensure_ascii=False))
        # print("聲母 json 文件已創建（可選）。")
        print("聲母 json 文件已創建。\n")
    return sjeng

def read_YonhMiuk(path='./resource/coproducts/Yonh_table.csv'):
    """
    讀取韻目表。(需要 re, pandas 庫。)

    在指定路徑下，創建并保存等待進一步處理的初始韻目設定表，并進行預處理。
    """
    with open('./resource/raw/YonhMiuk.txt', 'r', encoding='utf-8') as f:
        file = f.read()
    file = re.sub('【[\u4e00-\u9fa5㮇?]+】', '', file)
    file = re.sub(' ', '', file)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(file)
    basic_table = pd.read_csv(path).iloc[:,1:]
    table_khai = basic_table.copy()#.iloc[:,1:]
    table_khai.columns = ['A','B','C','D']
    return table_khai

def insert(df, i, df_add):
    '''
    以 pandas 爲基礎。

    指定第 i 行位置插入數據 (start from 0)。
    '''
    df_add = pd.DataFrame(df_add)
    if df.shape[1] == df_add.shape[1]:
        None
    else:
        df_add = df_add.T
    df_add.columns=df.columns
    df1 = df.iloc[:i, :]
    df2 = df.iloc[i:, :]
    df_new = pd.concat([df1, df_add, df2], ignore_index=True)
    return df_new

def swapping_row(table, col, item1, item2):
    '''
    以 pandas 爲基礎。

    以給定的列爲依據來定位給定值，交換給定值所在行的位置。
    '''
    item1_index = table[table[col]==item1].index.tolist()[0]
    item2_index = table[table[col]==item2].index.tolist()[0]
    copy1, copy2 = table.iloc[item1_index].copy(), table.iloc[item2_index].copy()
    table.iloc[item1_index], table.iloc[item2_index] = copy2, copy1
    return table

def create_YonhMiuk_table(table, table_rules, yonh_rules, save=False):
    """
    生成 pandas 格式的韻母表格。(需要 pandas 庫。)

    將生成的表格保存在 "./resource/coproducts/YonhMiuk.csv "路徑下，默認不保存。
    """
    table_khai = table
    # g先f仙順序
    table_khai = swapping_row(table_khai, "A", "先", "仙")
    # 無視重紐 (支脂祭眞諄仙宵清侵鹽)
    table_khai = table_khai.drop(table_khai[table_khai["C"].str.contains("[AB]")==True].index.tolist())
    # 一韻多目 (東分AB，麻分no，庚分rs)
    doubleMiuk_list = table_rules["replace"]["doubleMiuk"]
    for i in doubleMiuk_list:
        index = table_khai[table_khai["A"]==i].index.tolist()[0]
        table_khai = insert(table_khai, index, table_khai[table_khai["A"]==i])
    # 創建開合表
    table_ghop = pd.DataFrame(index=range(0, len(table_khai)), columns=['I','J','K','L'])
    table_ghop_nd = pd.DataFrame(index=range(0, len(table_khai)), columns=['M','N','O','P'])
    # 多韻同目 (V眞c寒l歌)
    sameMiuk_dict = table_rules["replace"]["sameMiuk"]
    for main, secondary in sameMiuk_dict.items():
        main_index = table_khai[table_khai["A"]==main].index.tolist()[0]
        secondary_index = table_khai[table_khai["A"]==secondary].index.tolist()[0]
        table_ghop.iloc[main_index] = table_khai.iloc[secondary_index]
        if main != "歌":
            table_khai = table_khai.drop(secondary_index).reset_index().drop(["index"], axis=1)
            table_ghop = table_ghop.drop(secondary_index).reset_index().drop(["index"], axis=1)
            table_ghop_nd = table_ghop_nd.drop(secondary_index).reset_index().drop(["index"], axis=1)
    # 合并開合表，創建Symbol
    table = pd.concat([table_khai, table_ghop, table_ghop_nd], axis=1)
    table.insert(0, "Symbol", None)
    table.Symbol = (
        [chr(i) for i in range(ord('A'),ord('Z')+1)] + 
        [chr(i) for i in range(ord('a'),ord('z')+1)] + 
        [str(i) for i in range(10)] + 
        list(table.Symbol)
    )[:len(table.Symbol)]
    table = table.set_index("Symbol")
    # 增訂表内容
    for symbol, cols in table_rules["replace"]["update"].items():
        for i in symbol:
            table.loc[i, list(cols[0])] = table.loc[i, list(cols[1])].values
    # 增加等呼信息
    for k, v in yonh_rules["tongx"].items(): # 等
        # print(k, v)
        table.loc[v] += k
    for k, v in yonh_rules["ho"].items(): # 呼
        table.loc[:,v] += k
    for k, v in yonh_rules["deuh"].items(): # 調
        table.loc[:,v] += k[0]
    # 保存文件
    if save:
        table.to_csv('./resource/coproducts/YonhMiuk.csv', index=True, encoding='utf-8-sig')
        print("- 韻母表已保存。")
    return table

def create_YonhMiuk_IPA_table(table, rules, save=False):
    """
    生成 pandas 格式的韻母音標表格。(需要 pandas 庫。)

    將生成的表格保存在 "./resource/coproducts/YonhMiuk_IPA.csv" 路徑下，默認不保存。
    """
    IPA_table = table.copy()
    # 以音標覆蓋
    for index, IPA in rules["yonh_IPA"].items(): 
        IPA_table.loc[index, IPA_table.loc[index].notnull()] = IPA
        # 創建合口韻的音標
        if index in rules["only_ghop"]:
            ghop = IPA
        else:
            if index in rules["tongx"]["一"]:
                ghop = "u" + IPA
            elif index in rules["tongx"]["二"]:
                ghop = "o" + IPA[1:]
            elif index in rules["tongx"]["三"]:
                ghop = IPA[:2]+"u"+IPA[2:]
            else:
                ghop = IPA[0] + "u" + IPA[1:]
        # 創建入聲音標
        if IPA[-1] == "m":
            njip = IPA[:-1] + "p"
            njip_ghop = ghop[:-1] + "p"
        elif IPA[-1] == "n":
            njip = IPA[:-1] + "t"
            njip_ghop = ghop[:-1] + "t"
        elif IPA[-1] == "ŋ":
            njip = IPA[:-1] + "k"
            njip_ghop = ghop[:-1] + "k"
        # 以入聲音標覆蓋
        if type(IPA_table.loc[index, "D"]) == str:
            IPA_table.loc[index, "D"] = njip
        if type(IPA_table.loc[index, "L"]) == str:
            IPA_table.loc[index, "L"] = njip_ghop
        # 以合口韻的音標覆蓋
        for i in range(3):
            if type(IPA_table.loc[index, rules["ho"]["合"][i]]) == str:
                if type(IPA_table.loc[index, rules["ho"]["開"][i]]) == str:
                    IPA_table.loc[index, rules["ho"]["合"][i]] = ghop
    # 眞部特殊合口韻音標
    for i in range(3):
        IPA_table.loc["V", ["M", "N", "P"][i]] = IPA_table.loc["V", ["I", "J", "L"][i]]
    # 等
    for k, v in rules["deuh"].items():
        # print(k, k[1:])
        IPA_table.loc[:,v] += k[1:]
    # 保存文件
    if save:
        IPA_table.to_csv("./resource/coproducts/YonhMiuk_IPA.csv", index=True, encoding='utf-8-sig')
        print("- 韻母音標表已保存。")
    return IPA_table

def create_YonhMiuk_Alphabet_table(table, rules, save=False):
    """
    生成 pandas 格式的韻母拼音表格。(需要 pandas 庫。)

    將生成的表格保存在 "./resource/coproducts/YonhMiuk_Alphabet.csv "路徑下，默認不保存。
    """
    Alphabet_table = table.copy()
    Alphabet_table = Alphabet_table.replace(rules["yonh"].keys(), rules["yonh"].values(), regex=True)
    Alphabet_table = Alphabet_table.replace(rules["deuh"].keys(), rules["deuh"].values(), regex=True)
    Alphabet_table = Alphabet_table.replace(rules["replace"].keys(), rules["replace"].values(), regex=True)
    # 保存文件
    if save:
        Alphabet_table.to_csv("./resource/coproducts/YonhMiuk_Alphabet.csv", index=True, encoding='utf-8-sig')
        print("- 韻母拼音表已保存。")
    return Alphabet_table

def table_to_json(table, name="", path=None):
    """
    將 pandas 表格轉化爲 json 格式。(需要 pandas, json 庫。)

    將 json 格式的數據保存在指定路徑下，默認不保存。
    """
    newjson = table.to_json(orient = "index", force_ascii=False)
    newjson = json.loads(newjson)
    # print(type(newjson))
    # print(newjson.values())
    for item in newjson.values():
        for key in list(item.keys()):
            # print(key, end='')
            if not item.get(key):
                # print(key, end='')
                item.pop(key)
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(newjson, indent=4, separators=(',', ': '), ensure_ascii=False))
        print(name + " json 文件已創建。")
    return newjson

def read_KuangxYonh(path="./resource/coproducts/KuangxYonh.txt", save=False):
    """
    從格式化的《廣韻》文件中讀取信息。

    將生成的表格保存在 "./resource/coproducts/KuangxYonh_info.json "路徑下，默認不保存。
    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    symbol = []; pyanxchet = []
    char_list = []; yonhmiuk = []; meaning = []
    info = None
    for i in lines:
        if re.match('[a-z A-z 0-9] [a-z A-z 0-9]{2}[^a-z^A-z^0-9]{2}', i)!=None:
            info = i
        elif i != "\n":
            symbol.append(info[0:4]) # ignore PyanxChet
            pyanxchet.append(info[4:6])
            char_list.append(i[0])
            yonhmiuk.append(i[1])
            meaning.append(re.sub('\n', '', i[2:]))
    sjeng_mux = [i[0] for i in symbol]
    yonh_miuk = [i[2:4] for i in symbol]
    KuangxYonh_json = {
        "CHAR": char_list, 
        "PYANXCHET": pyanxchet, 
        "MEANING": meaning, 
        "SJENGMUX_symbol": sjeng_mux, 
        "YONHMIUK_symbol": yonh_miuk
    }
    # 保存文件
    if save:
        with open("./resource/coproducts/KuangxYonh_info.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(KuangxYonh_json, indent=4, separators=(',', ': '), ensure_ascii=False))
        print("\n- 《廣韻》信息已保存。")
    return KuangxYonh_json

def create_SjengYonh(sjeng_mux, yonh_miuk, sjeng_json, yonh_json, IPA_json, Alphabet_rules, save=False):
    """
    創建包含聲韻信息的 json 格式數據。

    將生成的表格保存在 "./resource/coproducts/SjengYonh.json "路徑下，默認不保存。
    """
    SjengYonh = []; SjengYonh_IPA = []; SjengYonh_Alphabet = []
    for i in range(len(sjeng_mux)):#[:10]:
        # print('\n', item)
        [(sjeng, [sjeng_IPA, _])] = sjeng_json[sjeng_mux[i]].items()
        SjengYonh.append(sjeng + yonh_json[yonh_miuk[i][0]][yonh_miuk[i][1]])
        SjengYonh_IPA.append(sjeng_IPA + IPA_json[yonh_miuk[i][0]][yonh_miuk[i][1]])
        # Alphabet = sjeng_IPA + IPA_json[yonh_miuk[i][0]][yonh_miuk[i][1]]
        # for ipa, alphabet in Alphabet_rules.items():
        #     Alphabet = re.sub(ipa, alphabet, Alphabet)
        yonhmiuk_IPA = IPA_json[yonh_miuk[i][0]][yonh_miuk[i][1]]
        deuh_IPA = re.sub("\S*[^˥˧]", "", yonhmiuk_IPA)
        yonh_IPA = re.sub(deuh_IPA, "", yonhmiuk_IPA)
        # if sjeng_mux[i] == "Y": 
        #     print(yonhmiuk_IPA, yonh_IPA + " " + deuh_IPA)
        sjeng_Alphabet = re.sub(sjeng_IPA, Alphabet_rules["sjeng"][sjeng_IPA], sjeng_IPA)
        yonh_Alphabet = yonh_IPA
        for k, v in Alphabet_rules["yonh"].items():
            yonh_Alphabet = re.sub(k, v, yonh_Alphabet)
        deuh_Alphabet = re.sub(deuh_IPA, Alphabet_rules["deuh"][deuh_IPA], deuh_IPA)
        # if sjeng_mux[i] == "Y": 
        #     print(yonh_Alphabet + deuh_Alphabet + '|')
        Alphabet = sjeng_Alphabet + yonh_Alphabet + deuh_Alphabet
        for k, v in Alphabet_rules["replace"].items():
            Alphabet = re.sub(k, v, Alphabet)
        SjengYonh_Alphabet.append(Alphabet)
    SjengYonh_json = {
        "SjengYonh": SjengYonh, 
        "SjengYonh_IPA": SjengYonh_IPA, 
        "SjengYonh_Alphabet": SjengYonh_Alphabet
    }
    # 保存文件
    if save:
        with open("./resource/coproducts/SjengYonh.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(SjengYonh_json, indent=4, separators=(',', ': '), ensure_ascii=False))
        print("- 聲韻信息已保存。")
    return SjengYonh_json

def create_KuangxYonh_json(KuangxYonh_text, SjengYonh_info, path=None):#"./KuangxYonh.json"):
    """
    根據從格式化的《廣韻》文件中提取的信息，創建《廣韻》 json 文件。

    將 json 格式的數據保存在指定路徑下，默認不保存。
    """
    pyanxchet, char_list, sjeng_mux, yonh_miuk, meaning = KuangxYonh_text["PYANXCHET"], KuangxYonh_text["CHAR"], KuangxYonh_text["SJENGMUX_symbol"], KuangxYonh_text["YONHMIUK_symbol"], KuangxYonh_text["MEANING"]
    SjengYonh, SjengYonh_IPA, SjengYonh_Alphabet = SjengYonh_info["SjengYonh"], SjengYonh_info["SjengYonh_IPA"], SjengYonh_info["SjengYonh_Alphabet"]

    json_text = []
    for i in range(len(char_list)):
        json_text.append(
            {"CHAR":char_list[i], 
            "PYANXCHET":pyanxchet[i], 
            "SJENGYONH":SjengYonh[i], 
            "SJENGYONH_IPA":SjengYonh_IPA[i], 
            "SJENGYONH_ALPHABET":SjengYonh_Alphabet[i], 
            "MEANING":meaning[i], 
            "SJENGMUX_symbol":sjeng_mux[i], 
            "YONHMIUK_symbol":yonh_miuk[i]}
        )
    # json_text = json.dumps(json_text, indent=4, separators=(',', ': '), ensure_ascii=False)
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"KuangxYonh": json_text}, indent=4, separators=(',', ': '), ensure_ascii=False))
        print("\n《廣韻》 json 文件已創建。\n")
    return json_text

def merge_json(KuangxYonh_json, sjeng_json, yonh_json, IPA_json, yonh_Alphabet_json, path):
    """
    合并所有 json 格式的數據。

    將 json 格式的數據保存在指定路徑下。
    """
    json_text = {
        "KuangxYonh": KuangxYonh_json, 
        "sjeng": sjeng_json, 
        "yonh": yonh_json, 
        "IPA": IPA_json, 
        "Alphabet": yonh_Alphabet_json
    }
    json_text = json.dumps(json_text, indent=4, separators=(',', ': '), ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json_text)
    print("總合 json 文件已創建。\n")


# 已棄用
# def store_database(
#     char_list, yonh, meaning, path="./resource/KuangxYonh.db"
# ):
#     """
#     基於 Sqlite3 數據庫。

#     **已放棄使用**。
#     """
#     if os.path.isfile(path):
#         os.remove(path)
#     sjeng_mux = [i[0] for i in yonh]
#     yonh_miuk = [i[2:4] for i in yonh]
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE YONH(
#         ID integer primary key autoincrement, 
#         CHAR varchar(20), 
#         SJENGMUX varchar(20), 
#         YONHMIUK varchar(20), 
#         MEANING varchar(20))''')
#     for i in range(len(char_list)):
#         cursor.execute("INSERT INTO YONH (CHAR, SJENGMUX, YONHMIUK, MEANING) \
#             VALUES(?, ?, ?, ?)", 
#             (char_list[i], sjeng_mux[i], yonh_miuk[i], meaning[i]))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return None
