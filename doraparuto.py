import bangirasu
import bomanda
import doronchi
from sazandora import ZiheddoB  # 血統スクレイピング用クラス
################################################################################
class Doraparuto(bangirasu.Bangirasu):
    ### init ###################################################################
    def __init__(self, ) -> None:
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        bo: bomanda.Bomanda \
        =   bomanda.Bomanda()
        for id_race in bo.list_id_race_prod:
            # try:
            (doronchi.Doronchi(id_race=id_race, bo=bo)
            .set_bs()
            .set_tousu()
            .set_dict_race()
            .del_bs()
            .set_dict_model_and_p()
            .set_list_dict_race()
            .del_dict_race()
            .set_dict_list_dict_race()
            .del_list_dict_race()
            ### ここまでで一区切り ###
            .update_dict_list_dict_race_amp()
            .set_dict_data()
            .del_dict_list_dict_race()
            .set_dict_pred(type_pred="prod")
            .set_d1a_argmax()
            .init_dict_haraimodoshi(type_pred="prod")
            .set_umaban_to_buy())
            # except Exception:
            #     continue
        ### return #############################################################
        return #################################################################
################################################################################
