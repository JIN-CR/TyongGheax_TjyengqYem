# # When this code is under /resource folder. 
# # Guided by https://zhuanlan.zhihu.com/p/64893308
# import sys; sys.path.append("")
# from scripts.function import *
from function import *

if __name__ == "__main__":
    """
    1. 依據"revise.json"中給定的規則, 
       修訂從原始js文件中獲取的"qieyun@0.13.4.txt"的文本內容. 
    """
    text = formated_qieyun_text()#; print(text)
    revise_rules = read_rules("./resource/rules/revise.json")
    # print(len(rules["replace"]["mistakes"]["rule"]))#.keys()); # print(len(rules["replace"]["mistakes"]["values"]))#.keys())
    revise_qieyun(text, revise_rules)

    """
    2. 生成 json 格式的聲母信息 "sjeng_json". 
    """
    sjeng_rules = read_rules("./resource/settings/SjengMux.json")
    Alphabet_rules = read_rules("./resource/settings/Latinisation.json")
    sjeng_json = create_sjengmux_json(sjeng_rules, Alphabet_rules["sjeng"], path="./output/sjeng.json")
    # print(sjeng_json)

    """
    3. 生成 json 格式的韻母信息 "yonh_json", 
       生成 json 格式的韻母音標信息 "yonh_IPA_json". 
       生成 json 格式的韻母拼音信息 "yonh_Alphabet_json". 
    """
    table_khai = read_YonhMiuk()
    table_rules = read_rules("./resource/rules/Yonh_table.json")
    yonh_rules = read_rules("./resource/settings/YonhMiuk.json")
    yonh_table = create_YonhMiuk_table(table_khai, table_rules, yonh_rules, save=True)
    yonh_IPA_table = create_YonhMiuk_IPA_table(yonh_table, yonh_rules, save=True)
    yonh_Alphabet_table = create_YonhMiuk_Alphabet_table(yonh_IPA_table, Alphabet_rules, save=True)
    # print(yonh_table); # print(yonh_IPA_table)
    yonh_json = table_to_json(yonh_table, "韻母", "./output/yonh.json")
    yonh_IPA_json = table_to_json(yonh_IPA_table, "韻母音標", "./output/yonh_IPA.json")
    yonh_Alphabet_json = table_to_json(yonh_Alphabet_table, "韻母拼音", "./output/yonh_Alphabet.json")

    """
    4. 生成 json 格式的《廣韻》信息 "KuangxYonh_json". 
    """
    # store_database(char_list, symbol, meaning) # 已棄用
    # char_list, symbol, meaning = read_KuangxYonh()
    KuangxYonh_text = read_KuangxYonh(save=True)
    # print(KuangxYonh_text["symbol"])
    # item = "N mJ"; # print(sjeng_json[item[0]].keys()); print(yonh_json[item[2]][item[3]]); # [(sjeng, sjeng_IPA)] = sjeng_json[item[0]].items(); # print(sjeng)
    SjengYonh_info = create_SjengYonh(KuangxYonh_text["SJENGMUX_symbol"], KuangxYonh_text["YONHMIUK_symbol"], sjeng_json, yonh_json, yonh_IPA_json, Alphabet_rules, save=False)
    # print(SjengYonh_info["SjengYonh"][:10])
    # print(SjengYonh_info["SjengYonh_IPA"][:10])
    # print(SjengYonh_info["SjengYonh_Alphabet"][:10])
    KuangxYonh_json = create_KuangxYonh_json(KuangxYonh_text, SjengYonh_info, path="./output/KuangxYonh.json")
    # print(KuangxYonh_json[:10])

    """
    5. 合并所有 json 格式信息. 
    """
    merge_json(KuangxYonh_json, sjeng_json, yonh_json, yonh_IPA_json, yonh_Alphabet_json, "KuangxGhyueenq.json")

