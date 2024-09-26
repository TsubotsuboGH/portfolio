import bangirasu
import bomanda
import fukamaru1

class Gaburiasu(bangirasu.Bangirasu):
    def __init__(self, ) -> None:
        ### cprint #############################################################
        self.cprint() ##########################################################
        ########################################################################
        bo: bomanda.Bomanda \
        =   bomanda.Bomanda()
        for filter_race in bo.list_filter_race:
            fukamaru1.Fukamaru1(filter_race=filter_race, bo=bo, )
        ### return #############################################################
        return #################################################################
        ########################################################################
