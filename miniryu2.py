import itertools
from scipy import stats
import trueskill

import bomanda
import bangirasu
import metagurosu
################################################################################
class Miniryu2(bangirasu.Bangirasu):
    ############################################################################
    def __init__(self,
    dict_race
    : dict,
    tuple_key
    : tuple[str, ...],
    str_tuple_key
    : str,
    bo
    : bomanda.Bomanda,
    ) -> None:
        ### print ##############################################################
        self.cprint(dict_race["datetime"], loop=True, ) ########################
        ########################################################################
        self.datetime,                 self.id_race \
        = dict_race["datetime"], dict_race["id_race"],                      # 21!!
        self.dict_race \
        = dict_race
        self.tuple_key \
        = tuple_key
        self.str_tuple_key \
        = str_tuple_key
        self.dict_list \
        = { "list_str_tuple_value"
            : [],
            "list_list_chakujun"
            : [], }                                                         #!!!!!
        self.env \
        = trueskill.TrueSkill()                                             # 03
        self.me: metagurosu.Metagurosu \
        =    metagurosu.Metagurosu(bo=bo, )                                 # !!!!
        ### return #############################################################
        return #################################################################
    ############################################################################
    def create_index(self, ):
        self.me.create_index(**{
            "key_collection"
            : "rating",
            "keys"
            : [ ("str_tuple_key",    1, ), # この行がないと再計算時の日付が取得できない
                ("str_tuple_value",  1, ),
                ("datetime",        -1, ),
                ("id_race",         -1, ), ],
            "unique"
            : True, })
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def filter_list_horse(self, ):
        """
        出走していない (= 人気が None) の馬のデータを除外"""
        self.dict_race["list_horse"] \
        = [     dict_horse
            for dict_horse
            in  self.dict_race["list_horse"]
            if  dict_horse["ninki"] is not None]
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def update_dict_list_0(self, ):
        """
        After: filter_list_horse()
        --------------------------
        list_tuple_value, list_list_chakujun を追加。"""
        dict_dict_team = {}                                                 # 30
        for i, dict_horse \
        in  enumerate(self.dict_race["list_horse"]):                        # 93
            str_tuple_value \
            = str(tuple(
                self.get_value(**{
                    "index"
                    : i,
                    "dict_race"
                    : self.dict_race,
                    "key"
                    : key, })
                for key
                in  self.tuple_key))                                        # 65
            if str_tuple_value not in dict_dict_team:                       # 96
                dict_dict_team[str_tuple_value] \
                = { "list_chakujun"
                    : [], }                                                 # 51
            dict_dict_team[str_tuple_value]["list_chakujun"].append(
                     20
                if   dict_horse["chakujun"] is None
                else dict_horse["chakujun"])                                # 89
        for str_tuple_value, dict_team \
        in  dict_dict_team.items():
            self.dict_list["list_str_tuple_value"].append(str_tuple_value)
            self.dict_list["list_list_chakujun"].append(dict_team["list_chakujun"])
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def update_dict_list_1(self, ):
        """
        After: update_dict_list_0()
        ---------------------------
        list_rating_{tr}_old を追加。"""
        for type_rating in ["race", "day", ]:
            self.dict_list[f"list_rating_{type_rating}_old"] \
            = [ (self.get_rating(**{
                    "str_tuple_value"
                    : str_tuple_value,
                    "type_rating"
                    : type_rating, }), )
                for str_tuple_value
                in  self.dict_list["list_str_tuple_value"]]
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def get_rating(self, str_tuple_value: tuple, type_rating: str, ):
        filter \
        = { "str_tuple_key"
            : self.str_tuple_key,
            "str_tuple_value"
            : str_tuple_value, }
        if type_rating == "day":
            filter["datetime"] \
            = { "$not"
                : { "$regex"
                    : f"^{self.datetime[0:8]}", }, } # day の場合は、当日以外の最新から取得
        res \
        = self.me.find_one(**{
            "key_collection"
            : "rating",
            "filter"
            : filter,
            "projection"
            : { "rating.race.new"
                : 1 , },
            "sort"
            : [ ("datetime", -1, ), # -1: 降順
                ("id_race",  -1, ), ], }) # race と day で取得箇所が異なる
        if res is None:
            return self.env.create_rating()
        ### return #############################################################
        return self.env.create_rating(**{
            "mu"
            : res["rating"]["race"]["new"]["mu"], # day の new は使う機会ない
            "sigma"
            : res["rating"]["race"]["new"]["sigma"], }) # day の new は使う機会ない
    ############################################################################
    def update_dict_list_2(self, ):
        """
        After: update_dict_list_1()
        ---------------------------
        list_point を追加。"""
        self.dict_list["list_point"] \
        = [ - sum([
                 1     # team win
            if   v > 0
            else -1    # team lose
            if   v < 0
            else 0     # team draw
            for  v
            in   [
                sum([
                         1           # win
                    if   t[0] < t[1]
                    else -1          # lose
                    if   t[0] > t[1]
                    else 0           # draw
                    for  t
                    in   list(
                        itertools.product(
                            list_chakujun_0,
                            list_chakujun_1, ))])
                for i_1, list_chakujun_1
                in  enumerate(self.dict_list["list_list_chakujun"])
                if  i_0 != i_1]])
            for i_0, list_chakujun_0
            in  enumerate(self.dict_list["list_list_chakujun"])]
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def update_dict_list_3(self, ):
        """
        After: update_dict_list_2()
        ---------------------------
        ranks を追加。"""
        self.dict_list["ranks"] \
        = [     rank - 1
            for rank
            in  stats.rankdata(self.dict_list["list_point"], "min")]
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def update_dict_list_4(self, ):
        """
        After: update_dict_list_3()
        ---------------------------
        list_rating_{tr}_new を追加。"""
        for type_rating in ["race", "day", ]:
            self.dict_list[f"list_rating_{type_rating}_new"] \
            =        self.env.rate(**{
                        "rating_groups"
                        : self.dict_list[f"list_rating_{type_rating}_old"],
                        "ranks"
                        : self.dict_list["ranks"], })  \
                if   len(self.dict_list["ranks"]) != 1 \
                else self.dict_list[f"list_rating_{type_rating}_old"]
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def insert_documents_to_rating(self, ):
        """
        After: update_dict_list_4()
        ---------------------------
        collection: rating に insert。"""
        self.me.insert_many(
            key_collection=
                "rating",
            documents=
                [
                    {
                        "str_tuple_key"
                        : self.str_tuple_key,
                        "str_tuple_value"
                        : self.dict_list["list_str_tuple_value"][i],
                        "id_race"
                        : self.id_race,
                        "datetime"
                        : self.datetime,
                        "rating": {
                            type_rating
                            : { on
                                : { "mu"
                                    : self.dict_list[f"list_rating_{type_rating}_{on}"][i][0].mu,
                                    "sigma"
                                    : self.dict_list[f"list_rating_{type_rating}_{on}"][i][0].sigma, }
                                for on
                                in  ["old", "new", ] }
                            for type_rating
                            in  ["race", "day", ]}, }
                    for i
                    in  range(len(self.dict_list["ranks"]))
                ],
        )
        # for i in range(len(self.dict_list["ranks"])):
        #     document \
        #     = { "str_tuple_key"
        #         : self.str_tuple_key,
        #         "str_tuple_value"
        #         : self.dict_list["list_str_tuple_value"][i],
        #         "id_race"
        #         : self.id_race,
        #         "datetime"
        #         : self.datetime,
        #         "rating": {
        #             type_rating
        #             : { on
        #                 : { "mu"
        #                     : self.dict_list[f"list_rating_{type_rating}_{on}"][i][0].mu,
        #                     "sigma"
        #                     : self.dict_list[f"list_rating_{type_rating}_{on}"][i][0].sigma, }
        #                 for on
        #                 in  ["old", "new", ] }
        #             for type_rating
        #             in  ["race", "day", ]}, }
        #     self.me.insert_one(**{
        #         "key_collection"
        #         : "rating",
        #         "document"
        #         : document, })
        ### return #############################################################
        return #################################################################
    ############################################################################
