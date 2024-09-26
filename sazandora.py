import bs4
import datetime
import re
import requests

from bangirasu  import Bangirasu

class MonozuA:
    # init
    def __init__(self, tag_tr: bs4.Tag) -> None:
        self.list_tag_td \
            = tag_tr.select("td") # set: tdタグ(:行内のそれぞれのセル)のlist
        return
    #
    def set_id_horse(self, ):
        src \
            = self.list_tag_td[3].select_one("a")
        self.id_horse \
            = None if src is None else src.attrs["href"][7:-1]
        return self
    #
    def set_chakujun(self, ):
        src \
            = re.sub(r"\D", "", self.list_tag_td[0].text)
        self.chakujun \
            = int(re.sub(r"\D", "", src)) if src else None
        return self
    #
    def set_sei_and_rei(self, ):
        src_seirei \
            = self.list_tag_td[4].text
        self.sei \
            = ["牡", "牝", "セ"].index(src_seirei[0])
        self.rei \
            = int(src_seirei[1:])
        return self
    #
    def set_id_kishu(self, ):
        src \
            = self.list_tag_td[6].select_one("a")
        self.id_kishu \
            = None if src is None else src.attrs["href"][-6:-1]
        return self
    #
    def set_x10time(self, ):
        src \
            = self.list_tag_td[7].text.split(":")
        self.x10time \
            = int(src[0]) * 600 + int(float(src[1]) * 10) if src != [""] else None
        return self
    #
    def set_chakusa(self, ):
        src \
            = self.list_tag_td[8].text
        self.chakusa \
            = src if src else None # 空白(:1着)はNone
        return self
    #
    def set_agari3f(self, ):
        src_agari3f \
            = self.list_tag_td[11].text
        self.x10agari3f \
            = int(float(src_agari3f) * 10) if src_agari3f else None
        return self
    #
    def set_x10tansho(self, ):
        src_tansho \
            = self.list_tag_td[12].text
        self.x10tansho \
            = int(float(src_tansho) * 10) if src_tansho != "---" else None
        return self
    #
    def set_ninki(self, ):
        src_ninki \
            = self.list_tag_td[13].text
        self.ninki \
            = int(src_ninki) if src_ninki else None
        return self
    #
    def set_bataiju_and_zogen(self, ):
        src \
            = self.list_tag_td[14].text.split("(")
        if "." in src:
            raise Exception # 小数点が含まれている場合
        self.bataiju \
            = int(src[0])      if src != ["計不"] else None
        self.zogen \
            = int(src[1][:-1]) if src != ["計不"] else None
        return self
    #
    def set_shozoku_and_chokyoshi(self, ):
        src \
            = self.list_tag_td[18].text
        self.shozoku \
            = ["東", "西", "地", "外"].index(src[2])
        self.chokyoshi \
            = src[4:].replace("\n", "")
        return self
    #
    def set_id_chokyoshi(self, ):
        src \
            = self.list_tag_td[18].select_one("a")
        self.id_chokyoshi \
            = None if src is None else src.attrs["href"][-6:-1]
        return self
    #
    def set_id_banushi(self, ):
        src \
            = self.list_tag_td[19].select_one("a")
        self.id_banushi \
            = None if src is None else src.attrs["href"][-7:-1]
        return self
    #
    def set_shokin(self, ):
        src \
            = self.list_tag_td[20].text
        self.x10shokin \
            = int(float(src.replace(",", "")) * 10) if src else 0
        return self
    #
    def get_dict_horse(self, ):
        return {
            "id_horse"     : self.id_horse,
            "chakujun"     : self.chakujun,
            "wakuban"      : int(self.list_tag_td[1].text),
            "umaban"       : int(self.list_tag_td[2].text),
            "bamei"        : self.list_tag_td[3].text.replace("\n", ""),
            "sei"          : self.sei,
            "rei"          : self.rei,
            "x10kinryo"    : int(float(self.list_tag_td[5].text) * 10),
            "kishu"        : self.list_tag_td[6].text.replace("\n", ""),
            "id_kishu"     : self.id_kishu,
            "x10time"      : self.x10time,
            "chakusa"      : self.chakusa,
            "timeshisu"    : None,
            "tsuka"        : self.list_tag_td[10].text,
            "x10agari3f"   : self.x10agari3f,
            "x10tansho"    : self.x10tansho,
            "ninki"        : self.ninki,
            "bataiju"      : self.bataiju,
            "zogen"        : self.zogen,
            "chokyotime"   : None,
            "kyushacomment": None,
            "biko"         : None,
            "shozoku"      : self.shozoku,
            "chokyoshi"    : self.chokyoshi,
            "id_chokyoshi" : self.id_chokyoshi,
            "banushi"      : self.list_tag_td[19].text.replace("\n", ""),
            "id_banushi"   : self.id_banushi,
            "x10shokin"    : self.x10shokin, }

