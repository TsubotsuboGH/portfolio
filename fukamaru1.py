import importlib

import bomanda
import bangirasu
import fukamaru2
import fukamaru3
import metagurosu

class Fukamaru1(bangirasu.Bangirasu):
    ############################################################################
    def __init__(self,
    filter_race
    : dict[str, int],
    bo
    : bomanda.Bomanda,
    ) -> None:
        """
        0
        -
        filter
        : 予測の対象とするレース種別。馬場、頭数、競馬場などを指定した dict。
        
        00. [object] fukamaru2 を作成。
        01. 各 datetime を取得・設定。
        02. 各 datetime を比較し、model の update の必要性を検討。
        03. db から iter_dict_race を取得し、
            iter_dict_race から list_dict_race を設定。
        04. list_dict_race の要素数から、split できるかを検討。
        05. 以降使用しない iter_dict_race を削除。
        06. dict_list_dict_bairitsu を loop。"""
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.filter_race, self.bo, \
        =    filter_race,      bo,
        self.me: metagurosu.Metagurosu \
        =    metagurosu.Metagurosu(bo=bo, )
        ### cprint #############################################################
        self.cprint(self.filter_race, ) ########################################
        ########################################################################
        fu2 \
        = fukamaru2.Fukamaru2(filter_race=filter_race, bo=bo, )             # 00
        (fu2
        .set_datetime_latest_in_race()
        .set_datetime_in_model())                                           # 01
        if not fu2.should_update_model():                                   # 02
            ### return #########################################################
            return #############################################################
            ####################################################################
        (fu2
        .set_iter_dict_race()
        .set_list_dict_race())                                              # 03
        if not fu2.can_split():                                       # 04
            ### return #########################################################
            return #############################################################
            ####################################################################
        (fu2
        .del_iter_dict_race())                                              # 05
        for              dict_to_create_model \
        in  self.bo.list_dict_to_create_model:                              # 06
            while True:
                try:
                    (fukamaru3.Fukamaru3(
                        dict_to_create_model=
                            dict_to_create_model,
                        fu2=fu2,
                        bo =bo, )
                    .set_list_index_to_split()
                    .set_dict_list_dict_race()
                    # .del_list_dict_race()
                    .del_list_index_to_split()
                    ### amp pattern 1 ##########################################
                    # .set_p_to_amp()
                    # .update_dict_list_dict_race_amp()
                    # .update_dict_list_dict_race_ran()
                    ### amp pattern 2 ##########################################
                    .update_dict_list_dict_race_amp()
                    ### amp pattern fin ########################################
                    .set_dict_data()
                    .del_dict_list_dict_race()
                    ### ここまでで一区切り ###
                    .set_dataset()
                    .set_model()
                                                # .save_dict_model()
                    .set_d2a_pred(type_pred="test")
                    ### 0 ######################################################
                    .insert_data_to_analyze()
                    # ### 1 ######################################################
                    # # .update_dict_haraimodoshi(type_pred="test")
                    # ############################################################
                    # ### 2 ######################################################
                    # .set_d1a_argmax()
                    # .init_dict_haraimodoshi(type_pred="test")
                    # .set_dict_haraimodoshi()
                    # ############################################################
                    # .print_dict_haraimodoshi()
                    # # .save_dict_haraimodoshi()
                    )
                    break
                except Exception as e:
                    print(e)
                    if input("修正してください.") == "b":
                        break
                    importlib.reload(fukamaru3)
        ### return #############################################################
        return #################################################################
    ############################################################################
    def set_res(self, ):
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        self.res \
        = self.me.find_one(**{
            "key_collection"
            : "model",
            "filter"
            : { "filter_race"
                : self.filter_race, }, })
        ### return #############################################################
        return self ############################################################
    ############################################################################
    def get_p(self, ):
        ### cprint #############################################################
        self.cprint() ##########################################################
        ### return #############################################################
        return None if self.res is None else self.res["p"] #####################
    ############################################################################
    def get_dict_model(self, ):
        ### cprint #############################################################
        self.cprint() ##########################################################
        ### return #############################################################
        return (
                None
            if self.res is None
            else
                self.load_pkl(dir_file=self.res["path_pkl"]))
    ############################################################################
