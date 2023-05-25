import json
import pymysql
import re

######################## json ########################
with open("./resource/coproducts/KuangxYonh_info.json", 'r', encoding='utf-8') as f:
    KuangxYonh_info = json.loads(f.read())

with open("./output/sjeng.json", 'r', encoding='utf-8') as f:
    sjeng = json.loads(f.read())

with open("./output/yonh.json", 'r', encoding='utf-8') as f:
    yonh = json.loads(f.read())
with open("output/yonh_IPA.json", 'r', encoding='utf-8') as f:
    yonh_IPA = json.loads(f.read())
with open("./output/yonh_Alphabet.json", 'r', encoding='utf-8') as f:
    yonh_Alphabet = json.loads(f.read())


######################## MySQL ########################
host = input("你的數據庫 host 是：（默認爲 localhost）")
user = input("你的數據庫用戶名是：（默認爲 root）")
pwd = input("你的數據庫密碼是：")
if not host: host = 'localhost'
if not user: user = 'root'
db = pymysql.connect(host=host,
                     user=user,
                     password=pwd,
                     database='kuangxghyueenq')
cursor = db.cursor()

# cursor.execute("DROP TABLE sjengmux;")
# cursor.execute("DROP TABLE yonhmiuk;")

sql_KuangxYonh = """
CREATE TABLE IF NOT EXISTS KuangxYonh (
    `ID`                 INT              NOT NULL     COMMENT '編號' AUTO_INCREMENT,
    `CHAR`               CHAR(1)          DEFAULT NULL COMMENT '字',
    `PYANXCHET`          CHAR(2)          DEFAULT NULL COMMENT '反切',
    `MEANING`            CHAR(230)        DEFAULT NULL COMMENT '釋義',
    `SJENGMUX_symbol`    CHAR(1)   BINARY DEFAULT NULL COMMENT '聲母符號',
    `YONHMIUK_symbol`    CHAR(2)   BINARY DEFAULT NULL COMMENT '韻母符號',
    PRIMARY KEY (ID)
) CHARSET=utf8mb4;
"""
sql_sjengmux = """
CREATE TABLE IF NOT EXISTS sjengmux (
    `SJENGMUX_symbol`   CHAR(1) BINARY NOT NULL     COMMENT '聲母符號',
    `SJENGMUX`          CHAR(1)        DEFAULT NULL COMMENT '聲母',
    `SJENGMUX_IPA`      CHAR(3)        DEFAULT NULL COMMENT '聲母IPA',
    `SJENGMUX_ALPHABET` CHAR(1)        DEFAULT NULL COMMENT '聲母拼音',
    PRIMARY KEY (SJENGMUX_symbol)
) CHARSET=utf8mb4;
"""
sql_yonhmiuk = """
CREATE TABLE IF NOT EXISTS yonhmiuk (
    `YONHMIUK_symbol`   CHAR(2) BINARY NOT NULL     COMMENT '韻母符號',
    `YONHMIUK`          CHAR(1)        DEFAULT NULL COMMENT '韻母',
    `YONHMIUK_IPA`      CHAR(3)        DEFAULT NULL COMMENT '韻母IPA',
    `YONHMIUK_ALPHABET` CHAR(1)        DEFAULT NULL COMMENT '韻母拼音',
    PRIMARY KEY (YONHMIUK_symbol)
) CHARSET=utf8mb4;
"""
cursor.execute(sql_KuangxYonh)
cursor.execute(sql_sjengmux)
cursor.execute(sql_yonhmiuk)

cursor.execute("SELECT COUNT(ID) FROM kuangxyonh;")
kuangxyonh_len = cursor.fetchone()[0]
if kuangxyonh_len < 25332:
    cursor.execute("TRUNCATE KuangxYonh;")
    for i in range(len(KuangxYonh_info['CHAR'])):
        sql_KuangxYonh_insert = """
        INSERT IGNORE INTO kuangxyonh (`ID`, `CHAR`, `PYANXCHET`, `MEANING`, `SJENGMUX_symbol`, `YONHMIUK_symbol`) 
        VALUES (%s, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")
        """ % (i+1, KuangxYonh_info["CHAR"][i], KuangxYonh_info["PYANXCHET"][i], KuangxYonh_info["MEANING"][i], KuangxYonh_info["SJENGMUX_symbol"][i], KuangxYonh_info["YONHMIUK_symbol"][i])
        data = cursor.execute(sql_KuangxYonh_insert)
    db.commit()

cursor.execute("SELECT COUNT(SJENGMUX_symbol) FROM sjengmux;")
sjengmux_len = cursor.fetchone()[0]
if sjengmux_len < 38:
    cursor.execute("TRUNCATE sjengmux;")
    for i in sjeng.keys():
        [(sjengmux, _)] = sjeng[i].items()
        [(sjengmux_IPA, sjengmux_Alphabet)] = sjeng[i].values()
        # print(i, sjengmux, sjengmux_IPA, sjengmux_Alphabet)
        sql_sjengmux_insert = """
        INSERT IGNORE INTO sjengmux (`SJENGMUX_symbol`, `SJENGMUX`, `SJENGMUX_IPA`, `SJENGMUX_ALPHABET`) 
        VALUES (\"%s\", \"%s\", \"%s\", \"%s\")
        """ % (i, sjengmux, sjengmux_IPA, sjengmux_Alphabet)
        data = cursor.execute(sql_sjengmux_insert)
    db.commit()

cursor.execute("SELECT COUNT(YONHMIUK_symbol) FROM yonhmiuk;")
yonhmiuk_len = cursor.fetchone()[0]
if yonhmiuk_len < 300:
    cursor.execute("TRUNCATE yonhmiuk;")
    for i in yonh.keys():
        for j in yonh[i].keys():
            sql_yonhmiuk_insert = """
            INSERT IGNORE INTO yonhmiuk (`YONHMIUK_symbol`, `YONHMIUK`, `YONHMIUK_IPA`, `YONHMIUK_ALPHABET`) 
            VALUES (\"%s\", \"%s\", \"%s\", \"%s\")
            """ % (i+j, yonh[i][j], yonh_IPA[i][j], yonh_Alphabet[i][j])
            data = cursor.execute(sql_yonhmiuk_insert)
    db.commit()

cursor.execute("""SHOW GLOBAL VARIABLES LIKE \"%datadir%\"""")
print("你的數據已保存在以下路徑：\n", re.sub(r'\\', '/', cursor.fetchone()[1])+'kuangxghyueenq')

db.close()