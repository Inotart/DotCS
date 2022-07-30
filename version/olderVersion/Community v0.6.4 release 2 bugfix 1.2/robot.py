# 导入库
print("Importing.")
import os
import socket
import datetime
import time
import json
import threading
import random
import proxy
from proxy import forward
from proxy import utils
import sys
import urllib
import urllib.parse
import _thread as thread
import re
import requests
import platform

# 检测系统版本
platformVer = str(platform.platform())
if "indows" in platformVer:
    platformVer = "Windows"
else:
    platformVer = "Linux"

# 设置运行代码
codeRobot = \
r"""
# 设置版本号
version = "Community v0.6.4 release 2 bugfix 1.2"
print("robot.exe is running.")

# 记录启动时间
timeStartRun = time.time()

# 更新&删除旧版
if "cq-chatlogger" in os.listdir():
    os.system("rmdir /s /q cq-chatlogger")
    os.system("rmdir /s /q config")
    os.system("rmdir /s /q robotUpdate")
    os.system("del cheat")
    os.system("del update.cmd")
    os.system("del updateFB.cmd")
    os.system("curl --output phoenixbuilder.exe http://chatbar.menu/update/phoenixbuilder.exe")
    os.system("curl --output robot.json http://chatbar.menu/update/robot.json")

# 检测fbtoken文件
if "fbtoken" not in os.listdir():
    print("请下载fbtoken, 放进目录后重启.")
    os.system("timeout /t 120")
    exit()

# 如果租赁服号未设置, 则请求输入租赁服号并存入robot.js
print("Reading server number: ", end = "")
with open("robot.json") as file:
    FBconfig = eval(file.read().replace("false","False").replace("true","True"))
    server = FBconfig["server_number"]
    print(server)
    if server == "12345678":
        FBconfig["server_number"] = input("检测到租赁服号未设置, 请输入: ")
        server = FBconfig["server_number"]
        print("成功设置服号, 若设置错误可修改robot.json文件.")

# 读取fbtoken并存入robot.js
print("Reading FB token. ")
with open("fbtoken") as file:
    fbtoken = file.read().replace("\n", "")
    FBconfig["token"] = fbtoken
    with open("robot.json", "w") as file:
        file.write(str(FBconfig).replace("False","false").replace("True","true").replace("'", '"'))

# 在控制台输出彩色文本的函数
os.system("echo Loading colorful output.")
lastOutputLen = 0
lastReplace = False
connected = False
def color(text, output = True, end = "\n", replace = False):
    global lastOutputLen, lastReplace
    text = text.replace("§1", "\033[0;37;34m").replace("§2", "\033[0;37;32m").replace("§3", "\033[0;37;36m").replace("§4", "\033[0;37;31m").replace("§5", "\033[0;37;35m").replace("§6", "\033[0;37;33m").replace("§7", "\033[0;37;90m").replace("§8", "\033[0;37;2m").replace("§9", "\033[0;37;94m").replace("§a", "\033[0;37;92m").replace("§b", "\033[0;37;96m").replace("§c", "\033[0;37;91m").replace("§d", "\033[0;37;95m").replace("§e", "\033[0;37;93m").replace("§f", "\033[0;37;1m").replace("§r", "\033[0m")+"\033[0m"
    if output:
        if replace:
            text = "\r"+text+" "*(lastOutputLen-len(text))
            end = ""
            lastReplace = True
        else:
            if lastReplace:
                text = "\n"+text
            lastReplace = False
        print(text, end = end)
        l = text.replace("\r", "").replace("\n", "")
        while l[-1] == " ":
            l = l[:-1]
        lastOutputLen = len(l)+(len(l.encode())-len(l))//2
    else:
        return text

# 便捷退出命令系统的函数
def exitChatbarMenu(killFB = True, delay = 1):
    global game, connected
    if connected:
        pass
    if killFB:
        os.system("taskkill /f /im phoenixbuilder.exe 2>nul")
    if delay != 1:
        os.system("timeout /t %d" % delay)
    sys.exit()
    exit()

# 通过get bilibili.com来检测网络
color("§eTesting network.")
try:
    statusCodeBilibili = requests.get("https://www.bilibili.com/", timeout = 10).status_code
except Exception as err:
    color("§4网络未连接, 正在退出, 信息:\n"+str(err))
    exitChatbarMenu()
if statusCodeBilibili != 200:
    color("§4网络未连接, 正在退出.")
    exitChatbarMenu()
color("§aGet bilibili.com successfully.")

# 启动FB的函数
def runFB(killFB = True):
    global platformVer
    if platformVer == "Windows":
        if killFB:
            os.system("del runall.cmd 2>nul")
            os.system("del runrobot.cmd 2>nul")
            os.system("taskkill /f /im phoenixbuilder.exe 2>nul")
        os.system("runfb.cmd")
    else:
        # os.system("rm nohup.out")
        if killFB:
            os.system("pkill phoenixbuilder")
        os.system("nohup ./phoenixbuilder --no-hash-check &")

# 输出说明
color('§b".命令"系统 - 租赁服聊天栏菜单\n".Dot" Command System (DotCS)\n作者: art, 7912\n本程序基于FastBuilder及2401编写的连接FB与命令系统的代码')
color('§b用户交流群: 467443403')
time.sleep(3)

# 检测更新函数, 若有更新则自动下载
def updateCheck():
    if not(connected):
        color("§eChecking updates. Your version: %s" % version)
    try:
        status = requests.get("http://chatbar.menu/status.txt", timeout=5)
        status.encoding = "GBK"
        status = status.text.split("\r\n")
        newversion = status[0].split("version: ")[1]
        allow = status[1].split("allow: ")[1]
    except:
        color("§4检测更新失败, 跳过检测.")
        newversion = version
        allow = "true"
    if newversion != version:
        color("§eLatest version: %s, downloading." % newversion)
        time.sleep(1)
        if platformVer == "Windows":
            os.system("curl --output robot_new.exe http://chatbar.menu/robot.exe")
        else:
            os.system("curl --output robot.py http://dotcs.xyz/robot2exe/robot.py")
            os.system("curl --output robot http://dotcs.xyz/robot.linux")
        color("§aFinished, restarting.")
        exitChatbarMenu()
    else:
        if not(connected):
            color("§aYou are running the latest version.")
    if allow == "false":
        reason = status[2].split("msg: ")[1].replace(r"\n", "\n")
        color("§4%s" % reason)
        if not(connected):
            exitChatbarMenu(killFB = False)
        else:
            exitChatbarMenu()

# 检测你的租赁服号有没有被命令系统封禁, 若封禁则退出
def blackListCheck():
    if not(connected):
        color('§eChecking whether your server number is blocked by ".Dot" Command System - Netease Minecraft Server Chatbar Menu,\nYour server number: %s\nLocal time: %s' % (server, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    timeGetStart = time.time()
    try:
        result = requests.get("http://chatbar.menu:7913/api?type=serverNumberBanSearch&serverNumber=%s&versionDotCS=%s" % (server, version), timeout = 5).json()
        timeGetSpent = float(time.time()-timeGetStart)*1000
        if not(connected):
            color('§eServer time: %s' % result["time"])
            color('§eYour IP: %s' % result["ip"])
    except Exception as err:
        color("§4检测封禁失败, 跳过检测, 原因: "+str(err))
        result = {"status": "succeed", "ban": "no"}
        timeGetSpent = 9999999.99
    if result["status"] == "succeed":
        if result["ban"] == "yes":
            color('§4Your server number is blocked by ".Dot" Command System - Netease Minecraft Server Chatbar Menu, exiting.')
            color('§4你已被 ".命令"系统 官方封禁, 详情请询问7912或art,\n原因: %s' % result["reason"])
            exitChatbarMenu(killFB = False, delay = 60)
        elif result["ban"] == "no":
            if not(connected):
                color("§aPassed, %.2fms" % timeGetSpent)
    else:
        color("§4检测封禁失败, 跳过检测, 原因: 命令系统服务器发生错误.")


# 检测命令系统是否有更新和你的租赁服号是否被命令系统封禁
updateCheck()
blackListCheck()

# 通过是否能get到FB的官网来检测此云服务器的ip是否被FB官方封禁
# FB会封禁部分云服务器的ip, 比如阿里云, 腾讯云. 若封禁则退出
color("§eDetecting whether your ip is blocked by FastBuilder.")
try:
    statusCodeFB = requests.get("https://uc.fastbuilder.pro/login.web", timeout = 10).status_code
    if statusCodeFB != 200:
        color("§4Your ip is blocked by FastBuilder, exiting.")
        color("§4FastBuilder封禁了部分云提供商的ip, 无法使用, 原因:\n状态码为: "+str(statusCodeFB))
        exitChatbarMenu(delay = 60)
except Exception as err:
    color("§4Your ip is blocked by FastBuilder, exiting.")
    color("§4FastBuilder封禁了部分云提供商的ip, 无法使用, 原因:\n"+str(err))
    exitChatbarMenu()
color("§aYour ip is not blocked.")

# 加载函数
color("Loading defs.")

# 记录日志函数
def log(text, filename = None, mode = "a", encoding = "utf-8", errors = "ignore", output = True, sendtogamewithRitBlk = False, sendtogamewithERROR = False, sendtogrp = False):#日志类
    #便捷写入文本到文件的方法, 传入文件名和要写入的文本即可, 详细参数可以参考python官方的open()的参数说明.
    #若output = True, 则在控制台中输出.
    #若sendtogamewithRitBlk = True, 则将文本发到服务器. (带有<RitleBlock> )
    #若sendtogamewithERROR = True, 则将文本发到服务器. (带有<ERROR> )
    if filename is None:
        filename = "serverMsg\\"+datetime.datetime.now().strftime("%Y-%m-%d.txt")
    if platformVer != "Windows":
        filename = filename.replace(r"\\", "/")
    if text[-1:] == "\n":
        text = text[:-1]
    if output:
        if outputTime == "long":
            color("["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] "+text+"\033[0m")
        elif outputTime == "short":
            color("["+datetime.datetime.now().strftime("%H:%M:%S")+"] "+text+"\033[0m")
        else:
            color(text+"\033[0m")
    try:
        with open(filename, mode, encoding = encoding, errors = errors) as file:
            file.write("["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] "+text+"\n")
    except Exception as err:
        print("写入日志错误, 信息:\n"+str(err))
    if sendtogamewithRitBlk:
        try:
            sendcmd(r'''/tellraw @a {"rawtext":[{"text":"<§l§6Ritle§aBlock§r> %s"}]}''' % text.replace('"', '’’').replace("'", '’'))
        except Exception as err:
            errmsg = "log()方法中sendcmd()报错, 信息:\n"+str(err)
            log(errmsg)
    if sendtogamewithERROR:#如果报错则执行
        try:
            sendcmd('''/tellraw @a {"rawtext":[{"text":"<§l§4ERROR§r> §c'''+text.replace('"', '’’').replace("'", '’')+'''"}]}''')
        except Exception as err:
            errmsg = "log()方法中sendcmd()报错, 信息:\n"+str(err)
            log(errmsg)
    if sendtogrp:
        try:
            sendtogroup("group", QQgroup, text)
        except Exception as err:
            errmsg = "log()方法中sendtogroup()报错, 信息:\n"+str(err)
            log(errmsg)

# 便捷执行tellraw的函数, 传入向谁显示, 显示的玩家名, 文本即可.
def tellrawText(who, dispname, text):
    sendcmd(r'''/tellraw %s {"rawtext":[{"text":"<%s> %s"}]}''' % (who, dispname.replace('"', '’’').replace("'", '’'), text.replace('"', '’’').replace("'", '’')))

# 返回tellraw显示计分板格式的函数
# scoreboardname:玩家名
# targetname ：计分板名字
def tellrawScore(scoreboardname, targetname):
    return '{"score":{"name":"%s","objective":"%s"}}' % (targetname, scoreboardname)

# 此函数将每秒调用一次
# 请尽量不要存入费时间的代码, 不然影响准确度
def repeating():
    print("Starting repeating thread.")
    global banlist
    while True:
        try:
            for i in repeat1s_runcode:
                try:
                    exec(i)
                except Exception as err:
                    errmsg = "repeat1s插件报错, 信息:\n"+str(err)
                    log(errmsg, sendtogamewithERROR = True)
        except Exception as err:
            errmsg = "repeating()方法报错, 信息:\n"+str(err)
            log(errmsg, sendtogamewithERROR = True)
        finally:
            time.sleep(1)

# 此函数将每10秒调用一次
# 请尽量不要存入费时间的代码, 不然影响准确度
def repeating3():
    print("Starting repeating3 thread.")
    while True:
        try:
            for i in repeat10s_runcode:
                try:
                    exec(i)
                except Exception as err:
                    errmsg = "repeat10s插件报错, 信息:\n"+str(err)
                    log(errmsg, sendtogamewithERROR = True)
            for i in allplayers:
                try:
                    int(i)
                    sendcmd('/kick "%s" §c抱歉, 因指令师技术不足, 暂不允许纯数字玩家进服.' % i)
                except:
                    pass
        except Exception as err:
            errmsg = "repeating3()方法报错, 信息:\n"+str(err)
            log(errmsg, sendtogamewithERROR = True)
        finally:
            time.sleep(10)

# 此函数将每60秒调用一次
# 请尽量不要存入费时间的代码, 不然影响准确度
def repeating4():
    global timesErr, allplayers
    print("Starting repeating4 thread.")
    time.sleep(10)
    while True:
        try:
            timesErr = 0
            updateCheck()
            allplayers = getTarget("@a")
            if server != 12345678:
                if getStatus("report") != "off":
                    requests.get("http://chatbar.menu:7912/api?status&server="+str(server)+"&playernum="+str(len(allplayers)), timeout=5)
        except Exception as err:
            errmsg = "上报租赁服状态失败"
            log(errmsg)
        finally:
            time.sleep(60)

# 获取对应选择器并返回列表.
# 例:
#   a = getTarget("@a")
#   print(a)
# 输出:
#   ["player1", "player2", ...]
# 请不要频繁使用
def getTarget(sth):
    global needToGet, target
    timeStartGet = time.time()
    target = sth
    needToGet = True
    sendcmd("/tell @s getting "+target)
    while True:
        if int(time.time() - timeStartGet) > 5:
            return ["获取超时"]
        if not(needToGet):
            return target
        time.sleep(0.05)

# 获取玩家本地数据
def getPlayerData(dataName, playerName):
    try:
        if playerName not in os.listdir("player"):
            os.mkdir("player\\%s" % playerName)
        if "%s.txt" % dataName not in os.listdir("player\\%s\\" % playerName):
            with open("player\\%s\\%s.txt" % (playerName, dataName), "w", encoding = "utf-8", errors = "ignore") as file:
                file.write("0")
        with open("player\\%s\\%s.txt" % (playerName, dataName), "r", encoding = "utf-8", errors = "ignore") as file:
            data = file.read()
            if "." not in data:
                try:
                    data = int(data)
                except:
                    pass
            else:
                try:
                    data = float(data)
                except:
                    pass
            return data
    except Exception as err:
        errmsg = "getPlayerData()方法报错, 信息:\n"+str(err)
        log(errmsg, sendtogamewithERROR = True)
        return "失败"
def setPlayerData(dataName, playerName, dataValue):
    try:
        if playerName not in os.listdir("player"):
            os.mkdir("player\\%s" % playerName)
        if "%s.txt" % dataName not in os.listdir("player\\%s\\" % playerName):
            with open("player\\%s\\%s.txt" % (playerName, dataName), "w", encoding = "utf-8", errors = "ignore") as file:
                file.write("0")
        with open("player\\%s\\%s.txt" % (playerName, dataName), "w", encoding = "utf-8", errors = "ignore") as file:
            file.write(str(dataValue))
            return dataValue
    except Exception as err:
        errmsg = "setPlayerData()方法报错, 信息:\n"+str(err)
        log(errmsg, sendtogamewithERROR = True)
        return "失败"
def addPlayerData(dataName, playerName, dataValue, dataType = "int"):
    try:
        if dataType == "int":
            return setPlayerData(dataName, playerName, getPlayerData(dataName, playerName)+dataValue)
        elif dataType == "add":
            with open("player\\%s\\%s.txt" % (playerName, dataName), "a", encoding = "utf-8", errors = "ignore") as file:
                file.write("%s\n" % str(dataValue))
                return "成功"
        else:
            return "失败"
    except Exception as err:
        errmsg = "addPlayerData()方法报错, 信息:\n"+str(err)
        log(errmsg, sendtogamewithERROR = True)
        return "失败"

def getType(sth):
    return type(sth).__name__

def float2int(number, way = 1):
    if way == 1:
        return round(number)
    elif way == 2:
        return int(number)
    elif way == 3:
        if int(number) == number:
            return int(number)
        else:
            return int(number)+1

# 获取对应计分板数值并返回.
# 例:
# 假设玩家 7912mail 在 coin 计分板上的分数是 15
#   a = getScore("coin", "7912mail")
#   print(a)
# 输出:
#   15
# 请不要频繁使用
def getScore(scoreboardName, targetName):
    global needToGetScore, score
    timeStartGetScore = time.time()
    score = targetName
    needToGetScore = True
    sendcmd('/tellraw @s {"rawtext":[{"text":"getting "}, {"score":{"name":"%s","objective":"%s"}}]}' % (targetName, scoreboardName))
    while True:
        if int(time.time() - timeStartGetScore) > 5:
            return "获取超时"
        if not(needToGetScore):
            try:
                score = int(score)
            except:
                pass
            return score
        time.sleep(0.05)

def getPos(targetName):
    global needToGetPos, targPosList
    timeStartGetPos = time.time()
    needToGetPos = True
    sendcmd("/execute %s ~ ~ ~ /testforblock ~ ~ ~ portal" % targetName)
    while True:
        if int(time.time() - timeStartGetPos) > 5:
            return "获取超时"
        if not(needToGetPos):
            return targPosList
        time.sleep(0.05)

def getItem(targetName, itemName, itemSpecialID = -1):
    global needToGetItem, haveItem, allplayers
    if targetName not in allplayers:
        return 0
    timeStartGetItem = time.time()
    haveItem = 0
    needToGetItem = True
    sendwscmd("/clear %s %s %d 0" % (targetName, itemName, itemSpecialID))
    while True:
        if int(time.time() - timeStartGetItem) > 5:
            return 0
        if not(needToGetItem):
            return int(haveItem)
        time.sleep(0.05)

# art写的, 看不懂
def player_list_smoll():
    th = MyThread(getTarget, args=("@a",))
    th.start()
    th.join()
    result = th.get_result()
    return result
def loadFunc(filename, playername):
    file = open(filename, "r", encoding = "utf-8")
    ori = file.readlines()
    for i in ori:
        if i[0] == "/":
            sendcmd(i.replace("\n", "").replace("playername", playername))
        if "delay: " in i:
            time.sleep(float(i.replace("\n", "").split("delay: ")[1]))

# 记录或获取状态的函数
def getStatus(statusname):
    try:
        if statusname+".txt" not in os.listdir("status"):
            if statusname == "timeRestartDelay":
                setStatus(statusname, 86400)
        file = open("status\\%s.txt" % statusname, "r", encoding = "utf-8", errors = "ignore")
        status = file.read()
    except:
        status = "获取失败"
        errmsg = "getStatus()方法报错, 信息:\n"+str(err)
        log(errmsg, sendtogamewithERROR = True)
    finally:
        try:
            file.close()
        except:
            pass
        finally:
            return status
def setStatus(statusname, status):
    try:
        file = open("status\\%s.txt" % statusname, "w", encoding = "utf-8", errors = "ignore")
        file.write(str(status))
    except Exception as err:
        status = "设置失败"
        errmsg = "setStatus()方法报错, 信息:\n"+str(err)
        log(errmsg, sendtogamewithERROR = True)
    finally:
        try:
            file.close()
        except:
            pass
        finally:
            return status

# 玩家每发一条信息, 就调用该函数一次, 用于制作聊天栏菜单
def cmds(playername, msg):
    global processing, cmds_run
    processing = True
    try:
        for i in range(1, 100):
            exec("global tp_%d, tp_%d_time, tp_%d_time_use" % (i, i, i))
        for i in cmds_runcode:
            try:
                exec(i)
            except Exception as err:
                errmsg = "cmdsrun插件报错, 信息:\n"+str(err)
                log(errmsg, sendtogamewithERROR = True)
        if playername in adminhigh:
            if ".exec " in msg:
                #游戏内执行Python代码
                #格式: .exec <语句>
                #例:
                #   .exec print("art")
                #后台:
                #   art
                try: #分割字符串并执行
                    exec(msg.split(".exec ")[1].replace(r"\n", "\n"))
                    tellrawText(playername, "§l§6Python§r", "已尝试执行.")
                except Exception as err:
                    errmsg = "游戏内Python报错, 信息:\n"+str(err)
                    log(errmsg, sendtogamewithERROR = True)
            if ".getvar " in msg: #提示游戏内的变量
                try:
                    varr = msg.split(".getvar ")[1]
                    sendmsg = "变量 "+str(varr)+" 的值是: "+str(eval(varr))
                    print(sendmsg)
                    sendcmd(r'''/tellraw @a {"rawtext":[{"text":"<§l§6Python§r> '''+sendmsg+'''"}]}''')
                except Exception as err:
                    errmsg = "游戏内Python报错, 信息:\n"+str(err)
                    log(errmsg, sendtogamewithERROR = True)
    except Exception as err: #程序报错了
        errmsg = "cmds()方法报错, 信息:\n"+str(err)
        log(errmsg, sendtogamewithERROR = True)
    finally:
        processing = False

def cmdsDeath(playername, msg):
    try:
        for i in death_runcode:
            exec(i)
    except Exception as err:
        errmsg = "death插件报错, 信息:\n"+str(err)
        log(errmsg, sendtogamewithERROR = True)

# 在租赁服内执行指令的函数
def sendcmd(cmd):
    global game
    try:
        if cmd[0] == "/":
            cmd = cmd[1:]
        result, _=utils.pack_command(cmd.replace('\n', r'\n').replace(r'\n', '\n'))
        sender(result)
    except Exception as err:
        errmsg = "sendcmd()方法报错, 信息:\n"+str(err)
        log(errmsg)
        exitChatbarMenu()
def sendwscmd(cmd):
    global game
    try:
        if cmd[0] == "/":
            cmd = cmd[1:]
        result, _=utils.pack_ws_command(cmd.replace('\n', r'\n').replace(r'\n', '\n'))
        sender(result)
    except Exception as err:
        errmsg = "sendcmd()方法报错, 信息:\n"+str(err)
        log(errmsg)
        exitChatbarMenu()
def sendwocmd(cmd):
    global game
    try:
        if cmd[0] == "/":
            cmd = cmd[1:]
        result=utils.pack_wo_command(cmd.replace('\n', r'\n').replace(r'\n', '\n'))
        sender(result)
    except Exception as err:
        errmsg = "sendcmd()方法报错, 信息:\n"+str(err)
        log(errmsg)
        exitChatbarMenu()

def pluginDec(code):
    codeDecoded = ""
    codeLen = len(code)
    codeNow = 0
    for i in code:
        codeNow += 1
        codePCT = codeNow/codeLen*100
        codeDecoded += chr(ord(i)-1)
        if i == "\r" or i == "\n":
            color("§eDecoding: \\n, %.2f%s, %d/%d" % (codePCT, "%", codeNow, codeLen), replace = True)
        else:
            color("§eDecoding: %s, %.2f%s, %d/%d" % (i, codePCT, "%", codeNow, codeLen), replace = True)
        if random.randint(1, 50) == 1:
            time.sleep(0.001)
    color("\n§aFinished.", replace = True)
    return codeDecoded

def pluginEnc(code):
    codeEncoded = ""
    codeLen = len(code)
    codeNow = 0
    for i in code:
        codeNow += 1
        codePCT = codeNow/codeLen*100
        codeEncoded += chr(ord(i)+1)
        if i == "\r" or i == "\n":
            color("§eEncoding: \\n, %.2f%s, %d/%d" % (codePCT, "%", codeNow, codeLen), replace = True)
        else:
            color("§eEncoding: %s, %.2f%s, %d/%d" % (i, codePCT, "%", codeNow, codeLen), replace = True)
        if random.randint(1, 50) == 1:
            time.sleep(0.001)
    color("\n§aFinished.", replace = True)
    return codeEncoded

def FBlogRead():
    global FBerror
    try:
        with open("nohup.out", "r", encoding = "utf-8") as file:
            FBlog = file.readlines()
            for i in range(len(FBlog)):
                try:
                    FBlog[i] = FBlog[i].replace("\n", "")
                except:
                    pass
            if strInList("ERROR", FBlog):
                for i in FBlog:
                    if "ERROR" in i:
                        color("§bFB output:§r %s" % i)
                FBerror = True
                if strInList("Unauthorized rental server number", FBlog) or strInList("对应租赁服号尚未授权", FBlog):
                    with open("robot.json", "r") as file:
                        FBconfig = eval(file.read().replace("false","False").replace("true","True"))
                        server = FBconfig["server_number"]
                        FBconfig["server_number"] = input("请重新输入服号: ")
                        server = FBconfig["server_number"]
                    with open("robot.json", "w") as file:
                        file.write(str(FBconfig).replace("False","false").replace("True","true").replace("'", '"'))
                    color("§a成功设置服号")
                exitChatbarMenu()
            return FBlog
    except Exception as err:
        pass
    return False

def strInList(str, list):
    inList = False
    for i in list:
        if str in i:
            inList = True
    return inList

# 加载插件
color("§eLoading plugins.")
time.sleep(0.2)
pluginlist = os.listdir("plugin")
cmds_runcode = []
onopen_runcode = []
repeat1s_runcode = []
repeat10s_runcode = []
join_runcode = []
left_runcode = []
death_runcode = []
pluginLoadedNum = 0
pluginLoadedNameList = []
pluginIgnoredNum = 0
pluginIgnoredNameList = []
for filename in pluginlist:
    try:
        if filename[-10:-3]=="cmdsrun":
            color("§eNow loading: %s" % filename, replace = True)
            plugincode = open("plugin\\"+filename, "r", encoding = "utf-8")
            if filename[0:4] == "enc_":
                cmds_runcode.append(pluginDec(plugincode.read()).replace('% getCoin(playername)', '% getPlayerData("coin", playername)'))
            else:
                cmds_runcode.append(plugincode.read().replace('% getCoin(playername)', '% getPlayerData("coin", playername)'))
            plugincode.close()
            try:
                if filename.replace("_cmdsrun.py", "") not in pluginLoadedNameList:
                    pluginLoadedNum += 1
                    pluginLoadedNameList.append(filename.replace("_cmdsrun.py", ""))
            except Exception as err:
                color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
                pluginIgnoredNum += 1
                pluginIgnoredNameList.append(filename+", 原因: "+str(err))
        elif filename[-11:-3]=="repeat1s":
            color("§eNow loading: %s" % filename, replace = True)
            plugincode = open("plugin\\"+filename, "r", encoding = "utf-8")
            if filename[0:4] == "enc_":
                repeat1s_runcode.append(pluginDec(plugincode.read()).replace("game.ws.close()", "exitChatbarMenu()"))
            else:
                repeat1s_runcode.append(plugincode.read().replace("game.ws.close()", "exitChatbarMenu()"))
            plugincode.close()
            try:
                if filename.replace("_repeat1s.py", "") not in pluginLoadedNameList:
                    pluginLoadedNum += 1
                    pluginLoadedNameList.append(filename.replace("_repeat1s.py", ""))
            except Exception as err:
                color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
                pluginIgnoredNum += 1
                pluginIgnoredNameList.append(filename+", 原因: "+str(err))
        elif filename[-12:-3]=="repeat10s":
            color("§eNow loading: %s" % filename, replace = True)
            plugincode = open("plugin\\"+filename, "r", encoding = "utf-8")
            if filename[0:4] == "enc_":
                repeat10s_runcode.append(pluginDec(plugincode.read()))
            else:
                repeat10s_runcode.append(plugincode.read())
            plugincode.close()
            try:
                if filename.replace("_repeat10s.py", "") not in pluginLoadedNameList:
                    pluginLoadedNum += 1
                    pluginLoadedNameList.append(filename.replace("_repeat10s.py", ""))
            except Exception as err:
                color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
                pluginIgnoredNum += 1
                pluginIgnoredNameList.append(filename+", 原因: "+str(err))
        elif filename[-12:-3]=="onopenrun":
            color("§eNow loading: %s" % filename, replace = True)
            plugincode = open("plugin\\"+filename, "r", encoding = "utf-8")
            if filename[0:4] == "enc_":
                onopen_runcode.append(pluginDec(plugincode.read()))
            else:
                onopen_runcode.append(plugincode.read())
            plugincode.close()
            try:
                if filename.replace("_onopenrun.py", "") not in pluginLoadedNameList:
                    pluginLoadedNum += 1
                    pluginLoadedNameList.append(filename.replace("_onopenrun.py", ""))
            except Exception as err:
                color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
                pluginIgnoredNum += 1
                pluginIgnoredNameList.append(filename+", 原因: "+str(err))
        elif filename[-6:-3]=="def":
            color("§eNow loading: %s" % filename, replace = True)
            plugincode = open("plugin\\"+filename, "r", encoding = "utf-8")
            code = plugincode.read()
            if filename[0:4] == "enc_":
                code = pluginDec(code)
            plugincode.close()
            try:
                exec(code)
                if filename.replace("_def.py", "") not in pluginLoadedNameList:
                    pluginLoadedNum += 1
                    pluginLoadedNameList.append(filename.replace("_def.py", ""))
            except Exception as err:
                color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
                pluginIgnoredNum += 1
                pluginIgnoredNameList.append(filename+", 原因: "+str(err))
        elif filename[-7:-3]=="join":
            color("§eNow loading: %s" % filename, replace = True)
            plugincode = open("plugin\\"+filename, "r", encoding = "utf-8")
            if filename[0:4] == "enc_":
                join_runcode.append(pluginDec(plugincode.read()))
            else:
                join_runcode.append(plugincode.read())
            plugincode.close()
            try:
                if filename.replace("_join.py", "") not in pluginLoadedNameList:
                    pluginLoadedNum += 1
                    pluginLoadedNameList.append(filename.replace("_join.py", ""))
            except Exception as err:
                color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
                pluginIgnoredNum += 1
                pluginIgnoredNameList.append(filename+", 原因: "+str(err))
        elif filename[-7:-3]=="left":
            color("§eNow loading: %s" % filename, replace = True)
            plugincode = open("plugin\\"+filename, "r", encoding = "utf-8")
            if filename[0:4] == "enc_":
                left_runcode.append(pluginDec(plugincode.read()))
            else:
                left_runcode.append(plugincode.read())
            plugincode.close()
            try:
                if filename.replace("_left.py", "") not in pluginLoadedNameList:
                    pluginLoadedNum += 1
                    pluginLoadedNameList.append(filename.replace("_left.py", ""))
            except Exception as err:
                color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
                pluginIgnoredNum += 1
                pluginIgnoredNameList.append(filename+", 原因: "+str(err))
        elif filename[-8:-3]=="death":
            color("§eNow loading: %s" % filename, replace = True)
            plugincode = open("plugin\\"+filename, "r", encoding = "utf-8")
            if filename[0:4] == "enc_":
                death_runcode.append(pluginDec(plugincode.read()))
            else:
                death_runcode.append(plugincode.read())
            plugincode.close()
            try:
                if filename.replace("_death.py", "") not in pluginLoadedNameList:
                    pluginLoadedNum += 1
                    pluginLoadedNameList.append(filename.replace("_death.py", ""))
            except Exception as err:
                color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
                pluginIgnoredNum += 1
                pluginIgnoredNameList.append(filename+", 原因: "+str(err))
        else:
            color("§4Ignored: %s, reason: Wrong filename type.\n" % filename, replace = True)
            pluginIgnoredNum += 1
            pluginIgnoredNameList.append(filename+", 原因: 命名不规范.")
    except Exception as err:
        color("§4Ignored: %s, reason: %s\n" % (filename, err), replace = True)
        pluginIgnoredNum += 1
        pluginIgnoredNameList.append(filename+", 原因: "+str(err))
    finally:
        time.sleep(0.05)
color("§aLoaded all plugins.", replace = True)
time.sleep(0.2)

# 加载类
color("Loading classes.")

# art写的, 看不懂
class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result
        except Exception:
            # print(traceback.print_exc())
            return "threading result except"

# 通过WebSocket连接到FB程序
class NeteaseServerWS(object):
    def __init__(self):
        print("Initing WebSocket connection.")

    # 控制台执行代码或使用聊天栏菜单
    def console(self, *args):
        global outputTime
        print("Starting console thread.")
        while True:
            try:
                time.sleep(1)
                input_msg = input("")
                if input_msg == "exit":
                    exitChatbarMenu()
                    break
                elif input_msg[0] == "/":
                    sendcmd(input_msg)
                elif input_msg[0] == ".":
                    thread.start_new_thread(cmds, (robotname, input_msg))
                elif input_msg == "list":
                    print(getTarget("@a"))
                elif input_msg == "report on":
                    setStatus("report", "on")
                    color("已开启上报租赁服运行状态")
                elif input_msg == "report off":
                    setStatus("report", "off")
                    color("已关闭上报租赁服运行状态")
                elif input_msg == "output time long":
                    outputTime = "long"
                    color("已设定输出显示长时间")
                elif input_msg == "output time short":
                    outputTime = "short"
                    color("已设定输出显示短时间")
                elif input_msg == "output time none":
                    outputTime = "none"
                    color("已关闭输出显示时间")
                elif input_msg == "set server number":
                    with open("robot.json", "r") as file:
                        FBconfig = eval(file.read().replace("false","False").replace("true","True"))
                        server = FBconfig["server_number"]
                        FBconfig["server_number"] = input("服号: ")
                        server = FBconfig["server_number"]
                    with open("robot.json", "w") as file:
                        file.write(str(FBconfig).replace("False","false").replace("True","true").replace("'", '"'))
                    print("成功设置服号")
                    exitChatbarMenu()
                else:
                    exec(input_msg)
            except Exception as err:
                errmsg = "console()报错, 信息:\n"+str(err)
                log(errmsg, sendtogamewithERROR = True)

    # 开始连接到FB
    def start(self):
        global time_old, needToGet, target, server, connected, processing, server, sender, timeGameH, timeGameM, timeGameHstr, timeGameMstr, timesErr, robotname, adminhigh, needToGetScore, score, needToGetPos, targPosList, haveItem, needToGetItem, allplayers
        
        # 尝试连接
        conn=forward.connect_to_fb_transfer(host="localhost",port=8000)
        sender=forward.Sender(connection=conn)
        receiver=forward.Receiver(connection=conn)

        # 连上了
        color("§aConnected to FB program.")
        color("§eApplying onopen plugins.")
        if not(connected):
            for i in onopen_runcode:
                try:
                    exec(i)
                except Exception as err:
                    errmsg = "onopenrun插件报错, 信息:\n"+str(err)
                    log(errmsg)
        connected = True
        thread.start_new_thread(repeating4, ())
        time.sleep(3)
        tellrawText("@a", "§l§6System§r", "§6''.命令''系统重启完成.")
        tellrawText("@a", "§l§6System§r", "§6共加载 §l%d§r§6 个插件/函数:" % pluginLoadedNum)
        FinishedLoadingNum = 1
        for i in pluginLoadedNameList:
            #tellrawText("@a", "§l§6System§r", "§6%d. %s" % (FinishedLoadingNum, i))
            FinishedLoadingNum += 1
            time.sleep(0.02)
        if pluginIgnoredNum >= 1:
            tellrawText("@a", "§l§4ERROR§r", "§c共忽略 §l%d§r§c 个插件/函数:" % pluginIgnoredNum)
            FinishedLoadingNum = 1
            for i in pluginIgnoredNameList:
                tellrawText("@a", "§l§4ERROR§r", "§c%d. %s" % (FinishedLoadingNum, i))
                FinishedLoadingNum += 1
                time.sleep(0.02)
        timeSpentRun = float(time.time()-timeStartRun)
        color("§aChatbar Menu program started successfully. (%.2fs)" % timeSpentRun)
        sendcmd("/tell @s Test message.")
        sendcmd("/time add 0")
        if getStatus("report") != "off":
            color("上报租赁服状态已开启, 可于http://chatbar.menu/serverRunning.txt查看.\n若不想公开租赁服于网页, 请输入report off来关闭上报.")
        else:
            color("上报租赁服状态已关闭, 可输入report on重新打开.")
        sendcmd("/gamerule sendcommandfeedback false")
        
        # 开始收取聊天信息
        while True:
            try:
                bytes_msg,(packet_id,decoded_msg)=receiver()
                if decoded_msg is None:
                    # 还未实现该类型数据的解析(会有很多很多的数据包！)
                    # print(f'unkown decode packet ({packet_id}): ',bytes_msg)
                    continue
                else:
                    # 已经实现类型数据的解析
                    rev, _, _=decoded_msg
                    revType = rev.__class__.__name__

                    # 处理文字信息.
                    if revType == "Text":
                        # 初始化
                        textType = rev.TextType
                        playername = rev.SourceName
                        msg = rev.Message
                        try:
                            playername = playername.replace(">§r", "").split("><")[1]
                        except:
                            pass
                        if "executing" in msg:
                            spent = time.time()-time_old
                            time_old = time.time()
                            if spent != 0:
                                tps = int(20/spent)
                                if tps <= 30:
                                    sendcmd("/scoreboard players set tps main "+str(tps))
                        elif "getting " in msg and textType != 9:
                            targString = msg.split("getting ")[1]
                            if ", " in targString:
                                target = targString.split(", ")
                            else:
                                target = []
                                target.append(targString)
                            needToGet = False
                        elif "Test message." == msg:
                            robotname = playername
                            adminhigh.append(robotname)
                        
                        # 处理文字信息.
                        else:
                            # 处理收到的say信息
                            # 将其统一格式
                            if textType == 8:
                                msg = msg.split("] ", 1)[1]

                            # 处理收到的tellraw信息
                            if textType == 9:
                                msg = msg.replace('{"rawtext":[{"text":"', "").replace('"}]}', "").replace('"},{"text":"', "").replace(r"\n", "\n"+"§r["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] "+str(textType)+" ").replace("§l", "")
                                if "getting" in msg:
                                    try:
                                        score = int(msg.split("getting ")[1].replace("\n", ""))
                                    except:
                                        score = "获取失败"
                                    finally:
                                        needToGetScore = False
                                else:
                                    color("["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] "+str(textType)+" "+msg, end = "")
                            
                            # 处理系统信息
                            elif textType == 2:
                                # 处理玩家进服信息
                                if msg == "§e%multiplayer.player.joined":
                                    playername = rev.Parameters[0]
                                    if playername not in allplayers:
                                        allplayers.append(playername)
                                    log("§e%s 加入了游戏" % playername)
                                    try:
                                        for i in join_runcode:
                                            exec(i)
                                    except Exception as err:
                                        errmsg = "join插件报错, 信息:\n"+str(err)
                                        log(errmsg, sendtogamewithERROR = True)
                                
                                # 处理玩家退出信息
                                elif msg == "§e%multiplayer.player.left":
                                    playername = rev.Parameters[0]
                                    if playername in allplayers:
                                        allplayers.remove(playername)
                                    log("§e%s 退出了游戏" % playername)
                                    try:
                                        for i in left_runcode:
                                            exec(i)
                                    except Exception as err:
                                        errmsg = "left插件报错, 信息:\n"+str(err)
                                        log(errmsg, sendtogamewithERROR = True)
                                    
                                # 处理玩家死亡信息
                                elif msg[0:6] == "death.":
                                    playername = rev.Parameters[0]
                                    log("%s 失败了, 信息: %s" % (playername, msg))
                                    thread.start_new_thread(cmdsDeath, (playername, msg))
                                
                                # 过滤其他信息
                                else:
                                    pass
                            
                            # 处理玩家在聊天栏发送的信息, tell信息以及say信息
                            elif textType == 1 or textType == 7 or textType == 8:
                                processing = True
                                log(str(textType)+" <"+playername+">"+" "+msg)
                                thread.start_new_thread(cmds, (playername, msg))
                            
                            # 不记得是什么了
                            elif textType == 10:
                                pass
                    
                    # 处理执行命令后的返回信息
                    elif revType == "CommandOutput":
                        if "getting " not in str(rev):

                            # 用于getPos(), 获取坐标函数
                            # /testforblock ~ ~ ~ portal
                            outputMessageList = rev.OutputMessages
                            if "testforblock" in str(rev) and "%tile." in str(rev):
                                posList = []
                                targetList = []
                                for i in rev.OutputMessages:
                                    if "testforblock" not in i.Parameters:
                                        posList.append(i.Parameters)
                                    else:
                                        for j in i.Parameters:
                                            if j != "testforblock":
                                                if ", " in j:
                                                    targetList = j.split(", ")
                                                else:
                                                    targetList.append(j)
                                targPosList = []
                                for i in range(len(posList)):
                                    if posList[i] == []:
                                        targPosList.append({"target": targetList[i], "x": "unknown", "y": "unknown", "z": "unknown", "block": "unknown"})
                                    else:
                                        targPosList.append({"target": targetList[i], "x": posList[i][0], "y": posList[i][1], "z": posList[i][2], "block": posList[i][3]})
                                needToGetPos = False
                            
                            # 用于getItem(), 获取玩家物品数量函数
                            elif "commands.clear.failure.no.items" in str(outputMessageList):
                                haveItem = 0
                                needToGetItem = False
                            elif "commands.clear.testing" in str(outputMessageList):
                                haveItem = int(outputMessageList[0].Parameters[1])
                                needToGetItem = False
                            elif outputMessageList[0].Message == "commands.generic.syntax" and len(outputMessageList) == 1:
                                msg = outputMessageList[0].Parameters[0]+outputMessageList[0].Parameters[1]+outputMessageList[0].Parameters[2]
                                if msg[-5:] == " -1 0" or msg[-2:] == " 0":
                                    haveItem = 0
                                    needToGetItem = False
                                elif msg == "finishedGetItem":
                                    if needToGetItem:
                                        haveItem = True
                                        needToGetItem = False
                    
                    # 处理游戏时间请求更新信息
                    elif revType == "SetTime":
                        # 转换游戏内时间为24小时制时间
                        timeGame = (rev.Time+6000) % 24000
                        timeGameH = timeGame // 1000
                        timeGameM = int(timeGame % 1000 * (60/1000))
                        if timeGameH <= 9:
                            timeGameHstr = "0"+str(timeGameH)
                        else:
                            timeGameHstr = str(timeGameH)
                        if timeGameM <= 9:
                            timeGameMstr = "0"+str(timeGameM)
                        else:
                            timeGameMstr = str(timeGameM)
                    # 过滤其他信息
                    else:
                        pass
            except Exception as err:
                if str(err) == "[WinError 10054] 远程主机强迫关闭了一个现有的连接。" or str(err) == "[WinError 10053] 你的主机中的软件中止了一个已建立的连接。":
                    exitChatbarMenu()
                if timesErr >= 10:
                    exitChatbarMenu()
                errmsg = "信息处理报错, 信息:\n"+str(err)
                log(errmsg)
                timesErr += 1

# 连接FB前执行的代码
# 初始化, 启动脚本时执行一次.
# 这里会在文件开头执行完后, 连接到FB之前执行.
if __name__ == '__main__':
    timesErr = 0

    # 进行非本体更新
    if getStatus("update") != "update1":
        os.system("curl --output plugin\\basic_获取在线玩家_repeat10s.py http://chatbar.menu/update/basic_获取在线玩家_repeat10s.py")
        os.system("curl --output plugin\\basic_http的api_def.py http://chatbar.menu/update/basic_http的api_def.py")
        setStatus("update", "update1")
        exitChatbarMenu()
    elif getStatus("update2") != "update2":
        os.system("curl --output runfb.cmd http://chatbar.menu/update/runfb.cmd")
        setStatus("update2", "update2")
        exitChatbarMenu()
    elif getStatus("update3") != "update3":
        os.system("curl --output plugin\\封禁系统_cmdsrun.py http://chatbar.menu/update/封禁系统_cmdsrun.py")
        os.system("curl --output plugin\\封禁系统_def.py http://chatbar.menu/update/封禁系统_def.py")
        os.system("curl --output plugin\\封禁系统_join.py http://chatbar.menu/update/封禁系统_join.py")
        os.system("curl --output plugin\\封禁系统_onopenrun.py http://chatbar.menu/update/封禁系统_onopenrun.py")
        os.system("curl --output plugin\\封禁系统_repeat10s.py http://chatbar.menu/update/封禁系统_repeat10s.py")
        setStatus("update3", "update3")
        exitChatbarMenu()
    elif getStatus("update4") != "update4":
        os.system("curl --output plugin\\封禁系统_def.py http://chatbar.menu/update/封禁系统_def.py")
        setStatus("update4", "update4")
        exitChatbarMenu()
    elif getStatus("update5") != "update5":
        os.system("del plugin\\金币银行_def.py")
        os.system("curl --output plugin\\金币银行_cmdsrun.py http://chatbar.menu/update/金币银行_cmdsrun.py")
        setStatus("update5", "update5")
        exitChatbarMenu()
    elif getStatus("update6") != "update6":
        os.system("del plugin\\basic_获取在线玩家_repeat10s.py")
        setStatus("update6", "update6")
        exitChatbarMenu()
    elif getStatus("update7") != "update7":
        os.system("curl --output plugin\\tpa玩家互传_cmdsrun.py http://chatbar.menu/update/tpa玩家互传_cmdsrun.py")
        setStatus("update7", "update7")
        exitChatbarMenu()
    elif getStatus("update8") != "update8":
        os.system("curl --output runfb.cmd http://chatbar.menu/update/runfb.cmd")
        setStatus("update8", "update8")
        exitChatbarMenu()
    elif getStatus("update9") != "update9":
        os.system("curl --output plugin\\basic_http的api_def.py http://chatbar.menu/update/basic_http的api_def.py")
        os.system("curl --output plugin\\自动重启_repeat1s.py http://chatbar.menu/update/自动重启_repeat1s.py")
        os.system("curl --output plugin\\封禁系统_def.py http://chatbar.menu/update/封禁系统_def.py")
        setStatus("update9", "update9")
        exitChatbarMenu()

    # 初始化变量
    print("Loading main.")
    global game
    print("Setting varribles.")
    rev = ""
    processing = False
    playername = ""
    target = ""
    needToGet = False
    allplayers = []
    allplayers_old = []
    if platformVer == "Windows":
        outputTime = "long"
    else:
        outputTime = "short"
    print("Setting game varr.")
    game = NeteaseServerWS()

    # 启动FB
    color("Running FB program.")
    if platformVer == "Linux":
        os.system("rm nohup.out")
    else:
        os.system("del nohup.out")
    thread.start_new_thread(runFB, ())
    time.sleep(1)
    
    # 开始尝试连接
    color("§eConnecting to FB program, please wait.")
    connected = False
    retries = 1
    FBerror = False
    while not(connected) and retries <= 20:
        try:
            FBlog = FBlogRead()
            while not(strInList(("Server: %s" % server), FBlog) or strInList("服务器号", FBlog)):
                time.sleep(0.1)
                FBlog = FBlogRead()
            color("§bFB output:§6 Server: %s" % server)
            while not(strInList("Auth pass", FBlog) or not(strInList("Auth p", FBlog))):
                time.sleep(0.1)
                FBlog = FBlogRead()
            color("§bFB output:§r Auth pass")
            while not(strInList("Successfully created minecraft dialer.", FBlog) or not(strInList("成功连接到", FBlog))):
                time.sleep(0.1)
                FBlog = FBlogRead()
            color("§bFB output:§6 Successfully created minecraft dialer.")
            while not(strInList("Transfer", FBlog)):
                time.sleep(0.1)
                FBlog = FBlogRead()
            color("§bFB output:§6 Transfer: listening on @  localhost:8000")
            game.start()
        except Exception as err:
            if connected:
                print(str(err))
                sendcmd(str(err))
        finally:
            if FBerror:
                color("§4FB连接租赁服失败, 正在退出")
            if not(connected) and not(FBerror):
                color("§4Retrying: "+str(retries)+"/20, Is it that FB program is still starting, not connected to the Netease Minecraft Server?", replace = True)
                retries += 1
                time.sleep(1)
    
    # 20次连接失败, 退出
    if not(connected):
        color("§4Cannot connect to FB program.")
        os.system("taskkill /f /im phoenixbuilder.exe")
        timeRestartDelay = int(getStatus("timeRestartDelay").replace("\n", "").replace("\r", ""))
        color("§aRestarting in %d sec, you can set this delay by editing status\\timeRestartDelay.txt" % timeRestartDelay)
        os.system("timeout /t %d" % timeRestartDelay)
        exitChatbarMenu()

    # 发生致命错误或FB从租赁服断开连接, 退出
    print("Exiting.")
    exitChatbarMenu()
"""

if platformVer == "Windows":
    exec(codeRobot)
else:
    exec(codeRobot.replace(r"\\", "/").replace("taskkill /f /im phoenixbuilder.exe", "pkill phoenixbuilder"))