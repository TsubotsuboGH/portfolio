import datetime
import inspect
import numpy as np
import os
import pickle
import pprint
import re
import time

class Bangirasu:
    ### class 変数 #############################################################
    loop_prev \
    = False
    ### custom print ###########################################################
    def cprint(self,
    var_0
    : str | object = "msg",
    name_var
    : str | None = None,
    msg
    : str | None = None,
    # object
    # : object,
    # name_var
    # : int | str = "first",
    # type_cprint
    # : int = 1,
    loop
    : bool = False,
    # tuple_func
    # : tuple = (),
    ) -> None:
        ### loop と loop_prev が共に True でない場合は、改行
        if loop is False or Bangirasu.loop_prev is False:
            print("")
        ### loop と loop_prev が共に True の場合は、カーソルを先頭に移動
        else:
            print("\r", end="", )
        ### np.ndarray を比較すると error するので、除外
        if isinstance(var_0, np.ndarray):
            pass
        ### default, isinstance(str) がないと ndarray 等で error
        elif var_0 == "msg":
            print("[INFO] {ctime}, {structure}"
                .format(
                    ctime=
                        datetime.datetime.now(), # current time
                    structure=
                        " > ".join([
                            "{name_file} {line}"
                            .format(
                                name_file=
                                    fi.filename.split("\\")[-1],
                                line=
                                    fi.lineno,
                            )
                            for fi
                            in  inspect.stack()
                        ][-1:0:-1]
                        )
                        # " > ".join([
                        #         fi.code_context[0]
                        #         .replace(" ", "")
                        #         .replace("()", "")
                        #         .replace("\n", "")
                        #         .replace(".", ".py > ", 1)
                        #     if  fi.function == "<module>"
                        #     and fi.code_context is not None
                        #     else
                        #         fi.function
                        #     for fi
                        #     in  inspect.stack()[-1:0:-1]
                        # ]), # FrameInfo
                        if msg is None
                        else msg,
                ),
                end="", )
            ### return #########################################################
            return #############################################################
        ### loop と loop_prev が共に True でない場合は、変数名を表示
        if loop is False or Bangirasu.loop_prev is False:
            Bangirasu.loop_prev \
            = loop
            if name_var is None:
                ### get: name_var
                src \
                = inspect.stack()[1].code_context
                if src is None:
                    self.raise_exception("type error: None")
                src \
                = re.search(r"\(.*\)", src[0])
                if src is None:
                    self.raise_exception("type error: None")
                name_var \
                = src.group()[1:-1].replace(" ", "").split(",")[0]
            ### print: name_var
            print("    {}".format(name_var, ), )
        ### print: value_var
        print("    = {}".format(var_0), end="", )
        ### return #############################################################
        return #################################################################
    ############################################################################
    def calc_rating(self,
    dict_rating
    : dict[str, dict[str, dict[str, dict[str, float]]]] | None,
    type_rating
    : str,
    new
    : bool,
    ) -> float:
        if dict_rating is None:
            return 0 # 初期 rating
        no \
        = "new" if new else "old"
        return (
              dict_rating["rating"][type_rating][no]["mu"]
            - dict_rating["rating"][type_rating][no]["sigma"] * 3)
    #
    def dump_pkl(self, dir_file, obj) -> None:
        with open(dir_file, "wb") as f:
            pickle.dump(obj, f)
        return
    #
    def load_pkl(self, dir_file, ) -> dict:
        with open(dir_file, "rb") as f:
            obj = pickle.load(f)
        return obj
    #
    def pprint(self, obj, ) -> None:
        pprint.pprint(obj)
        return
    #
    def makedirs(self, dir, exist_ok=False, ) -> None:
        os.makedirs(dir, exist_ok=exist_ok, )
        return
    #
    def get_name_file(self, ) -> str:
        return str(time.time()).replace(".", "")
    #
    def get_value(self, dict_race, index, key: str, ):
        """
        dict_race から必要な値を取得するための関数。
        ------------------------------------------------------------------------
        12. NEW
        +-- obj
        +-- この操作は必要ないと思うが、return するのが dict じゃないのに
            dict ってつくのが嫌なので。
        53. LOOP
        +-- key IN tuple_key
        +-- tuple_key は階層順に並んでいるはずなので、
            順番に取り出すことで、より深い階層の値にアクセスできる。
            26. LOOP
            +-- INFINITY
            +-- 値が list の場合は、key でアクセスできない。
                すなわち、index でアクセスする必要があるため、
                値が list 以外になるまで、この操作を繰り返す。
                15. UPDATE
                +-- obj
            16. UPDATE
            +-- obj
            +-- 値が list でなくなれば、再度 key でアクセスできるので、
                key に対応する値を取得。
        82. RETURN"""
        list_splitted,    obj, \
        = key.split("."), dict_race,                                        # 12
        for k in list_splitted:                                             # 53
            if k == "$":
                obj = obj[index]
            else:
                obj = obj[k]
        return obj                                                          # 82
    #
    def get_nested_value(self, obj, key: str, ):
        list_splitted \
        = key.split(".")
        for key in list_splitted:
            if key[0] == "$":
                obj = obj[int(key[1:])]
            else:
                obj = obj[key]
        return obj
    #
    def raise_exception(self, msg: str = "", ):
        raise Exception(msg)
################################################################################
class Varidate:
    #
    def varidate_dict_detail(self, dict_detail: dict[str, int]) -> bool:
        set_key: set[str] \
            = {"nen", "tsuki", "hi", "keibajo", "kai", "nichi", "r", }
        # dict でない場合
        if not isinstance(dict_detail, dict):
            raise Exception("dict ではありません")
        # key が完全一致しない場合
        if set([k for k in dict_detail]) != set_key:
            raise Exception("key が一致しません")
        # value がすべて int でない場合
        if set([type(v) for v in dict_detail.values()]) != {int}:
            raise Exception("int ではありません")
        # True
        return True
