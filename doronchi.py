import bs4
import re
import requests

import bangirasu
import bomanda
################################################################################
class Doronchi(bangirasu.Bangirasu):
    ############################################################################
    def __init__(self, id_race: str, bo: bomanda.Bomanda) -> None:
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.bo: bomanda.Bomanda \
        =    bo
        self.id_race: str \
        = id_race
        ### return #############################################################
        return #################################################################
    ############################################################################
    def set_bs(self):
        """
        After: なし
        -----------"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        uri_race \
        = "https://race.netkeiba.com/race/shutuba.html?race_id=" \
        + f"{self.id_race}&rf=race_submenu"
        ### cprint #############################################################
        self.cprint(uri_race) ##################################################
        ########################################################################
        content \
        = requests.get(uri_race).content
        self.bs \
        = bs4.BeautifulSoup(content, "html.parser")
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def set_tousu(self):
        """
        After: set_bs()
        ---------------"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.tousu: int \
        = len(self.bs.select(".HorseList"))
        ### cprint #############################################################
        self.cprint(self.tousu) ################################################
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def set_dict_race(self):
        """
        After: set_tousu()
        ------------------"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        src \
        = self.bs.select_one(".RaceName")
        if src is None:
            raise Exception("error: racemei")
        racemei \
        = src.text.replace("\n", "")
        ### cprint #############################################################
        self.cprint(racemei) ###################################################
        ########################################################################
        src \
        = self.bs.select_one(".RaceData01")
        if src is None:
            raise Exception("error: kyoso")
        src \
        = src.text.replace(" ", "").replace("\n", "").split("/")
        kyoso \
        = ["芝", "ダ", "障", ].index(src[1][0])
        kyori \
        = int(re.sub(r"\D", "", src[1]))
        tenko \
        = ["晴", "曇", "雨", "小雨", "雪", "小雪", ].index(src[2][3:])
        baba \
        = ["良", "稍重", "重", "不良", ].index(src[3][3:])
        hasso \
        = int(src[0][:2]) * 60 + int(src[0][3:5])
        ### cprint #############################################################
        self.cprint(kyoso) #####################################################
        self.cprint(kyori) #####################################################
        self.cprint(tenko) #####################################################
        self.cprint(baba) ######################################################
        self.cprint(hasso) #####################################################
        ########################################################################
        keibajo: int \
        = int(self.id_race[4:6])
        kai    : int \
        = int(self.id_race[6:8])
        nichi  : int \
        = int(self.id_race[8:10])
        r      : int \
        = int(self.id_race[10:12])
        datetime \
        = "{ye}{mo}{da}{ho}{mi}".format(
            ye=str(self.bo.nen),
            mo=str(self.bo.tsuki).zfill(2),
            da=str(self.bo.hi).zfill(2),
            ho=str(hasso // 60).zfill(2),
            mi=str(hasso % 60).zfill(2), )
        ### cprint #############################################################
        self.cprint(keibajo) ###################################################
        self.cprint(kai) #######################################################
        self.cprint(nichi) #####################################################
        self.cprint(r) #########################################################
        self.cprint(datetime) ##################################################
        ########################################################################
        self.dict_race = {
            "list_horse"
            : [     DorameshiyaA(tag_tr=tag_tr)
                    .set_id_horse()
                    .set_dict_pedigree()
                    .get_dict_horse()
                for tag_tr
                in  self.bs.select(".HorseList")],
            "nen"     : self.bo.nen,
            "tsuki"   : self.bo.tsuki,
            "hi"      : self.bo.hi,
            "racemei" : racemei,
            "kyoso"   : kyoso,
            "kyori"   : kyori,
            "tenko"   : tenko,
            "baba"    : baba,
            "hasso"   : hasso,
            "keibajo" : keibajo,
            "kai"     : kai,
            "nichi"   : nichi,
            "r"       : r,
            "id_race" : self.id_race,
            "datetime": datetime,
            "calc"    : {
                "tousu": self.tousu, }, }
        return self
    #
    def del_bs(self, ):
        """
        After: set_dict_race()
        ----------------------"""
        print("[IN Doronchi 4a] del_bs()")
        del self.bs
        return self
    #
    def set_dict_model_and_p(self, ):
        """
        After: del_bs()
        ---------------"""
        print("[IN Doronchi 4b] set_dict_model_and_p()")
        filter \
        = { 
            "baba"
            : self.dict_race["baba"],
            "calc.tousu"
            : self.dict_race["calc"]["tousu"],
            "keibajo"
            : self.dict_race["keibajo"],
            "kyori"
            : self.dict_race["kyori"],
            "kyoso"
            : self.dict_race["kyoso"], }
        ### verify #############################################################
        self.verify_list_filter(list_filter=[filter])
        ########################################################################
        res \
        =   (Gabaito(**{
                "filter"
                : filter, })
            .set_res())
        if res is None:
            raise Exception("model が存在しません。")
        self.dict_model,        self.p, \
        = res.get_dict_model(), res.get_p()
        return self
    #
    def set_list_dict_race(self, ):
        """
        After: set_dict_model()
        ---------------"""
        print("[IN Doronchi 5] set_list_dict_race()")
        self.list_dict_race \
        = [ self.get_dict_race_trimmed(**{
                "dict_race"
                : self.dict_race,
                "new"
                : True, }), ]
        return self
    #
    def del_dict_race(self, ):
        """
        After: set_list_dict_race()
        ---------------------------"""
        print("[IN Doronchi 6a] del_dict_race()")
        del self.dict_race
        return self
    #
    def set_dict_list_dict_race(self, ):
        """
        After: del_dict_race()
        ----------------------"""
        print("[IN Doronchi 6b] set_dict_list_dict_race()")
        self.dict_list_dict_race \
        = { "prod"
            : self.list_dict_race, }
        return self
    #
    def del_list_dict_race(self, ):
        """
        After: set_dict_list_dict_race()
        --------------------------------"""
        print("[IN Doronchi 7] del_list_dict_race()")
        del self.list_dict_race
        return self
    #
    def set_umaban_to_buy(self, ):
        print("[IN Doraparuto] set_umaban_to_buy()")
        for i in range(len(self.d1a)):
            id_race: str \
            = self.dict_data["prod"]["list_id_race"][i]
            umaban : str \
            = str(self.dict_data["prod"]["list_list_umaban"][i][self.d1a[i]])
            self.dict_haraimodoshi[id_race]["bet"][umaban] \
            += 1 # bet
        self.pprint(self.dict_haraimodoshi)
    #
    # def append_rating_to_list_dict_race(self, ):
    #     """
    #     After: set_list_dict_race()
    #     ---------------------------"""
    #     for list_tuple_key in self.list_list_tuple_key:
    #         dict_detail \
    #         = self.get_path_pkl(list_tuple_key=list_tuple_key, )
    #         if dict_detail is None:
    #             raise Exception(
    #                 "dict_detail.pkl が存在しません "
    #                 "[in append_rating_to_list_dict_race in Doraparuto]")
    #         for i, dict_race in enumerate(self.list_dict_race):
    #             for j, dict_horse in enumerate(dict_race["list_dict_horse"]):
    #                 self.list_dict_race
    #                 # 以下工事中
    #                 pass
    #     return self
    ############################################################################
    def test(self, ):
        a = self.dict_data
        self.pprint(a)
    ############################################################################