class DorameshiyaA(ZiheddoB):
    #
    def __init__(self, tag_tr: bs4.Tag) -> None:
        self.list_tag_td \
        = tag_tr.select("td")
        return
    #
    def set_id_horse(self, ):        
        # id_horse #########################################################
        src \
        = self.list_tag_td[3].select_one("a")
        if src is None:
            raise Exception("error: id_horse")
        self.id_horse \
        = src.attrs["href"][-10:]
        return self
    #
    def set_dict_pedigree(self, ):
        self.dict_pedigree \
        = ZiheddoB(id_horse=self.id_horse).get_dict_ped()
        del self.dict_pedigree["id_horse"]
        return self
    #
    def get_dict_horse(self, ):
        # chakujun #########################################################
        chakujun \
        = 1 # set_dict_data() で 1 着馬の index を取得するので、None にはできない
        # wakuban ##########################################################
        wakuban \
        = int(self.list_tag_td[0].text)
        # umaban ###########################################################
        umaban \
        = int(self.list_tag_td[1].text)
        # bamei ############################################################
        bamei \
        = self.list_tag_td[3].text.replace("\n", "")
        # sei / rei ########################################################
        src \
        = self.list_tag_td[4].text
        sei \
        = ["牡", "牝", "セ"].index(src[0])
        rei \
        = int(src[1:])
        # x10kinryo ########################################################
        x10kinryo \
        = int(float(self.list_tag_td[5].text) * 10)
        # kishu ############################################################
        kishu \
        = self.list_tag_td[6].text.replace("\n", "")
        # id_kishu #########################################################
        src \
        = self.list_tag_td[6].select_one("a")
        if src is None:
            raise Exception("error: id_kishu")
        id_kishu \
        = src.attrs["href"][-6:-1]
        # x10time ##########################################################
        x10time \
        = None
        # chakusa ##########################################################
        chakusa \
        = None
        # timeshisu ########################################################
        timeshisu \
        = None
        # tsuka ############################################################
        tsuka \
        = None
        # x10agari3f #######################################################
        x10agari3f \
        = None
        # x10tansho ########################################################
        x10tansho \
        = None
        # ninki ############################################################
        ninki \
        = 1 # None だと error、0 だとset_dict_data() で error
        # bataiju, zogen ###################################################
        bataiju, zogen, \
        = None, None,
        # chokyotime #######################################################
        chokyotime \
        = None
        # kyushacomment ####################################################
        kyushacomment \
        = None
        # biko #############################################################
        biko \
        = None
        # shozoku ##########################################################
        src \
        = self.list_tag_td[7].select_one("span")
        if src is None:
            raise Exception("error: shozoku")
        shozoku \
        = ["美浦", "栗東"].index(src.text)
        # chokyoshi, id_chokyoshi ##########################################
        src \
        = self.list_tag_td[7].select_one("a")
        if src is None:
            raise Exception("error: chokyoshi")
        chokyoshi \
        = src.text
        id_chokyoshi \
        = src.attrs["href"][-6:-1]
        # banushi ##########################################################
        banushi \
        = None
        # id_banushi #######################################################
        id_banushi \
        = None
        # x10shokin ########################################################
        x10shokin \
        = None
        # dict_horse #######################################################
        return {
            "id_horse"    : self.id_horse,
            "chakujun"    : chakujun,
            "wakuban"     : wakuban,
            "umaban"      : umaban,
            "bamei"       : bamei,
            "sei"         : sei,
            "rei"         : rei,
            "x10kinryo"   : x10kinryo,
            "kishu"       : kishu,
            "id_kishu"    : id_kishu,
            "x10tansho"   : x10tansho,
            "ninki"       : ninki,
            "shozoku"     : shozoku,
            "chokyoshi"   : chokyoshi,
            "id_chokyoshi": id_chokyoshi,
            "pedigree"    : self.dict_pedigree,
            "calc"
            : { "mannenrei"
                : rei,
                "shijiritsu"
                : None, }, }
