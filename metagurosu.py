import math
import pymongo
from   pymongo            import MongoClient
from   pymongo.database   import Database    # 型ヒント用
from   pymongo.collection import Collection  # 型ヒント用

import bomanda

class Metagurosu:
    """const から諸々設定する機能と、MongoDB関連の機能を持つモジュール"""
    #
    def __init__(self, bo: bomanda.Bomanda, ) -> None:
        self.client             : MongoClient \
        = MongoClient(bo.uri_mongodb)
        self.db                 : Database    \
        = self.client[bo.name_db]
        self.dict_collection    : dict[str, Collection] \
        = { key:
                self.db[value]
            for key, value
            in  bo.dict_name_collection.items()}
        return
    # # collection: race に rating を追加しなくなったので、削除予定
    # def sort_rating(self) -> None:
    #     res \
    #         = self.find(**{
    #             "key_collection": "race",
    #             "filter"        : {}, })
    #     list_list_list_key \
    #         = [
    #                 d["list_list_key"]
    #             for d
    #             in  res[0]["list_horse"][0]["rating"]] # サンプルを1個取得
    #     list_index \
    #         = [
    #                 list_list_list_key.index(list_list_key)
    #             for list_list_key
    #             in  self.l_l_l_key]
    #     del list_list_list_key # もう使わない
    #     for dict_race in res:
    #         print("\r" + dict_race["datetime"], end="")
    #         for d_h in dict_race["list_horse"]:
    #             if "rating" not in d_h:
    #                 continue
    #             if self.l_l_l_key==[d["list_list_key"] for d in d_h["rating"]]:
    #                 continue
    #             list_dict_rating = [
    #                      d_h["rating"][index]
    #                 if   d_h["rating"][index]["list_list_key"] == list_list_key
    #                 else False
    #                 for  index, list_list_key
    #                 in   zip(list_index, self.l_l_l_key)]
    #             if False in list_dict_rating:
    #                 raise Exception(dict_race["id_race"])
    #             self.set_value(**{
    #                 "name_collection": "race",
    #                 "filter"         : {
    #                     "id_race": dict_race["id_race"], },
    #                 "update"         : {
    #                     "list_horse.$[elem].rating": list_dict_rating, },
    #                 "array_filters"  : [
    #                     {
    #                         "elem.id_horse": d_h["id_horse"], }, ], })
    #     return
    #
    def count_document(
        self,
        key_collection: str,
        filter        : dict, ):
        return self.dict_collection[key_collection].count_documents(**{
            "filter": filter, })
    #
    def find_one(
        self,
        key_collection: str,
        filter        : dict,
        projection    : dict        | None=None,
        sort          : list[tuple] | None=None, ) -> dict | None:
        return self.dict_collection[key_collection].find_one(**{
            "filter"    : filter,
            "projection": projection,
            "sort"      : sort, })
    #
    def find(
        self,
        key_collection: str,
        filter        : dict,
        projection    : dict        | None=None,
        sort          : list[tuple] | None=None, ):
        return self.dict_collection[key_collection].find(**{
            "filter"    : filter,
            "projection": projection,
            "sort"      : sort, })
    # document を insert
    def insert_one(
        self,
        key_collection: str,
        document      : dict, ) -> None:
        self.dict_collection[key_collection].insert_one(document)
        return
    #
    def insert_many(self,
    key_collection: str,
    documents     : list[dict],
    ) -> None:
        self.dict_collection[key_collection].insert_many(documents=documents)
        return
    #
    def update_one(
        self,
        key_collection,
        filter,
        update,
        array_filters = None, ) -> None:
        self.dict_collection[key_collection].update_one(**{
            "filter"       : filter,
            "update"       : update,
            "array_filters": array_filters, })
        return
    #
    def delete_one(
        self,
        key_collection: str,
        filter        : dict, ) -> None:
        self.dict_collection[key_collection].delete_one(**{
            "filter": filter, })
        return
    #
    def set_value(
        self,
        name_collection: str,
        filter         : dict,
        update         : dict, 
        array_filters  : list | None = None, ) -> None:
        self.dict_collection[name_collection].update_one(
            filter=filter,
            update={"$set": update, },
            array_filters=array_filters, ) # update_one
        return
    # index を作成
    def create_index(self, key_collection, keys, unique=False, ) -> None:
        self.dict_collection[key_collection].create_index(**{
            "keys"  : keys,
            "unique": unique, })
        return
    #
    def get_path_pkl(
        self,
        list_tuple_key: list[tuple[str, ...]], ) -> str | None:
        res \
        = self.find_one(**{
            "key_collection"
            : "dir_file",
            "filter"
            : list_tuple_key, })
        if res is None:
            return None
        return res["path_pkl"]
    #
    def del_rating(self) -> None:
        if input("WARNING: 本当に rating を削除しますか？") != "y":
            print("削除しませんでした。")
            return
        self.dict_collection["race"].update_many(**{
            "filter": {
                # "id_race"          : "200006010101",
                "list_horse.rating": {
                    "$exists"      : 1, }, },
            "update": {
                "$unset": {
                    "list_horse.$[].rating": "", }, }, }) # [] は必須。list_horse内の全ての要素を表す。
        self.dict_collection["dir_file"].drop()
        print("[collection] dir_file, [value] list_horse.$[].rating を削除しました。")
        return
    #
    def del_rating_0(self, ):
        self.dict_collection["rating"].delete_many(**{
            "filter": {
                "tuple_tuple_key": [["kyoso"], ["list_horse", "id_horse"]], }, })
        return
    """### 取消・除外「後」の頭数 ###########################################"""
    def calc_tousu(self):
        res \
        = self.find(**{
            "key_collection"
            : "race",
            "filter"
            : { "calc.tousu"
                : { "$exists"
                    : 0, }, }, # 計算の必要なし
            "projection"
            : { "datetime"        : 1,
                "id_race"         : 1,
                "list_horse.ninki": 1, }, })#.limit(10000)
        for dict_race in res:
            print(f'\r{dict_race["datetime"]} [in calc_tousu()]', end="", )
            tousu \
            = sum([
                    1
                for dict_horse
                in  dict_race["list_horse"]
                if  dict_horse["ninki"] is not None])
            self.update_one(**{
                "key_collection"
                : "race",
                "filter"
                : { "id_race"
                    : dict_race["id_race"], },
                "update"
                : { "$set"
                    : { "calc.tousu"
                        : tousu, }, }, })
        print("\n[in calc_tousu in Metagurosu] calculated: tousu")
        return self
    """### 数え年の馬齢を満年齢に変更 #######################################"""
    def calc_mannenrei(self):
        """
        rei を満年齢に変換し、list_horse.[].calc.mannenrei にセット
        クエリで確認した結果、2 ~ 15 以外の値は存在しなかった。"""
        res \
        = self.find(**{
            "key_collection"
            : "race",
            "filter"
            : { "list_horse.calc.mannenrei"
                : { "$exists"
                    : 0, }, },
            "projection"
            : { "datetime"
                : 1,
                "id_race"
                : 1,
                "nen"
                : 1,
                "list_horse.id_horse"
                : 1,
                "list_horse.rei"
                : 1, }, })#.limit(10000)
        for dict_race in res:
            print(f'\r{dict_race["datetime"]} [in calc_mannenrei()]', end="", )
            for dict_horse in dict_race["list_horse"]:
                if dict_race["nen"] <= 2000:
                    mannenrei = dict_horse["rei"] - 1
                else:
                    mannenrei = dict_horse["rei"]
                self.update_one(**{
                    "key_collection"
                    : "race",
                    "filter"
                    : { "id_race"
                        : dict_race["id_race"],
                        "list_horse.id_horse"
                        : dict_horse["id_horse"], },
                    "update"
                    : { "$set"
                        : { "list_horse.$.calc.mannenrei"
                            : mannenrei, }, }, })
        print("\n[in calc_mannenrei in Metagurosu] calculated: mannenrei")
        return self
    """### 支持率を計算 #####################################################"""
    def calc_shijiritsu(self) -> None:
        """
        単勝オッズを単勝支持率に変換し、
        list_horse.[].calc.shijiritsu にセット
        list_horse.calc は、計算を skip する際の確認に使用。
        list_horse.ninki は、x10tansho が存在するかの判定に使用。"""
        res \
        = self.find(**{
            "key_collection"
            : "race",
            "filter"
            : { "list_horse.calc.shijiritsu"
                : { "$exists"
                    : 0, }, },
            "projection"
            : { "id_race"
                : 1,
                "list_horse.id_horse"
                : 1,
                "list_horse.x10tansho"
                : 1,
                "list_horse.ninki" # None の確認に使用
                : 1, }, })#.limit(1)
        for dict_race in res:
            print(f'\r{dict_race["id_race"]} [in calc_shijiritsu()]', end="", )
            list_dict_horse \
            = [     dict_horse
                for dict_horse
                in  dict_race["list_horse"]
                if  dict_horse["ninki"] is not None]
            list_x10tansho \
            = [     dict_horse["x10tansho"]
                for dict_horse
                in  list_dict_horse]
            # print(f"\n{list_x10tansho}")
            # e_prod = excepted product (e(x) = x 番を除いた総積)
            # 以下のやり方だと、支持率の合計値が 0.[9*15]6 <-> 1.[0*15]4 以内に収まる
            list_e_prod \
            = [     math.prod(list_x10tansho[:i] + list_x10tansho[i+1:])
                for i
                in  range(len(list_x10tansho))]
            sum_list_e_prod \
            = sum(list_e_prod)
            list_shijiritsu \
            = [     list_e_prod[i] / sum_list_e_prod
                for i
                in  range(len(list_x10tansho))]
            for shijiritsu, dict_horse \
            in  zip(list_shijiritsu, list_dict_horse):
                # print(f'{shijiritsu} - {dict_horse["x10tansho"]} - {dict_horse["id_horse"]}')
                self.update_one(**{
                    "key_collection"
                    : "race",
                    "filter"
                    : { "id_race"
                        : dict_race["id_race"],
                        "list_horse.id_horse"
                        : dict_horse["id_horse"], },
                    "update"
                    : { "$set"
                        : { "list_horse.$.calc.shijiritsu"
                            : shijiritsu, }, }, })
        return
    # """### 取消・除外のゲートを「外枠」側に詰める ###########################"""
    # def calc_umaban_o(self) -> None:
    #     res = self.find(**{
    #         "key_collection": "race",
    #         "filter"        : {},
    #         "projection"    : {
    #             "datetime"            : 1,
    #             "id_race"             : 1,
    #             "list_horse.id_horse" : 1,
    #             "list_horse.umaban"   : 1,
    #             "list_horse.ninki"    : 1,
    #             # 計算を skip する際の確認に使用
    #             "list_horse.calc"     : 1, },
    #         })#.limit(10000)
    #     for dict_race in res:
    #         print(f'\r{dict_race["datetime"]} [in calc_umaban_o()]', end="", )
    #         for dict_horse in dict_race["list_horse"]:
    #             if "calc" in dict_horse and "mannenrei" in dict_horse["calc"]:
    #                 continue # 既に登録済み
    #             if dict_race["nen"] <= 2000:
    #                 mannenrei = dict_horse["rei"] - 1
    #             else:
    #                 mannenrei = dict_horse["rei"]
    #             self.update_one(**{
    #                 "key_collection": "race",
    #                 "filter"        : {
    #                     "id_race"            : dict_race["id_race"],
    #                     "list_horse.id_horse": dict_horse["id_horse"], },
    #                 "update"        : {
    #                     "$set": {
    #                         "list_horse.$.calc.mannenrei": mannenrei, }, }, })
