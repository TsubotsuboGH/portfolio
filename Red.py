import importlib

import bomanda
import kairyu
import sazandora
import metagurosu
import gaburiasu
import test
# from doraparuto import Doraparuto
# from kairyu import Miniryu

while True:
    importlib.reload(bomanda)
    bo \
    = bomanda.Bomanda()
    print(
        "\n"
        "s: scrape & calc\n"
        "k: rating を追加\n"
        "g: 予測（実験）\n"
        "d: 予測（本番）\n"
        "t: テスト\n"
        "b: break\n"
    )
    command = input(">>> ")
    ### データベースアップデート ###############################################
    if   command == "s":
        sazandora.Sazandora().scrape()
        metagurosu.Metagurosu(bo=bo, ).calc_tousu().calc_mannenrei().calc_shijiritsu()
    ### データベースに rating を追加 ###########################################
    elif command == "k":
        kairyu.Kairyu()
    ### 予測 (実験) ############################################################
    elif command == "g":
        gaburiasu.Gaburiasu()
    ### 予測 (本番) ############################################################
    elif command == "d":
        doraparuto.Doraparuto()
    ### テスト #################################################################
    elif command == "t":
        test.Test()
    ### 終了 ###################################################################
    elif command == "b":
        break
    ### いずれにも該当しない ###################################################
    else:
        print("正しいコマンドを入力してください。")
    # Metagurosu().create_index(**{
    #     "key_collection"
    #     : "rating",
    #     "keys"
    #     : [ ("str_tuple_key",    1, ), # この行がないと再計算時の日付が取得できない
    #         ("str_tuple_value",  1, ),
    #         # ("datetime",        -1, ),
    #         ("id_race",         -1, ), ],
    #     "unique"
    #     : True, })
    """#### データベースの不具合・不整合チェック ############################"""
    # m = Metagurosu().sort_rating()
    # raise Exception

    """#### (WARNING) rating をすべて削除 ###################################"""
    # Metagurosu().del_rating()
    # raise Exception
