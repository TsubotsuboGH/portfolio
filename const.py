### model を作成するための dict の list ########################################
LIST_DICT_TO_CREATE_MODEL \
: list[
    dict[str,
        str |
        bool |
        dict[str,
            str |
            int |
            float
        ] |
        list[
            dict[str,
                str |
                float |
                list[
                    dict[str,
                        str |
                        int |
                        dict[str,
                            int]]]]]]] \
= [
    ### 1着 ####################################################################
    {
        "type_d1a_y"
        : "i1chaku",
        "use_optuna"
        : [True, False, ][0],
        "params"
        : {},
        "list_dict_bairitsu"
        : [
            {
                "type_data"
                : "train",
                "rate"
                : 0.64,
                "list_dict_amp"
                : [
                    {   "type_amp"
                        : "random_select",
                        "bairitsu"
                        : { "min_count_of_data"
                            : 400000, },
                    },
                    {
                        "type_amp"
                        : "random_umaban",
                        "bairitsu"
                        : 1
                    },
                    # {
                    #     "type_amp"
                    #     : "random_umaban",
                    #     "bairitsu"
                    #     : { "min_count_of_data"
                    #         : 1000000, },
                    # },
                ],
            },
            {
                "type_data"
                : "valid",
                "rate"
                : 0.8,
                "list_dict_amp"
                : [
                    {
                        "type_amp"
                        : "random_umaban",
                        "bairitsu"
                        : "$0.list_dict_amp.$0.bairitsu",
                    },
                    # {
                    #     "type_amp"
                    #     : "random_select",
                    #     "bairitsu"
                    #     : "$0.list_dict_amp.$0.bairitsu",
                    # },
                    # {
                    #     "type_amp"
                    #     : "random_umaban",
                    #     "bairitsu"
                    #     : 1
                    # },
                ],
            },
            {
                "type_data"
                : "test",
                "rate"
                : 1.0,
                "list_dict_amp"
                : [
                    {
                        "type_amp"
                        : "random_umaban",
                        "bairitsu"
                        : 100,
                    },
                ],
            },
        ],
    },
    ### 1番人気 ################################################################
    {
        "type_d1a_y"
        : "i1ninki",
        "use_optuna"
        : [True, False, ][0],
        "params"
        : {},
        "list_dict_bairitsu"
        : [
            {
                "type_data"
                : "train",
                "rate"
                : 0.64,
                "list_dict_amp"
                : [
                    {
                        "type_amp"
                        : "random_umaban",
                        "bairitsu"
                        : { "min_count_of_data"
                            : 400000, },
                    },
                ],
            },
            {
                "type_data"
                : "valid",
                "rate"
                : 0.8,
                "list_dict_amp"
                : [
                    {
                        "type_amp"
                        : "random_umaban",
                        "bairitsu"
                        : "$0.list_dict_amp.$0.bairitsu",
                    },
                    # {
                    #     "type_amp"
                    #     : "random_select",
                    #     "bairitsu"
                    #     : "$0.list_dict_amp.$0.bairitsu",
                    # },
                    # {
                    #     "type_amp"
                    #     : "random_umaban",
                    #     "bairitsu"
                    #     : 1
                    # },
                ],
            },
            {
                "type_data"
                : "test",
                "rate"
                : 1.0,
                "list_dict_amp"
                : [
                    {
                        "type_amp"
                        : "random_umaban",
                        "bairitsu"
                        : 100,
                    },
                ],
            },
        ],
    },
]#[1:]
### model の pkl の保存先 ######################################################
DIR_PKL_MODEL: str \
= "pkl/model/"
### 当日予測するレースの情報 ###################################################
NEN  : int \
= 2024
TSUKI: int \
= 8
HI   : int \
= 24
### mongodbのuri ###############################################################
URI_MONGODB: str \
= "mongodb://localhost:27017/"
### dbのname ###################################################################
NAME_DB    : str \
= "test"
### collectionのnameのdict #####################################################
### 必須: raceキー
DICT_NAME_COLLECTION: dict[str, str] \
= {
    # "race": "race_netkeiba",
    "race"     : "race_netkeiba_1", # race : レース情報を document に持つ collection の名前
    "keisu"    : "keisu",           # keisu: 係数の情報を document に持つ collection の名前
    "pedigree" : "pedigree",        # pedigree: 血統の情報
    # rating 等を算出するのに使用した、あるいはこれからも使用する
    # 変数を記録したもの。
    "dir_file" : "dir_file",
    "rating"   : "rating",
    "model"    : "model",
    "other"    : "other", # 雑多なもの置き場
}
### rating の type #############################################################
TYPE_RATING: str \
= ["race", "day", ][1]
### 増幅前の最低データ数 #######################################################
MIN_LEN_LIST_DICT_RACE: int \
= 25
### 増幅後の最低データ数 #######################################################
# WANT       : int \
# = 100000
### list_filter (race) #########################################################
LIST_FILTER_RACE: list[dict[str, int]] \
= [
    {
        "keibajo": 4,
        "kyori": 2850,
        "kyoso": 2,
        "calc.tousu": 14,
        "baba": 0,
    },
]
### list_id_race_prod / 当日予測用 #############################################
LIST_ID_RACE_PROD: list[str] \
= [
    "202404030707",
]
### list_list_key ##############################################################
LIST_LIST_KEY: list[list[str]] = [
    [   "list_horse.$.sei",            ],
]
