<div align="center">
    <h1 align="center">中夏正音</h1>
    <b>
        <p align="center" style="font-size: larger">讀經之法，法中夏之音，此是九天之正音也。</p>
        <p align="right">——《上清太極隱注玉經寶訣》</p>
    </b>
</div>

按魏晉音系，處於上古、中古漢語交際時期，上承秦漢、下啓唐宋。而道教諸經籍，亦多出於六朝，故所言「正音」，當爲《切韻》所反映六朝音系。

本項目以王力先生的著作《漢語語音史》爲依據，擬定六朝中古漢語音韻。

## 項目結構

```
TyongGheax-TjyengqYem
├── docs/
│   ├── 拉丁化.md
│   ├── 聲韻.md
│   └── 數據說明.md          
├── resource/
│   ├── coproducts/
│   │   ├── KuangxYonh.txt
│   │   ├── Yonh_table.csv
│   │   ├── YonhMiuk_IPA.csv
│   │   └── YonhMiuk.csv
│   ├── raw/
│   │   ├── qieyun@0.13.4/          # 文本來源於 qieyun-js 項目中所提及鏈接
│   │   │   ├── index.js
│   │   │   ├── qieyun@0.13.4.js
│   │   │   └── qieyun@0.13.4.txt
│   │   └── YonhMiuk.txt            # 韻目表，來源於“韻典網”
│   ├── rules/
│   │   ├── revise.json             # 針對切韻文本的修正設定
│   │   └── Yonh_table.json         # 針對韻母表格的修正設定
│   └── settings/
│       ├── Latinisation.json       # 拉丁化設定
│       ├── SjengMux.json           # 聲母設定
│       └── YonhMiuk.json           # 韻母設定
├── scripts/
│   ├── function.py
│   └── run.py
├── .gitignore
├── KuangxGhyuenq.json              # 整合後的最終文本數據
├── README.md
└── requirements.txt
```

## 參考

<!-- 王力. 《王力全集》第二卷《汉语语音史》卷上第三章《魏晋南北朝音系（220——581）》, 北京: 中華書局, 2014 年, 第 108-161 頁. -->

<!-- 魏晋南北朝音系（220—581）[M] // 王力. 汉语语音史: 卷上. 北京: 中華書局, 2014: 108-161. -->

[王力. 汉语语音史](https://downloads.freemdict.com/uploads/manjushri/分流/王力全集(全25卷)/王力全集02.汉语语音史.pdf)[M]. 北京: 中華書局, 2014.

[王力. 中国语言学史](https://downloads.freemdict.com/uploads/manjushri/分流/王力全集(全25卷)/王力全集05.中国语言学史.pdf)[M]. 北京: 中華書局, 2013.

<!-- [GitHub@nk2028/qieyun-js](https://github.com/nk2028/qieyun-js#Usage) [#Usage](https://cdn.jsdelivr.net/npm/qieyun@0.13.4) -->

@nk2028. [qieyun-js: README#Usage.](https://github.com/nk2028/qieyun-js#Usage) [DS/OL]. (2022-09-06)[2023-02-04].

<!-- [GitHub@Sêkai Zhou](https://github.com/syimyuzya)：

- [有女同車《〈廣韻〉全字表》原表](https://github.com/syimyuzya/guangyun0704) -->
