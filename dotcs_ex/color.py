from typing import Literal, TextIO
import datetime
import sys
import re
import sys
import re
color_rep = {
    "§1":"\033[0;37;34m",
    "§2":"\033[0;37;32m",
    "§3":"\033[0;37;36m",
    "§4":"\033[0;37;31m",
    "§5":"\033[0;37;35m",
    "§6":"\033[0;37;33m",
    "§7":"\033[0;37;90m",
    "§8":"\033[0;37;2m",
    "§9":"\033[0;37;94m",
    "§a":"\033[0;37;92m",
    "§b":"\033[0;37;96m",
    "§c":"\033[0;37;91m",
    "§d":"\033[0;37;95m",
    "§e":"\033[0;37;93m",
    "§f":"\033[0;37;1m",
    "§r":"\033[0m",
    }
color_rep = dict((re.escape(k), v) for k, v in color_rep.items())
color_rep_str = "|".join(color_rep.keys())
color_rep_compile = re.compile(color_rep_str)
info_rep = {
    "§1":"\033[7;37;34m",
    "§2":"\033[7;37;32m",
    "§3":"\033[7;37;36m",
    "§4":"\033[7;37;31m",
    "§5":"\033[7;37;35m",
    "§6":"\033[7;37;33m",
    "§7":"\033[7;37;90m",
    "§8":"\033[7;37;2m",
    "§9":"\033[7;37;94m",
    "§a":"\033[7;37;92m",
    "§b":"\033[7;37;96m",
    "§c":"\033[7;37;91m",
    "§d":"\033[7;37;95m",
    "§e":"\033[7;37;93m",
    "§f":"\033[7;37;1m",
    "§r":"\033[0m"
    }
info_rep = dict((re.escape(k), v) for k, v in info_rep.items())
info_rep_str = "|".join(info_rep.keys())
info_rep_compile = re.compile(info_rep_str)
def removeColorInText(text):
    """
    过滤 color 函数中 info 的彩色字
    ---
    参数:
        text:str 文本
    返回:
        str"""
    return text.replace("\033[0;37;34m", "").replace("\033[0;37;32m", "").replace("\033[0;37;36m", "").replace("\033[0;37;31m", "").replace("\033[0;37;35m", "").replace("\033[0;37;33m", "").replace("\033[0;37;90m", "").replace("\033[0;37;2m", "").replace("\033[0;37;94m", "").replace("\033[0;37;92m", "").replace("\033[0;37;96m", "").replace("\033[0;37;91m", "").replace("\033[0;37;95m", "").replace("\033[0;37;93m", "").replace("\033[0;37;1m", "").replace("\033[0m", "").replace("\033[7;37;34m", "").replace("\033[7;37;32m", "").replace("\033[7;37;36m", "").replace("\033[7;37;31m", "").replace("\033[7;37;35m", "").replace("\033[7;37;33m", "").replace("\033[7;37;90m", "").replace("\033[7;37;2m", "").replace("\033[7;37;94m", "").replace("\033[7;37;92m", "").replace("\033[7;37;96m", "").replace("\033[7;37;91m", "").replace("\033[7;37;95m", "").replace("\033[7;37;93m", "").replace("\033[7;37;1m", "")
def removeColorMC(text: str) -> str:
    """
    过滤mc的彩色字
    ---
    参数:
        text:文本
    返回:
        str
    """
    return text.replace("§0", "\033[0;37;30m").replace("§1", "").replace("§2", "").replace("§3", "").replace("§4", "").replace("§5", "").replace("§6", "").replace("§7", "").replace("§8", "").replace("§9", "").replace("§a", "").replace("§b", "").replace("§c", "").replace("§d", "").replace("§e", "").replace("§f", "m").replace("§r", "")


def getTextColorInTheEnd(text: str) -> str:
    """
    获取 Text 的结尾内容并返回对应代码
    ---
    参数:
        text:文本
    返回:
        str
    """
    if "\033[" in text and "m" in text:
        return "\033[" + text.split("\033[")[-1].split("m")[0] + "m"
    else:
        return "\033[0m"


