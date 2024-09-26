import itertools
import lightgbm as lgb
import math
import matplotlib.pyplot as plt
import numpy as np
from optuna_integration import lightgbm as lgb_o
import random
random.seed(20240907)

import bangirasu
import bomanda
import fukamaru2
import metagurosu

class Fukamaru3(bangirasu.Bangirasu):
    ### init ###################################################################
    def __init__(self,
    dict_to_create_model
    : dict[str,
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
                            int]]]]]],
    fu2
    : fukamaru2.Fukamaru2,
    bo
    : bomanda.Bomanda,
    ) -> None:
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.dict_to_create_model, self.fu2, \
        =    dict_to_create_model,      fu2,
        self.me, \
        =    metagurosu.Metagurosu(bo=bo, ),                                # !!!!
        self.type_d1a_y: str \
        = self.dict_to_create_model["type_d1a_y"] # type: ignore
        self.document_to_insert: dict \
        = { "filter_race"
            : self.fu2.filter_race,
            "path_pkl_model"
            : bo.dir_pkl_model + self.get_name_file() + ".pkl",
            "datetime"
            : self.fu2.datetime_latest_in_race, }
        ### return #############################################################
        return #################################################################
    ############################################################################
    def set_list_index_to_split(self, ):
        """
        3a-2b
        -----
        00. SET
        +-- self.list_index_to_split
        +-- self.list_dict_race を train、valid、test に split するための、
            index の list
        +-- [   0,
                train の end index,
                valid の end index,
                test  の end index, ]"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ### error ##############################################################
        if not isinstance(self.dict_to_create_model["list_dict_bairitsu"],list):
            self.raise_exception("type error") #################################
        ########################################################################
        self.list_index_to_split: list[int] \
        = (   [0]
            + [     self.raise_exception(msg="type error")
                if  not isinstance(
                        dict_bairitsu,
                        dict, )
                or  "rate" not in dict_bairitsu
                else
                    int(  len(self.fu2.list_dict_race)
                        * dict_bairitsu["rate"])
                if  isinstance(
                        dict_bairitsu["rate"],
                        float, )
                else
                    self.raise_exception(msg="type error", )
                for                                 dict_bairitsu
                in  self.dict_to_create_model["list_dict_bairitsu"]])       # 00
        ### cprint #############################################################
        self.cprint(self.list_index_to_split, ) ################################
        self.cprint(
            [     self.list_index_to_split[i+1]
                - self.list_index_to_split[i]
                for i
                in  range(len(self.list_index_to_split) - 1)],
            name_var=
                "(each count of data)", )
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def set_dict_list_dict_race(self, ):
        """
        3a-3
        ----
        00. NEW
        +-- self.dict_list_dict_race
        +-- self.fukamaru2.list_dict_race を
            train・valid・test に splitする。"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ### error ##############################################################
        if not isinstance(self.dict_to_create_model["list_dict_bairitsu"],list):
            self.raise_exception("type error") #################################
        ########################################################################
        self.dict_list_dict_race \
        = { dict_bairitsu["type_data"] # type: ignore
            : self.fu2.list_dict_race[
                self.list_index_to_split[i] : self.list_index_to_split[i+1]]
            ### error 回避用 ###################################################
            if  isinstance(
                    dict_bairitsu,
                    dict, )
            and "type_data" in dict_bairitsu
            and isinstance(
                    dict_bairitsu["type_data"],
                    str, )
            else
                self.raise_exception("type error")
            ### error 回避用 ここまで ##########################################
            for i, dict_bairitsu
            in  zip(
                range(len(self.list_index_to_split) - 1), # 3つに分けたいので -1
                self.dict_to_create_model["list_dict_bairitsu"], )}         # 00
        ### print ##############################################################
        for key in self.dict_list_dict_race: ###################################
            self.cprint(len(self.dict_list_dict_race[key])) ####################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def del_list_dict_race(self, ):
        """
        3a-4a
        -----"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        del self.fu2.list_dict_race
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def del_list_index_to_split(self, ):
        """
        3a-4b
        -----"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        del self.list_index_to_split
        ### return #############################################################
        return self ############################################################
    ### amp pattern 1 ##########################################################
    def set_p_to_amp(self, ):
        """
        3b
        --
        欲しいデータ数に応じて、順列 nPn の n の値を決める。
        ex. n = 5 の場合は、後ろ 5 頭のすべての順列を作成し、
            結合することを意味する。"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        count_race: int \
        = self.me.count_document(**{
            "key_collection"
            : "race",
            "filter"
            : self.fu2.filter_race, })
        threshold : float \
        = 100000 / (count_race * self.fu2.tousu) # 100000: 最低限欲しいデータ数 # tousu: ズラしの分
        self.p \
        = range(1, 11)[
            sum([   1
                for v
                in  [1, 2, 6, 24, 120, 720, 5040, 40320, ]
                if  v <= threshold])]
        if self.p > self.fu2.tousu:
            raise Exception("[IN set_p_to_amp] p が tousu を上回っています。")
        ### print ##############################################################
        self.cprint(self.p) ####################################################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def update_dict_list_dict_race_amp_old(self, ):
        """
        4
        -
        00. UPDATE
        +-- self.dict_list_dict_race
        +-- 必要データ数まで増幅する。"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.dict_list_dict_race \
        = { key_0
            : [   { key_1
                    : value_1
                    if   key_1 != "list_dict_horse"
                    else
                      (value_1[i:] + value_1[:i])[:-self.p]
                      + list(tuple_dict_horse_permutated)
                    for  key_1, value_1
                    in  dict_race.items()}
                for dict_race
                in  list_dict_race
                for i
                in  range(self.fu2.tousu) # ズラし
                for tuple_dict_horse_permutated
                in  itertools.permutations(
                    (dict_race["list_dict_horse"][i:]
                    + dict_race["list_dict_horse"][:i])[-self.p:])]
            for key_0, list_dict_race
            in  self.dict_list_dict_race.items()}                           # 00
        ### print ##############################################################
        for key in self.dict_list_dict_race: ###################################
            self.cprint(len(self.dict_list_dict_race[key])) ####################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def update_dict_list_dict_race_ran_old(self, ):
        """
        After: update_dict_list_dict_race_amp()
        ---------------------------------------"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.dict_list_dict_race \
        = { key_0
            : [   { key_1
                    : value_1
                    if key_1 != "list_dict_horse"
                    else
                      random.sample(value_1, len(value_1))
                    for  key_1, value_1
                    in  dict_race.items()}
                for dict_race
                in  list_dict_race]
            for key_0, list_dict_race
            in  self.dict_list_dict_race.items()}                           # 00
        ### print ##############################################################
        for key in self.dict_list_dict_race: ###################################
            self.cprint(len(self.dict_list_dict_race[key])) ####################
        ### return #############################################################
        return self ############################################################
    ### amp pattern 2 ##########################################################
    def update_dict_list_dict_race_amp(self, ):
        ### cprint #############################################################
        self.cprint() ##########################################################
        ### error ##############################################################
        if not isinstance(self.dict_to_create_model["list_dict_bairitsu"],list):
            self.raise_exception("type error") #################################
        ########################################################################
        for i,                                        dict_bairitsu \
        in  enumerate(self.dict_to_create_model["list_dict_bairitsu"]):
            ### error 回避 #####################################################
            if not (
                    isinstance(
                        dict_bairitsu,
                        dict, )
                and isinstance(
                        self.dict_to_create_model["list_dict_bairitsu"],
                        list, )):
                self.raise_exception("type error")
            ### erorr 回避 ここまで ############################################
            self.dict_to_create_model["list_dict_bairitsu"][i] \
            = { key
                : value
                if not isinstance(value, list, )
                else
                  [   dict_amp
                    | { "bairitsu"
                        : dict_amp["bairitsu"]
                        if isinstance(dict_amp["bairitsu"], int, )
                        else
                            self.get_nested_value(**{
                            "obj"
                            : self.dict_to_create_model["list_dict_bairitsu"],
                            "key"
                            : dict_amp["bairitsu"], })
                        if isinstance(dict_amp["bairitsu"], str, )
                        else
                            math.ceil(
                                dict_amp["bairitsu"]["min_count_of_data"]
                            // len(self.dict_list_dict_race[dict_bairitsu["type_data"]], ), )}
                    for dict_amp
                    in  value
                  ]
                for key, value
                in  dict_bairitsu.items()}
        for i,                                        dict_bairitsu \
        in  enumerate(self.dict_to_create_model["list_dict_bairitsu"]):
            ### error 回避 #####################################################
            if not (
                    isinstance(
                        dict_bairitsu,
                        dict, )
                and isinstance(
                        self.dict_to_create_model["list_dict_bairitsu"],
                        list, )):
                self.raise_exception("type error")
            ### erorr 回避 ここまで ############################################
            if not isinstance(dict_bairitsu["list_dict_amp"], list, ):
                self.raise_exception("type error")
            type_data \
            = dict_bairitsu["type_data"]
            for _, dict_amp in enumerate(dict_bairitsu["list_dict_amp"]):
                if not isinstance(dict_amp["bairitsu"], int, ):
                    self.raise_exception("bairitsu isn't int type")
                if   dict_amp["type_amp"] == "random_select":
                    self.dict_list_dict_race[type_data] \
                    = [ {   "id_race"
                            : str(k),
                            "datetime"
                            : str(k),
                            "list_dict_horse"
                            : random.sample(
                                population=
                                    [   self.dict_list_dict_race
                                        [type_data]
                                        [random.randrange(
                                            len(self.dict_list_dict_race[type_data]))]
                                        ["list_dict_horse"]
                                        [l]
                                        for l
                                        in  range(self.fu2.tousu) ],
                                k=  self.fu2.tousu), }
                        for k
                        in  range(
                                  dict_amp["bairitsu"]
                                * len(self.dict_list_dict_race[type_data])) ]
                elif dict_amp["type_amp"] == "random_umaban":
                    self.dict_list_dict_race[type_data] \
                    = [ {   key_1
                            : value_1
                            if key_1 != "list_dict_horse"
                            else
                            random.sample(value_1, len(value_1), )
                            for key_1, value_1
                            in  dict_race.items() }
                        for dict_race
                        in  self.dict_list_dict_race[type_data]
                        for _
                        in  range(dict_amp["bairitsu"]) ] # 1Rあたり何倍にするか
                else:
                    self.raise_exception("type_amp error")
        ### print ##############################################################
        for key in self.dict_list_dict_race: ###################################
            self.cprint(len(self.dict_list_dict_race[key])) ####################
        ### return #############################################################
        return self ############################################################
    ### amp pattern fin ########################################################
    ############################################################################
    def set_dict_data(self, ):
        """
        5
        -
        00. NEW
        +-- self.dict_data
        +-- 01. list_dict_race を dict_race として loop する。
            02. dict_race から、各特徴量を抽出し、list 化・ndarray 化する。"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.dict_data \
        = { key_0
            : { "d2a_x"
                : np.array([
                    sum([   dict_horse["rating"]
                        for dict_horse
                        in  dict_race["list_dict_horse"]],
                        [], )
                    # + [dict_race["baba"]] # 馬場情報を追加する
                    for dict_race
                    in  list_dict_race]),
                "list_list_umaban"
                : [ [       dict_horse["umaban"]
                        for dict_horse
                        in  dict_race["list_dict_horse"]]
                    for dict_race
                    in  list_dict_race],
                "d2a_x10tansho"
                : np.array([
                    [       dict_horse["x10tansho"]
                        for dict_horse
                        in  dict_race["list_dict_horse"]]
                    for dict_race
                    in  list_dict_race]),
                "list_id_race"
                : [     dict_race["id_race"] # race の id
                    for dict_race
                    in  list_dict_race],
                "list_datetime"
                : [     dict_race["datetime"] # datetime
                    for dict_race
                    in  list_dict_race], }
            | {
                ### i1chaku pattern 1 : 1着馬の index を time から取得 #########
                "d1a_y_{}".format(self.type_d1a_y)
                : np.array([
                        np.argmin([
                                (     100000
                                    if dict_horse["x10time"] is None
                                    else
                                    dict_horse["chakujun"]
                                    if key_0 in ["test"]
                                    else
                                    dict_horse["x10time"])
                            for dict_horse
                            in  dict_race["list_dict_horse"]
                        ])
                    if key_0 in ["train", "valid", ]
                    else
                        [       dict_horse["chakujun"]
                            for dict_horse
                            in  dict_race["list_dict_horse"]
                        ].index(1)
                    if key_0 in ["test"]
                    else
                        self.raise_exception("i1chaku error")
                    for dict_race
                    in  list_dict_race])
                ### i1chaku pattern 2 : 1着馬の index をそのまま取得 ###########
                # "d1a_y_i1chaku"
                # : np.array([
                #     [       dict_horse["chakujun"]
                #         for dict_horse
                #         in  dict_race["list_dict_horse"]
                #     ].index(1)
                #     for dict_race
                #     in  list_dict_race]),
                ### i1chaku pattern fin ########################################
                if self.type_d1a_y == "i1chaku"
                ### i1ninki ####################################################
                else
                  np.array([
                    [       dict_horse["ninki"]
                        for dict_horse
                        in  dict_race["list_dict_horse"]
                    ].index(1)
                    for dict_race
                    in  list_dict_race])
                if self.type_d1a_y == "i1ninki"
                ### error ######################################################
                else
                  self.raise_exception()
                ################################################################
            }
            for key_0, list_dict_race
            in  self.dict_list_dict_race.items()}                           # 00
        ### print ##############################################################
        self.cprint(self.dict_data.keys()) #####################################
        for key in self.dict_data.keys(): ######################################
            self.cprint(self.dict_data[key]["d2a_x"].shape) ####################
        for key in self.dict_data: #############################################
            self.cprint(set(list(self.dict_data[key][f"d1a_y_{self.type_d1a_y}"])))
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def del_dict_list_dict_race(self, ):
        """
        6a
        --"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        del self.dict_list_dict_race
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def set_dataset(self):
        """
        6b
        --
        00. NEW
        +-- dataset
        +-- 最初に train を追加する。
        01. SET
        +-- self.dataset
        +-- 次に valid を追加する。
            reference に train を指定する必要があるので、00. と分けている。"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        dataset \
        = { "train"
            : lgb.Dataset(**{
                "data"
                : self.dict_data
                    ["train"]
                    ["d2a_x"],
                "label"
                : self.dict_data
                    ["train"]
                    ["d1a_y_{}".format(self.type_d1a_y, )], }), }           # 00
        self.dataset \
        = (   dataset
            | { "valid"
                : lgb.Dataset(**{
                    "data"
                    : self.dict_data
                        ["valid"]
                        ["d2a_x"],
                    "label"
                    : self.dict_data
                        ["valid"]
                        ["d1a_y_{}".format(self.type_d1a_y, )],
                    "reference"
                    : dataset
                        ["train"], }), })                                   # 01
        ### return #############################################################
        return self ############################################################
    ### lgb_o ##################################################################
    def set_model(self):
        """
        7
        -"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        if not isinstance(self.dict_to_create_model["params"], dict):
            self.raise_exception("type error")
        params \
        = (   self.dict_to_create_model["params"]
            | { # 学習対象: 多クラス分類
                "objective"
                : "multiclass",
                # クラス数
                "num_class"
                : len(set(self.dict_data
                    ["train"]
                    ["d1a_y_{}".format(self.type_d1a_y, )])), } )
        arg \
        = { "params"
            : params,
            "train_set"
            : self.dataset["train"],
            "num_boost_round"
            : 1000,
            "valid_sets"
            : [ self.dataset["valid"], ],
            "callbacks"
            : [ lgb.early_stopping(stopping_rounds=100),
                lgb.log_evaluation(0), ], }
        if self.dict_to_create_model["use_optuna"]:
            self.model \
            = lgb_o.train(**arg)
        else:
            self.model \
            = lgb.train(**arg)
        ### print ##############################################################
        self.cprint(self.model.params) #########################################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def save_model(self, ):
        """
        8
        -"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.dump_pkl(**{
            "dir_file"
            : self.document_to_insert["path_pkl_model"],
            "obj"
            : self.model, })
        self.me.delete_one(**{
            "key_collection"
            : "model",
            "filter"
            : { "filter_race"
                : self.fu2.filter_race, }, })
        self.me.insert_one(**{
            "key_collection"
            : "model",
            "document"
            : self.document_to_insert, })
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def set_d2a_pred(self, type_pred: str, ):
        """
        9
        -
        type_pred: test or prod"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        src_d2a_pred \
        = self.model.predict(self.dict_data[type_pred]["d2a_x"])
        ### verify #############################################################
        if not isinstance(src_d2a_pred, np.ndarray, ): #########################
            self.raise_exception("type error") #################################
        ########################################################################
        self.d2a_pred: np.ndarray \
        = src_d2a_pred
        ### print ##############################################################
        self.cprint(self.d2a_pred) #############################################
        self.cprint(self.d2a_pred.shape) #######################################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def insert_data_to_analyze(self, ):
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        id_doc \
        = self.get_name_file() # <----------------------------------------------
        self.cprint(id_doc) # <-------------------------------------------------
        self.me.insert_one(**{
            "key_collection"
            : "other",
            "document"
            : {
                "id_doc"
                : id_doc,
                "data"
                : {
                    k
                    : v
                    for k, v
                    in  self.dict_data["test"].items()
                    if not isinstance(v, np.ndarray)
                },
                "d2a_pred"
                : [list(l) for l in self.d2a_pred], }, }) # type: ignore
        ### return #############################################################
        return self ############################################################
    ### haraimodoshi 1 #########################################################
    def update_dict_haraimodoshi(self, type_pred: str, ):
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.dict_haraimodoshi \
        = { self.dict_data[type_pred]["list_id_race"][i]
            : { "bet"
                : { str(j+1)
                    : 0
                    for j
                    in  range(18)}, # 最高で18頭立てまでなので
                "datetime"
                : self.dict_data[type_pred]["list_datetime"][i], }
            for i
            in  range(len(self.dict_pred["i1chaku"]))} # type: ignore
        for i in range(len(self.dict_pred["i1chaku"])): # type: ignore
            id_race: str \
            = self.dict_data["test"]["list_id_race"][i]
            for j in range(len(self.dict_pred["i1chaku"][i])): # type: ignore
                umaban : str \
                = str(self.dict_data["test"]["list_list_umaban"][i][j])
                self.dict_haraimodoshi[id_race]["bet"][umaban] \
                += int(self.dict_pred["i1chaku"][i][j] * 100) # type: ignore
        for id_race in self.dict_haraimodoshi:
            res \
                = self.me.find_one(**{
                    "key_collection": "race",
                    "filter"        : {
                        "id_race"   : id_race, }, })
            if res is None:
                raise Exception("document isn't founded")
            self.dict_haraimodoshi[id_race]["haraimodoshi"] \
                = { umaban:
                           haraimodoshi
                        *  self.dict_haraimodoshi[id_race]["bet"][umaban]
                    for umaban, haraimodoshi
                    in  res["haraimodoshi"]["単勝"].items()}
            self.dict_haraimodoshi[id_race]["sum_bet"] \
                = sum(self.dict_haraimodoshi[id_race]["bet"].values()) * 100
        ### return #############################################################
        return self ############################################################
    ### haraimodoshi 2 #########################################################
    def set_d1a_argmax(self, ):
        """
        10
        --"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.d1a \
        = np.argmax(self.d2a_pred, axis=1, )
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def init_dict_haraimodoshi(self, type_pred: str, ):
        """
        11
        --"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.dict_haraimodoshi \
        = { self.dict_data[type_pred]["list_id_race"][i]
            : { "bet"
                : { str(j+1)
                    : 0
                    for j
                    in  range(18)}, # 最高で18頭立てまでなので
                "datetime"
                : self.dict_data[type_pred]["list_datetime"][i], }
            for i
            in  range(len(self.d1a))}
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def set_dict_haraimodoshi(self, ):
        """
        12
        --"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        for i in range(len(self.d1a)):
            id_race: str \
            = self.dict_data["test"]["list_id_race"][i]
            umaban : str \
            = str(self.dict_data["test"]["list_list_umaban"][i][self.d1a[i]])
            self.dict_haraimodoshi[id_race]["bet"][umaban] \
            += 1 # bet
        for id_race in self.dict_haraimodoshi:
            res \
                = self.me.find_one(**{
                    "key_collection": "race",
                    "filter"        : {
                        "id_race"   : id_race, }, })
            if res is None:
                raise Exception("document isn't founded")
            self.dict_haraimodoshi[id_race]["haraimodoshi"] \
                = { umaban:
                           haraimodoshi
                        *  self.dict_haraimodoshi[id_race]["bet"][umaban]
                    for umaban, haraimodoshi
                    in  res["haraimodoshi"]["単勝"].items()}
            self.dict_haraimodoshi[id_race]["sum_bet"] \
                = sum(self.dict_haraimodoshi[id_race]["bet"].values()) * 100
        ### return #############################################################
        return self ############################################################
    # ############################################################################
    # def save_dict_haraimodoshi(self, ):
    #     ### print ##############################################################
    #     print("[IN save_dict_haraimodoshi() IN Fukamaru3]") ####################
    #     ########################################################################
    #     self.bangirasu.dump_pkl(**{
    #         "dir_file"
    #         : self.path_pkl_haraimodoshi,
    #         "obj"
    #         : self.dict_haraimodoshi, })
    #     ### print ##############################################################
    #     return self ############################################################
    ############################################################################
    def print_dict_haraimodoshi(self, ):
        """
        13
        --"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        l = [
            {k1: v1 for k1, v1 in v0.items()} | {"id_race": k0}
            for k0, v0 in self.dict_haraimodoshi.items()]
        l = sorted(l, key=lambda v: v["datetime"])
        for v in l:
            print(f'datetime: {v["datetime"]} - id_race: {v["id_race"]}')
            print(f'    count           : {v["bet"]}')
            print(f'    sum_bet         : {v["sum_bet"]}')
            print(f'    haraimodoshi    : {v["haraimodoshi"]}')
        sum_sum_bet \
            = sum([v["sum_bet"] for v in l])
        sum_sum_haraimodoshi \
            = sum([v1 for v0 in l for v1 in v0["haraimodoshi"].values()])
        count_hit \
            = sum([
                1
                for v0 in l
                if  sum(v0["haraimodoshi"].values()) != 0])
        count_hit_plus \
            = sum([
                1
                for v0 in l
                if  v0["sum_bet"] <= sum(v0["haraimodoshi"].values())])
        print(f'投票レース数        : {len(l)}')
        print(f'的中レース数        : {count_hit}')
        print(f'的中レース率        : {count_hit / len(l)}')
        print(f'的中レース数(+のみ) : {count_hit_plus}')
        print(f'的中レース率(+のみ) : {count_hit_plus / len(l)}')
        print(f'sum_sum_bet         : {sum_sum_bet}')
        print(f'sum_sum_haraimodoshi: {sum_sum_haraimodoshi}')
        print(f'回収率              : {sum_sum_haraimodoshi / sum_sum_bet}')
        ### return #############################################################
        return self ############################################################
    ############################################################################
