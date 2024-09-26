import const

class Komoru:
    #
    def verify_list_id_race_prod(self, list_id_race_prod: list[str], ):
        if list_id_race_prod == []:
            return
        for id_race in list_id_race_prod:
            if len(id_race) != 12:
                raise Exception(
                    "[IN Komoru] "
                    f"{id_race} <- id_race の長さが 12 ではありません。")
        return
    #
    def verify_list_filter_race(self,
    list_filter_race
    : list[dict[str, int]],
    ):
        if list_filter_race == []:
            return
        for filter in list_filter_race:
            if (set(filter.keys())
            != {"baba", "calc.tousu", "keibajo", "kyori", "kyoso", }):
            # != {"calc.tousu", "keibajo", "kyori", "kyoso", }):
                raise Exception(
                    "[IN Komoru] "
                    f"{set(filter.keys())} <- filter の key が一致しません。")
        return

class Bomanda(Komoru):
    def __init__(self) -> None:
        self.uri_mongodb,     self.name_db,  self.dict_name_collection, \
        = const.URI_MONGODB, const.NAME_DB, const.DICT_NAME_COLLECTION,
        self.type_rating,     self.nen,  self.tsuki,  self.hi, \
        = const.TYPE_RATING, const.NEN, const.TSUKI, const.HI,
            # self.list_d1a_y \
            # = const.LIST_D1A_Y
        self.list_dict_to_create_model \
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
        = const.LIST_DICT_TO_CREATE_MODEL
        # 各要素を sort し、tuple に変換する。その後、set で重複 tuple を削除し、
        # list に戻し、最後に全体を sort する。
        self.list_tuple_key \
        = sorted(list(set(
                tuple(sorted(list_key))
            for list_key
            in  const.LIST_LIST_KEY)))
        #
        self.list_id_race_prod: list[str] \
        = const.LIST_ID_RACE_PROD
        self.verify_list_id_race_prod(self.list_id_race_prod)
        #
        self.list_filter_race: list[dict[str, int]] \
        = const.LIST_FILTER_RACE
        ### verify #############################################################
        self.verify_list_filter_race(self.list_filter_race) ####################
        ########################################################################
        #
        self.dir_pkl_model \
        = const.DIR_PKL_MODEL
        #
        self.min_len_list_dict_race \
        = const.MIN_LEN_LIST_DICT_RACE
        return