class MonozuB:
    #
    def __init__(self, tag_tr: bs4.Tag) -> None:
        src \
            = tag_tr.select_one("th")
        self.syubetsu \
            = None if src is None else src.text
        src \
            = tag_tr.select("td")
        list_umaban \
            = src[0].get_text("/").split("/") # brを"/"に変換
        list_haraimodoshi \
            = src[1].get_text("/").split("/") # brを"/"に変換
        self.dict_haraimodoshi = {
            umaban:
                int(haraimodoshi.replace(",", ""))
            for     umaban,      haraimodoshi
            in  zip(list_umaban, list_haraimodoshi)}
        return
    #
    def get_tuple_key_and_value(self, ):
        return (self.syubetsu, self.dict_haraimodoshi, )

class ZiheddoA:
    """
    dict_race の作成を Sazandora 内でやろうとすると、self に設定した値が残り、
    バグの原因になりそう。各レース間で、共通の値は1つもないので、
    レースごとに object を作成することにした。"""
    #
    def __init__(self, id_race: str, date: int, ) -> None:
        self.id_race, self.date, \
            = id_race, date,
        return
    #
    def set_bs(self, ):
        """
        set: uri
        set: beautifulSoup"""
        uri              : str \
            = f"https://db.netkeiba.com/race/{self.id_race}"
        response         : requests.Response \
            = requests.get(uri)
        response.encoding \
            = "euc-jp" # 文字化け対策
        self.bs          : bs4.BeautifulSoup \
            = bs4.BeautifulSoup(response.text, "html.parser")
        return self
    #
    def set_src(self, ):
        """
        After: set_bs()
        ------------------------------------------------------------------------
        set: src_0(競争,距離,天候,馬場状態,発走時刻などの行をそのまま取得)
        set: src_1(日付,回,競馬場,日,クラスなどの行をそのまま取得)
        set: src_2(馬の情報のテーブル)
        set: src_3(払戻のテーブルをそのまま取得)
        set: src_4(コーナー通過順位のテーブル)
        set: src_5(ラップタイムのテーブル)
        set: list_src_0_splitted: 競争~発走時刻までのソース
        set: list_tag_tr_2: 馬関連のtag_trのlist(次のclassに向けて)
        set: list_tag_tr_3: 払戻関連のtag_trのlist(次のclassに向けて)"""
        self.s0             : bs4.Tag | None \
            = self.bs.select_one("#main > div > div > div span")
        self.s1             : bs4.Tag | None \
            = self.bs.select_one("diary_snap div > p")
        self.s2             : bs4.Tag | None \
            = self.bs.select_one(".race_table_01")
        self.s3             : list[bs4.Tag] \
            = self.bs.select(".pay_table_01")
        self.s4             : bs4.Tag | None \
            = self.bs.select_one("table[summary=\"コーナー通過順位\"]")
        self.s5             : bs4.Tag | None \
            = self.bs.select_one("table[summary=\"ラップタイム\"]")
        self.l_s0_splitted: list[str] \
            = [] if self.s0 is None else self.s0.text.split("/") # "/"で分割
        self.list_tag_tr_2: list[bs4.Tag] \
            = [] if self.s2 is None else self.s2.select("tr:not(.txt_c)")
        self.list_tag_tr_3: list[bs4.Tag] \
            = [tag_tr for table in self.s3 for tag_tr in table.select("tr")]
        return self
    #
    def set_racemei(self, ):
        """
        After: set_bs()
        ------------------------------------------------------------------------
        """
        src_racemei : bs4.Tag | None \
            = self.bs.select_one("#main h1")
        if not src_racemei: # Noneの場合
            raise Exception
        self.racemei: str \
            = src_racemei.text
        return self
    #
    def set_hasso(self, ):
        """
        After: set_src()
        ------------------------------------------------------------------------
        SET: 発走時刻"""
        src_hasso : list[str] \
            = self.l_s0_splitted[3].split()[2].split(":")
        self.hasso: int \
            = int(src_hasso[0]) * 60 + int(src_hasso[1])
        return self
    #
    def set_datetime(self, ):
        """
        After: set_src()
        ------------------------------------------------------------------------
        SET: datetime (nen, tsuki, hi, 発走時刻を int にしたもの)"""
        src_time                \
            = re.search(r"\d+:\d+", self.l_s0_splitted[3]) # re.matchは先頭からなので×
        if src_time is None:
            raise Exception("timeエラー")
        time              : str \
            = src_time.group().replace(":", "")
        self.datetime     : str \
            = f"{self.date}{time}"
        return self
    # dict_race
    def get_dict_race(self, ):
        """
        After: set_racemei(), set_hasso(), set_datetime()
        ------------------------------------------------------------------------
        """
        return {
            "list_horse"  : [
                MonozuA(tag_tr=tag_tr)
                    .set_id_horse().set_chakujun().set_sei_and_rei()
                    .set_id_kishu().set_x10time().set_chakusa().set_agari3f()
                    .set_x10tansho().set_ninki().set_bataiju_and_zogen()
                    .set_shozoku_and_chokyoshi().set_id_chokyoshi()
                    .set_id_banushi().set_shokin().get_dict_horse()
                for tag_tr in self.list_tag_tr_2],
            "nen"         : int(str(self.date)[0:4]), # 年
            "tsuki"       : int(str(self.date)[4:6]), # 月
            "hi"          : int(str(self.date)[6:8]), # 日
            "racemei"     : self.racemei,
            "kyoso"       : \
                ["芝", "ダ", "障"].index(self.l_s0_splitted[0][0]), # 0~2
            "kyori"       : \
                int(re.sub(r"\D", "", self.l_s0_splitted[0])), # 数値以外を""に置換
            "tenko"       : \
                ["晴", "曇", "雨", "小雨", "雪", "小雪"].index(self.l_s0_splitted[1].split()[2]), # 0~5
            "baba"        : \
                ["良", "稍重", "重", "不良"].index(self.l_s0_splitted[2].split()[2]), # 0~3
            "hasso"       : self.hasso,
            "keibajo"     : int(self.id_race[4:6]), # 1~10:札幌,函館,福島,新潟,東京,中山,中京,京都,阪神,小倉
            "kai"         : int(self.id_race[6:8]),   # 回
            "nichi"       : int(self.id_race[8:10]),  # 日
            "r"           : int(self.id_race[10:12]), # R
            "id_race"     : self.id_race,
            "haraimodoshi": \
                dict([
                        MonozuB(tag_tr=tag_tr).get_tuple_key_and_value()
                    for tag_tr
                    in  self.list_tag_tr_3]), # k と v の tuple の list を渡すと dict が作れる
            "str_src_0"   : str(self.s0),
            "str_src_1"   : str(self.s1),
            "str_src_2"   : str(self.s2),
            "str_src_3"   : str(self.s3),
            "str_src_4"   : str(self.s4),
            "str_src_5"   : str(self.s5),
            "datetime"    : self.datetime, }