def _color(*values, output: bool = True, end: str = '\n', replace: bool = False, replaceByNext: bool = False, info: str | bool = " 信息 ", sep=' ', file: TextIO = sys.stdout, flush=False, word_wrapping: bool = True, text: str = None, is_time: bool = True, end_not_replace: bool = False, no_color: int = 0, title_time: str = "[%H:%M:%S] ", color_mode: int = 0, **date) -> None | str:
    """
    在命令系统控制台输出信息
    默认情况下，将值打印到流或 sys.stdout。
    ---

    参数:
        values : 要输出的内容.
        text: 要输出的内容(旧版),默认不使用,如果使用就当作 只有一个参数的 values 进行处理
        file: 类似文件的对象（流）;默认为 sys.stdout。
        sep: 在值之间插入字符串，默认为空格。
        end: 字符串追加在最后一个值之后，默认换行符。
        output: bool -> 是否输出.(返回的值是 values 拼接后的值)
        replace: bool -> 将 end 值修改为 "" 并返回行首(首个输出改成了 \\r )
            True: 若下次输出时 replace 还是为True, 则这次输出将被下次输出覆盖, 否则不会被覆盖.
            False: 普通的输出.
        replaceByNext: bool -> 是否一定被下次输出覆盖.(作用与 replace 相同,权限级别更高)
            True : 将 replace 的值改为 True
            False: 不做任何影响
        info: str -> 输出内容前的反色信息.(默认使用 文本的第一个彩色字符)
        flush: 是否强制冲刷流(如果output值为 True,则会在 end 输出后执行)
        word_wrapping : bool -> 是否自动换行输出(会将所有的\n进行处理)(默认为 True)
        is_time : 是否在终端显示时间(默认为 False)
        end_not_replace : 输出的内容结尾是否不添加彩色字的重置符(默认False)
        no_color : 是否直接移除彩色字的效果(默认值为0)
            0 : 不移除
            1 : 只移除 info 
            2 : 只移除 values
            3 : 都移除
            4 : info 的彩色字符号不做处理
            5 : values 的彩色字符号不做处理
            6 : info 、values 的彩色字符号均不做处理 
        title_time: 格式化时间 ,默认值 "[%H:%M:%S] "
    返回: None | str
    """
    if text:
        return color(text, output=output, end=end, replace=replace, replaceByNext=replaceByNext, info=info, sep=sep, file=file, flush=flush, word_wrapping=word_wrapping, text=None, **date)
    if replaceByNext:replace = True
    _values = []
    if replace:_values.append("\n");end = ""
    # 获取 values[0][0:2] 的优化
    if info:
        if no_color not in [1, 3]:
            if no_color not in [4, 6]:
                if color_mode not in [1, 3]:
                    match str(values[0])[0:2]:
                        case "§1":
                            _info = "\033[7;37;34m"
                        case "§2":
                            _info = "\033[7;37;32m"
                        case "§3":
                            _info = "\033[7;37;36m"
                        case "§4":
                            _info = "\033[7;37;31m"
                        case "§5":
                            _info = "\033[7;37;35m"
                        case "§6":
                            _info = "\033[7;37;33m"
                        case "§7":
                            _info = "\033[7;37;90m"
                        case "§8":
                            _info = "\033[7;37;2m"
                        case "§9":
                            _info = "\033[7;37;94m"
                        case "§a":
                            _info = "\033[7;37;92m"
                        case "§b":
                            _info = "\033[7;37;96m"
                        case "§c":
                            _info = "\033[7;37;91m"
                        case "§d":
                            _info = "\033[7;37;95m"
                        case "§e":
                            _info = "\033[7;37;93m"
                        case "§f":
                            _info = "\033[7;37;1m"
                        case "§r":
                            _info = "\033[0m"
                        case _:
                            _info = "\033[7;37;1m"
                else:
                    match str(values[0])[0:2]:
                        case "§1":
                            _info = "\033[7;37;34m§1"
                        case "§2":
                            _info = "\033[7;37;32m§2"
                        case "§3":
                            _info = "\033[7;37;36m§3"
                        case "§4":
                            _info = "\033[7;37;31m§4"
                        case "§5":
                            _info = "\033[7;37;35m§5"
                        case "§6":
                            _info = "\033[7;37;33m§6"
                        case "§7":
                            _info = "\033[7;37;90m§7"
                        case "§8":
                            _info = "\033[7;37;2m§8"
                        case "§9":
                            _info = "\033[7;37;94m§9"
                        case "§a":
                            _info = "\033[7;37;92m§a"
                        case "§b":
                            _info = "\033[7;37;96m§b"
                        case "§c":
                            _info = "\033[7;37;91m§c"
                        case "§d":
                            _info = "\033[7;37;95m§d"
                        case "§e":
                            _info = "\033[7;37;93m§e"
                        case "§f":
                            _info = "\033[7;37;1m§f"
                        case "§r":
                            _info = "\033[0m§r"
                        case _:
                            _info = "\033[7;37;1m"
                if color_mode  in [1, 3]:
                    info = "".join([_info, info.replace("§1", "\033[7;37;34m§1").replace("§2", "\033[7;37;32m§2").replace("§3", "\033[7;37;36m§3").replace("§4", "\033[7;37;31m§4").replace("§5", "\033[7;37;35m§5").replace("§6", "\033[7;37;33m§6").replace("§7", "\033[7;37;90m§7").replace("§8", "\033[7;37;2m§8").replace(
                        "§9", "\033[7;37;94m§9").replace("§a", "\033[7;37;92m§a").replace("§b", "\033[7;37;96m§b").replace("§c", "\033[7;37;91m§c").replace("§d", "\033[7;37;95m§d").replace("§e", "\033[7;37;93m§e").replace("§f", "\033[7;37;1m§f").replace("§r", "\033[0m§r")+"\033[0m ", "\033[0m"])
                else:
                    info = "".join([_info, info.replace("§1", "\033[7;37;34m").replace("§2", "\033[7;37;32m").replace("§3", "\033[7;37;36m").replace("§4", "\033[7;37;31m").replace("§5", "\033[7;37;35m").replace("§6", "\033[7;37;33m").replace("§7", "\033[7;37;90m").replace("§8", "\033[7;37;2m").replace(
                        "§9", "\033[7;37;94m").replace("§a", "\033[7;37;92m").replace("§b", "\033[7;37;96m").replace("§c", "\033[7;37;91m").replace("§d", "\033[7;37;95m").replace("§e", "\033[7;37;93m").replace("§f", "\033[7;37;1m").replace("§r", "\033[0m")+"\033[0m ", "\033[0m"])
        else:
            info = "[{}] ".format(removeColorInText(info).replace(" ", ""))
    else:
        info = ""
    next_print_first = ""

    for i in values:
        i = str(i)
        if word_wrapping:
            # 特殊处理
            if "\n" in i:
                all = i.split("\n")
                __values = []
                for v, f in enumerate(all):
                    all_1 = len(all)-1
                    f = str(f)
                    ret = re.findall('§[a-fr0-9]', f)
                    if len(ret) != 0:
                        next_print_first = ret[-1]
                    pass
                    if v == 0:
                        if no_color not in [5, 6]:
                            if color_mode not in [2, 3]:
                                __values.append((next_print_first+f+"\n").replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+"\033[0m")
                            else:
                                __values.append(next_print_first.replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+(f+"\n").replace("§1", "\033[0;37;34m§1").replace("§2", "\033[0;37;32m§2").replace("§3", "\033[0;37;36m§3").replace("§4", "\033[0;37;31m§4").replace("§5", "\033[0;37;35m§5").replace("§6", "\033[0;37;33m§6").replace("§7", "\033[0;37;90m§7").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m§9").replace("§a", "\033[0;37;92m§a").replace("§b", "\033[0;37;96m§b").replace("§c", "\033[0;37;91m§c").replace("§d", "\033[0;37;95m§d").replace("§e", "\033[0;37;93m§e").replace("§f", "\033[0;37;1m§f").replace("§r", "\033[0m§r")+"\033[0m")
                        else:
                            __values.append(
                                (next_print_first+f+"\n")+"\033[0m")
                        continue
                    if v == all_1:
                        if no_color not in [5, 6]:
                            if color_mode not in [2, 3]:
                                __values.append((datetime.datetime.now().strftime(title_time)+info+next_print_first+f).replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+"\033[0m")
                            else:
                                __values.append((datetime.datetime.now().strftime(title_time).replace("§1", "\033[0;37;34m§1").replace("§2", "\033[0;37;32m§2").replace("§3", "\033[0;37;36m§3").replace("§4", "\033[0;37;31m§4").replace("§5", "\033[0;37;35m§5").replace("§6", "\033[0;37;33m§6").replace("§7", "\033[0;37;90m§7").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m§9").replace("§a", "\033[0;37;92m§a").replace("§b", "\033[0;37;96m§b").replace("§c", "\033[0;37;91m§c").replace("§d", "\033[0;37;95m§d").replace("§e", "\033[0;37;93m§e").replace("§f", "\033[0;37;1m§f").replace("§r", "\033[0m§r")+"\033[0m"+info+"\033[0m"+next_print_first.replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+f)+"\033[0m")
                        else:
                            __values.append((datetime.datetime.now().strftime(
                                title_time)+info+next_print_first+f)+"\033[0m")
                        continue
                    if no_color not in [5, 6]:
                        if color_mode not in [2, 3]:
                            __values.append((datetime.datetime.now().strftime(title_time)+info+next_print_first.replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                                "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+f.replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                                "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+"\033[0m"+"\n")+"\033[0m")
                        else:
                            __values.append((datetime.datetime.now().strftime(title_time)+info+next_print_first.replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+f.replace("§1", "\033[0;37;34m§1").replace("§2", "\033[0;37;32m§2").replace("§3", "\033[0;37;36m§3").replace("§4", "\033[0;37;31m§4").replace("§5", "\033[0;37;35m§5").replace("§6", "\033[0;37;33m§6").replace("§7", "\033[0;37;90m§7").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m§9").replace("§a", "\033[0;37;92m§a").replace("§b", "\033[0;37;96m§b").replace("§c", "\033[0;37;91m§c").replace("§d", "\033[0;37;95m§d").replace("§e", "\033[0;37;93m§e").replace("§f", "\033[0;37;1m§f").replace("§r", "\033[0m§r")+"\033[0m"+"\n")+"\033[0m")
                    else:
                        __values.append((datetime.datetime.now().strftime(
                            title_time)+info+next_print_first+f+"\n")+"\033[0m")
                _values.append("".join(__values))
            else:
                if no_color not in [5, 6]:
                    if color_mode not in [2, 3]:
                        _values.append(i.replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                            "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+"\033[0m")
                    else:
                        _values.append(i.replace("§1", "\033[0;37;34m§1").replace("§2", "\033[0;37;32m§2").replace("§3", "\033[0;37;36m§3").replace("§4", "\033[0;37;31m§4").replace("§5", "\033[0;37;35m§5").replace("§6", "\033[0;37;33m§6").replace("§7", "\033[0;37;90m§7").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m§9").replace("§a", "\033[0;37;92m§a").replace("§b", "\033[0;37;96m§b").replace("§c", "\033[0;37;91m§c").replace("§d", "\033[0;37;95m§d").replace("§e", "\033[0;37;93m§e").replace("§f", "\033[0;37;1m§f").replace("§r", "\033[0m§r")+"\033[0m")
                else:
                    _values.append(i+"\033[0m")
        else:
            if no_color not in [2, 3]:
                if no_color not in [5, 6]:
                    if color_mode not in [2, 3]:
                        _values.append(i.replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace(
                            "§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+"\033[0m")
                    else:
                        _values.append(i.replace("§1", "\033[0;37;34m§1").replace("§2", "\033[0;37;32m§2").replace("§3", "\033[0;37;36m§3").replace("§4", "\033[0;37;31m§4").replace("§5", "\033[0;37;35m§5").replace("§6", "\033[0;37;33m§6").replace("§7", "\033[0;37;90m§7").replace("§8", "\033[0;37;2m").replace(
                                    "§9", "\033[0;37;94m§9").replace("§a", "\033[0;37;92m§a").replace("§b", "\033[0;37;96m§b").replace("§c", "\033[0;37;91m§c").replace("§d", "\033[0;37;95m§d").replace("§e", "\033[0;37;93m§e").replace("§f", "\033[0;37;1m§f").replace("§r", "\033[0m§r")+"\033[0m")
                else:
                    _values.append(i+"\033[0m")
            else:
                _values.append(removeColorMC(i))
    if end_not_replace:
        _values[-1] = _values[-1].rstrip("\033[0m")
    if output:
        if is_time:
            print(datetime.datetime.now().strftime(title_time),
                  sep="", end="", file=file, flush=flush)
        print(info, sep="", end="", file=file, flush=flush)
        print(*_values, sep=sep, end=end, file=file, flush=flush)
    else:
        return_text = []
        if is_time:
            return_text.append(datetime.datetime.now().strftime(title_time))
        for i, v in enumerate(_values):
            return_text.append(v)
            if i != len(_values)-1:
                return_text.append(sep)
            else:
                return_text.append("\033[0m")
        return "".join(return_text)

def info_repalce(text:str)->str:
    return info_rep_compile.sub(lambda m: info_rep[re.escape(m.group(0))], text)

def color_replace(text:str)->str:
    return color_rep_compile.sub(lambda m: color_rep[re.escape(m.group(0))], text)
def color(*values, output: bool = True, end: str = '\n', replace: bool = False, replaceByNext: bool = False, info: str | bool = " 信息 ", sep=' ', file: TextIO = sys.stdout, flush=False, word_wrapping: bool = True, text: str = None, is_time: bool = True, end_not_replace: bool = False, no_color: int = 0, title_time: str = "[%H:%M:%S] ", color_mode: int = 0, **date) -> None | str:
    """
    在命令系统控制台输出信息
    默认情况下，将值打印到流或 sys.stdout。
    ---

    参数:
        values : 要输出的内容.
        text: 要输出的内容(旧版),默认不使用,如果使用就当作 只有一个参数的 values 进行处理
        file: 类似文件的对象（流）;默认为 sys.stdout。
        sep: 在值之间插入字符串，默认为空格。
        end: 字符串追加在最后一个值之后，默认换行符。
        output: bool -> 是否输出.(返回的值是 values 拼接后的值)
        replace: bool -> 将 end 值修改为 "" 并返回行首(首个输出改成了 \\r )
            True: 若下次输出时 replace 还是为True, 则这次输出将被下次输出覆盖, 否则不会被覆盖.
            False: 普通的输出.
        replaceByNext: bool -> 是否一定被下次输出覆盖.(作用与 replace 相同,权限级别更高)
            True : 将 replace 的值改为 True
            False: 不做任何影响
        info: str -> 输出内容前的反色信息.(默认使用 文本的第一个彩色字符)
        flush: 是否强制冲刷流(如果output值为 True,则会在 end 输出后执行)
        word_wrapping : bool -> 是否自动换行输出(会将所有的\n进行处理)(默认为 True)
        is_time : 是否在终端显示时间(默认为 False)
        end_not_replace : 输出的内容结尾是否不添加彩色字的重置符(默认False)
        title_time: 格式化时间 ,默认值 "[%H:%M:%S] "
    返回: None | str
    """
    if text:return color(text, output=output, end=end, replace=replace, replaceByNext=replaceByNext, info=info, sep=sep, file=file, flush=flush, word_wrapping=word_wrapping, text=None, **date)
    if replaceByNext:replace = True
    _values = []
    if replace:_values.append("\n");end = ""
    if info:
        match str(values[0])[0:2]:
            case "§1":
                _info = "\033[7;37;34m"
            case "§2":
                _info = "\033[7;37;32m"
            case "§3":
                _info = "\033[7;37;36m"
            case "§4":
                _info = "\033[7;37;31m"
            case "§5":
                _info = "\033[7;37;35m"
            case "§6":
                _info = "\033[7;37;33m"
            case "§7":
                _info = "\033[7;37;90m"
            case "§8":
                _info = "\033[7;37;2m"
            case "§9":
                _info = "\033[7;37;94m"
            case "§a":
                _info = "\033[7;37;92m"
            case "§b":
                _info = "\033[7;37;96m"
            case "§c":
                _info = "\033[7;37;91m"
            case "§d":
                _info = "\033[7;37;95m"
            case "§e":
                _info = "\033[7;37;93m"
            case "§f":
                _info = "\033[7;37;1m"
            case "§r":
                _info = "\033[0m"
            case _:
                _info = "\033[7;37;1m"
        info ="".join([_info,info_repalce(info),"\033[0m"," "])
    else:
        info = ""
    next_print_first = ""
    for i in values:
        i = str(i)
        if word_wrapping:
            # 特殊处理
            if "\n" in i:
                all = i.split("\n")
                __values = []
                for v, f in enumerate(all):
                    all_1 = len(all)-1
                    f = str(f)
                    ret = re.findall('§[a-fr0-9]', f)
                    if len(ret) != 0:
                        next_print_first = ret[-1]
                    if v == 0:
                        __values.append("".join([color_replace(next_print_first),color_replace(f),"\033[0m","\n"]))
                        continue
                    if v == all_1:
                        __values.append("".join([datetime.datetime.now().strftime(title_time) if is_time else "",info,color_replace(next_print_first),color_replace(f),"\033[0m"]))
                        continue
                    __values.append("".join([datetime.datetime.now().strftime(title_time) if is_time else "",info,color_replace(next_print_first),color_replace(f),"\033[0m","\n"]))
                
                _values.append("".join(__values))
            else:
                _values.append(color_replace(i)+"\033[0m")
        else:
            _values.append(color_replace(i)+"\033[0m")
    if end_not_replace:
        _values[-1] = _values[-1].rstrip("\033[0m")
    if output:
        _values[0] = "".join([datetime.datetime.now().strftime(title_time) if is_time else "",info if info else "",_values[0]])
        print(*_values, sep=sep, end=end, file=file, flush=flush)
 
 
 
 