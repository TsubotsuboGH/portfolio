import bomanda
import bangirasu
import metagurosu
################################################################################
class Waza(bangirasu.Bangirasu):
    ############################################################################
    def get_dict_race_trimmed(
    self,
    dict_race
    : dict,
    new
    : bool,
    bo
    : bomanda.Bomanda,
    me
    : metagurosu.Metagurosu,
    ) -> dict:
        ### print ##############################################################
        self.cprint(dict_race["datetime"], loop=True, ) ########################
        ########################################################################
        return {
            "id_race"
            : dict_race["id_race"],
            "datetime"
            : dict_race["datetime"],
            "list_dict_horse"
            : sorted([{
                "umaban"
                : dict_horse["umaban"],
                "chakujun"
                : dict_horse["chakujun"],
                "ninki"
                : dict_horse["ninki"],
                "x10tansho"
                : dict_horse["x10tansho"],
                "x10time"
                : dict_horse["x10time"],
                "shijiritsu"
                : dict_horse["calc"]["shijiritsu"],
                "rating"
                : [ self.calc_rating(**{
                        "dict_rating"
                        : me.find_one(**{
                            "key_collection"
                            : "rating",
                            "filter"
                            : { "str_tuple_key"
                                : str(tuple_key),
                                "str_tuple_value"
                                : str(tuple(
                                        self.get_value(dict_race, i, key)
                                    for key
                                    in  tuple_key)), }
                            |({}
                            if new
                            else
                              { "id_race"
                                : dict_race["id_race"], }), }),
                        "type_rating"
                        : bo.type_rating,
                        "new"
                        : new, })
                    for tuple_key
                    in  bo.list_tuple_key]
                }
                for i, dict_horse
                in  enumerate(dict_race["list_horse"])
                if  dict_horse["ninki"] is not None], key=lambda d: d["umaban"]), }