class ZiheddoB:
    #
    def __init__(self, id_horse: str, ) -> None:
        uri             : str \
            = f"https://db.netkeiba.com/horse/ped/{id_horse}/"
        while True: # 謎エラーの防止のため
            try:
                response: requests.Response \
                    = requests.get(uri) # set: beautifulSoup
                break
            except requests.exceptions.SSLError:
                pass
        response.encoding \
            = "euc-jp" # 文字化け対策
        bs              : bs4.BeautifulSoup \
            = bs4.BeautifulSoup(response.text, "html.parser")
        self.dict_ped   : dict[str, str] \
            = {"id_horse": id_horse, } # 新規変数、当代を追加
        # 1, 2, 3, 4 代前 と 5 代前を結合
        # rowspan と height で違うため、このような形式にしている
        # bs.select では list が返されるため、すべての list を sum で結合
        list_tag_a \
            = sum([
                bs.select(f"td[rowspan='{rowspan}'] > a:nth-child(1)")
                for rowspan
                in  ["16", "8", "4", "2", ]], []) \
            + bs.select(f"td[height='20'] > a:nth-child(1)")
        self.dict_ped.update({
            f"{i+2}": tag_a.attrs["href"][7:-1]
            for i, tag_a in enumerate(list_tag_a)})
        return
    #
    def get_dict_ped(self, ):
        return self.dict_ped

