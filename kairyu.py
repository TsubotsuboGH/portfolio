import bomanda
import metagurosu
import bangirasu
import miniryu1
################################################################################
class Kairyu(bangirasu.Bangirasu):
    ############################################################################
    def __init__(self, ) -> None:
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.bo: bomanda.Bomanda \
        =    bomanda.Bomanda()
        self.me: metagurosu.Metagurosu \
        =    metagurosu.Metagurosu(bo=self.bo, )
        self.me.create_index(**{
            "key_collection"
            : "race",
            "keys"
            : [ ("datetime",        1, ),
                ("id_race",         1, ), ],
            "unique"
            : True, }) # miniryu1 > Miniryu1 > set_iter_dict_race() 用
        for              tuple_key \
        in  self.bo.list_tuple_key:
            (miniryu1.Miniryu1(
                tuple_key=
                    tuple_key,
                bo= self.bo, )
            .check_existence_of_value()
            .set_iter_dict_race()
            .loop_iter_dict_race())
        ### return #############################################################
        return #################################################################
    ############################################################################
    def test(self, ):
        """
        rating を race に追加する関数"""
        for tuple_key in self.bo.list_tuple_key:
            str_tuple_key \
            = str(tuple_key)
            list_dict_race \
            = self.me.find(**{
                "key_collection"
                : "race",
                "filter"
                : { "list_horse.rating.{}".format(str_tuple_key)
                    : { "$exists"
                        : 0, }, },
                "sort"
                : [ ("datetime", 1, ), ], })
            print(str_tuple_key)
            for dict_race in list_dict_race:
                print("\r" + dict_race["datetime"], end="", )
                for i, dict_horse in enumerate(dict_race["list_horse"]):
                    if dict_horse["ninki"] is None:
                        continue
                    str_tuple_value \
                    = str(tuple(self.get_value(dict_race, i, key)
                        for key
                        in  tuple_key))
                    src_rating \
                    = self.me.find_one(**{
                        "key_collection"
                        : "rating",
                        "filter"
                        : { "str_tuple_key"
                            : str(tuple_key),
                            "str_tuple_value"
                            : str_tuple_value,
                            "id_race"
                            : dict_race["id_race"], }, })
                    if src_rating is None:
                        raise Exception("rating が存在しません。")
                    self.me.update_one(**{
                        "key_collection"
                        : "race",
                        "filter"
                        : { "id_race"
                            : dict_race["id_race"], },
                        "update"
                        : { "$set"
                            : { "list_horse.$[elem].rating"
                                : {str_tuple_key: src_rating["rating"], }, }, }, 
                        "array_filters"
                        : [ {   "elem.id_horse"
                                : dict_horse["id_horse"], }, ], })
        ### return #############################################################
        return #################################################################
    ############################################################################