################################################################################
class Fukamaru2(Waza):
    ############################################################################
    def __init__(self,
    filter_race
    : dict[str, int],
    bo
    : bomanda.Bomanda,
    ) -> None:
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.bo \
        =    bomanda.Bomanda()
        self.me, \
        =    metagurosu.Metagurosu(bo=bo, ),                                # !!!!
        self.filter_race \
        = filter_race
        self.tousu \
        = filter_race["calc.tousu"]
        self.makedirs(dir=self.bo.dir_pkl_model, exist_ok=True, )
        ### return #############################################################
        return #################################################################
    ############################################################################
    def set_datetime_latest_in_race(self, ):
        """
        1a
        --"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        res \
        = self.me.find_one(**{
            "key_collection"
            : "race",
            "filter"
            : self.filter_race,
            "sort"
            : [ ("datetime", -1, ), ], })
        if res is None:
            self.datetime_latest_in_race \
            = None
        else:
            self.datetime_latest_in_race \
            = res["datetime"]
        ### cprint #############################################################
        self.cprint(self.datetime_latest_in_race, ) ############################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def set_datetime_in_model(self, ):
        """
        1b
        --"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        res \
        = self.me.find_one(**{
            "key_collection"
            : "model",
            "filter"
            : { "filter_race"
                : self.filter_race, }, })
        if res is None:
            self.datetime_in_model \
            = None
        else:
            self.datetime_in_model \
            = res["datetime"]
        ### cprint #############################################################
        self.cprint(self.datetime_in_model, ) ##################################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def should_update_model(self, ) -> bool:
        """
        2
        -"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        if self.datetime_latest_in_race is None:
            ### Exception ######################################################
            self.raise_exception( ##############################################
                msg="過去データが存在しないため、model を作成できません。", ) ##
            ####################################################################
        if self.datetime_in_model is None:
            ### print ##########################################################
            self.cprint(msg="model が存在しません。model を作成します。") ######
            ### return #########################################################
            return True ########################################################
            ####################################################################
        if self.datetime_latest_in_race  < self.datetime_in_model:
            ### Exception ######################################################
            self.raise_exception( ##############################################
                msg="datetime_latest_in_model の方が大きいです。" ##############
                    "何かしらの不整合が発生しています。", ) ####################
        if self.datetime_latest_in_race == self.datetime_in_model:
            ### print ##########################################################
            self.cprint(msg="model は最新です。") ##############################
            ### return #########################################################
            return False #######################################################
            ####################################################################
        else:
            ### print ##########################################################
            self.cprint(msg="datetime_latest_in_model の方が小さいです。" ######
                            "model のアップデートを開始します。") ##############
            ### return #########################################################
            return True ########################################################
    ############################################################################
    def set_iter_dict_race(self, ):
        """
        3a-0
        ----"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.iter_dict_race \
        = self.me.find(**{
            "key_collection"
            : "race",
            "filter"
            : self.filter_race,
            "sort"
            : [ ("datetime", 1, ), ], })#.limit(1000)
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def set_list_dict_race(self, ):
        """
        3a-1
        ----
        00. SET
        +-- self.list_dict_race
        +-- 01. self.res を dict_race として loop する。
            02. keibajo と kyoso が一致する dict_race のみ抽出する。
            03. dict_race["list_horse"] を dict_horse として loop する。
            04. 必要な情報のみを抽出する。
            05. umaban で sort する。
        01. DELETE
        +-- self.res"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.me.create_index(**{
            "key_collection"
            : "rating",
            "keys"
            : [ ("str_tuple_key",   1, ),
                ("str_tuple_value", 1, ),
                ("id_race",         1, ), ],
            "unique"
            : True, })
        self.list_dict_race \
        = [ self.get_dict_race_trimmed(
                dict_race=
                    dict_race,
                new=False,
                bo =self.bo,
                me =self.me, )
            for dict_race
            in  self.iter_dict_race]                                        # 00
        ### cprint #############################################################
        self.cprint(len(self.list_dict_race), ) ################################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def can_split(self, ) -> bool:
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        if len(self.list_dict_race) <= self.bo.min_len_list_dict_race:
            ### return #########################################################
            return False #######################################################
            ####################################################################
        else:
            ### return #########################################################
            return True ########################################################
    ############################################################################
    def del_iter_dict_race(self, ):
        """
        3a-2a
        -----"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        del self.iter_dict_race                                             # 01
        ### return #############################################################
        return self ############################################################
    # list_horse.rating を消したら削除予定 #####################################
    def verify_rating(self):
        for dict_race in self.iter_dict_race:
            print(dict_race["id_race"])
            for i, dict_horse in enumerate(dict_race["list_horse"]):
                if "rating" not in dict_horse:
                    continue
                for dict_rating in dict_horse["rating"]:
                    tuple_key = []
                    for list_key in dict_rating["list_list_key"]:
                        if "list_horse" in list_key:
                            tuple_key.append(list_key[0] + ".$." + ".".join(list_key[1:]))
                        else:
                            tuple_key.append(".".join(list_key))
                    r = self.me.find_one(
                        key_collection="rating",
                        filter={
                            "str_tuple_key": str(tuple(tuple_key)),
                            "str_tuple_value": str(tuple(self.get_value(dict_race, i, key) for key in tuple_key)),
                            "id_race": dict_race["id_race"],
                            "datetime": dict_race["datetime"],
                        })
                    if r is None:
                        raise Exception("None")
                    for r0, r1 in zip(r["rating"].values(), dict_rating["rating"].values()):
                        for ti in ["old", "new"]:
                            for ty in ["mu", "sigma"]:
                                if str(r0[ti][ty])[:10] != str(r1[ti][ty])[:10]:
                                    raise Exception("not equal")
                    # dict_rating["rating"]["a"] = "b"
                    # b = r["rating"] == dict_rating["rating"]
                    # if not b:
                    #     self.pprint(r["rating"])
                    #     self.pprint(dict_rating["rating"])
                    #     raise Exception("not equal")
                    # self.pprint(r["rating"])
                    # self.pprint(dict_rating["rating"])
                    # raise Exception
                # self.pprint(dict_horse)
                # raise Exception
        raise Exception("complete")
    ############################################################################