class Sazandora(Bangirasu):
    """スクレイピング用 class"""
    #
    def __init__(self):
        super().__init__()
        self.date_today : int \
            = int(datetime.date.today().strftime("%Y%m%d")) # get: date(today)
        src \
            = self.find_one(**{
                "key_collection": "race",
                "filter"        : {},
                "projection"    : {
                    "datetime": 1, },
                "sort"          : [
                    ("datetime", -1), ], })
        self.date_latest_in_db: int \
            = 20000101 if src is None else int(src["datetime"][0:8])
        return
    # すべてを scrape
    def scrape(self, ) -> None:
        while self.date_latest_in_db <= self.date_today:
            try:
                self.in_while()
            except requests.exceptions.SSLError: # たまになる、理由は不明
                continue
        for dict_race in self.find(**{
            "key_collection": "race",
            "filter"        : {
                "list_horse.pedigree": {
                    "$exists": 0, }, },
            "projection"    : {
                "id_race"            : 1,
                "list_horse.id_horse": 1, }, }):
            self.in_for_b(dict_race=dict_race)
        return
    #
    def in_while(self, ) -> None:
        self.set_list_id_race()                                             # 00
        for id_race in self.list_id_race:                                   # 01
            self.in_for(id_race=id_race)                                    #
        self.update_date_latest_in_db()
        return
    # 日付から list_id_race を scrape
    def set_list_id_race(self, ) -> None:
        """
        00: NEW
        +-- uri_date
        +-- その日に行われたレースの一覧が表示される uri。
        01: NEW
        +-- content
        +-- uri の content を取得。
        02: NEW
        +-- bs
        +-- content を bs4 の形式に変換。
        03: NEW
        +-- list_tag_a
        +-- aタグのうち、href  にid_race を含むものの list
        04: SET
        +-- self.list_id_race
        +-- id_race の list
        05: RETURN
        +-- list_id_race"""
        uri_date         : str \
            = f"https://db.netkeiba.com/race/list/{self.date_latest_in_db}/"# 00
        content      = requests.get(uri_date).content                       # 01
        bs           = bs4.BeautifulSoup(content, "html.parser")            # 02
        list_tag_a   = bs.select("li > dl > dd > a")                        # 03
        self.list_id_race: list[str] \
            = [tag_a.attrs["href"][6:-1] for tag_a in list_tag_a]           # 04
        return                                                              # 05
    #
    def in_for(self, id_race: str, ) -> None:
        if id_race[4:6] == "P0":
            print(f"    {id_race} は, 外国の競馬場です.")
            return
        if id_race == "200808020399":
            id_race = "200808020301"
        elif id_race == "200808020398":
            id_race = "200808020302"
        if self.find_one(**{
            "key_collection": "race",
            "filter"        : {
                "id_race": id_race, }, }) is not None:
            print(f"    {id_race} は, 既に登録済みです.")
            return
        else:
            print(f"    {id_race}")
        dict_race \
            = ZiheddoA(id_race=id_race, date=self.date_latest_in_db) \
                .set_bs().set_src().set_racemei().set_hasso().set_datetime() \
                .get_dict_race()
        self.insert_one(key_collection="race", document=dict_race, )
        return
    #
    def update_date_latest_in_db(self, ) -> None:
        # update: date_latestを1日進める
        self.date_latest_in_db += 1
        # update: date_latestが32日や13月になった場合
        if "32" == str(self.date_latest_in_db)[6:8]: # 32日
            self.date_latest_in_db += 69
        if "13" == str(self.date_latest_in_db)[4:6]: # 13月
            self.date_latest_in_db += 8800
        return
    #
    def set_set_id_horse_inserted(self, ):
        self.set_id_horse_inserted: set[str] \
            = {
                    dict_horse["id_horse"]
                for dict_horse
                in  self.find(**{
                    "key_collection": "pedigree",
                    "filter"        : {},
                    "projection"    : {
                        "id_horse": 1, }, })}
        return self
    #
    def in_for_b(self, dict_race: dict, ) -> None:
        print(f'[in in_for_b] {dict_race["id_race"]}')
        for dict_horse in dict_race["list_horse"]:
            self.in_for_ba(**{
                "id_race" : dict_race["id_race"],
                "id_horse": dict_horse["id_horse"], })
        return
    #
    def in_for_ba(self, id_race: str, id_horse: str, ):
        if self.find_one(**{
            "key_collection": "pedigree",
            "filter"        : {
                "id_horse": id_horse, }, }) is None:
            self.insert_one(**{
                "key_collection": "pedigree",
                "document"      : ZiheddoB(id_horse=id_horse).get_dict_ped(), })
            self.create_index(**{
                "key_collection": "pedigree",
                "keys"          : "id_horse", }) # 時短のため index を作成
        dict_ped \
            = self.find_one(**{
                "key_collection": "pedigree",
                "filter"        : {
                    "id_horse": id_horse, },
                "projection"    : {
                    "_id"     : 0,
                    "id_horse": 0, }, })
        self.update_one(**{
            "key_collection": "race",
            "filter"        : {
                "id_race": id_race, },
            "update"        : {
                "$set": {
                    "list_horse.$[elem].pedigree": dict_ped, }, },
            "array_filters" : [
                {
                    "elem.id_horse": id_horse, }, ], })
        return
