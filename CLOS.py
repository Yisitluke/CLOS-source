import json
import subprocess
import time
from getpass import getpass
import hashlib
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def clear():
    subprocess.run(("cls" if os.name == "nt" else "clear"), shell=True)

def IdentifyJson(data):
    return json.dumps(data)

def IdentifyPython(data):
    return json.loads(data)

def IdentifyHash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def CompareHash(given, target):
    if IdentifyHash(given) == target:
        return True
    else:
        return False

def DefineUserData(username, passwd):
    return {
    "-username-": username,
    "-password-": IdentifyHash(passwd),
    "-settings-": {
        "-vmax-": 3
        }
    }

def DefineUserFile(usrdat):
    if not os.path.exists(os.path.join("system", "users", f"{usrdat['-username-']}.json")):
        Save(usrdat, os.path.join("system", "users", f"{usrdat['-username-']}.json"))
    else:
        print(rReturn(2, "BootLoader:UserAlreadyExists", warnN=False))

def ValidateUserData(data):
    a = DefineUserData("Username", "Password")
    for i in a:
        if not i in data:
            return False
        if isinstance(a[i], dict):
            for aS in a[i]:
                if not aS in data[i]:
                    return False
    return True

def rReturn(level, restype, warnN, x1=None, x2=None):
    if level == -1:
        level = "OPRND;"
    if level == 0:
        level = "SUCCE;"
    if level == 1:
        level = "WARN;"
    if level == 2:
        level = "ERR;"

    if restype == "BootLoader:UserNotFound":
        restype = f"USER '{x1.lower()}' WAS NOT FOUND."
    if restype == "BootLoader:UserAlreadyExists":
        restype = "USER IS ALREADY TAKEN."
    if restype == "BootLoader:InvalidUsernameInput":
        restype = f"USERNAME '{x1}' IS NOT VALID."
    if restype == "OprSys:VerificationSuccess":
        restype = "VERIFICATION CORRECT."
    if restype == "OprSys:VerificationSubFailure":
        restype = "INCORRECT GIVEN PASSWORD."
    if restype == "OprSys:VerificationFailure":
        restype = "VERIFICATION INCORRECT."
    if restype == "OprSys:UnknownCommand":
        restype = f"'{x1}' IS UNKNOWN."
    if restype == ".:InvalidInput":
        restype = "INVALID INPUT."

    return f"{level} {restype}{(' CONTINUE THIS OPERATION?' if warnN else '')}"

def rYesNo():
    a = input("")
    if a.lower() == "y" or a.lower() == "yes":
        b = True
    elif a.lower() == "n" or a.lower() == "no":
        b = False
    else:
        return rReturn(2, ".:InvalidInput", warnN=False)
    return b, a

def Save(usrdatPort, usrpatPort):
    with open(usrpatPort, "w") as f:
        f.write(IdentifyJson(usrdatPort))

def Load(usrpatPort):
    with open(usrpatPort, "r") as f:
        usrdat = IdentifyPython(f.read())
    return usrdat

def IdentifyUser(target):
    a = (False, None, None)
    for i in list(os.scandir(os.path.join("system", "users"))):
        ref = Load(i.path)
        if not ValidateUserData(ref):
            continue
        try:
            if ref["-username-"] == target:
                a = (True, ref, i.path)
                break
        except KeyError:
            continue
    return a

def DisplayUser():
    for i in list(os.scandir(os.path.join("system", "users"))):
        ref = Load(i.path)
        if not ValidateUserData(ref):
            continue
        try:
            print(f"{ref['-username-']}")
        except KeyError:
            continue
        

def PathEnsure():
    if not os.path.exists("system"):
        os.mkdir("system")
    if not os.path.exists(os.path.join("system", "users")):
        os.mkdir(os.path.join("system", "users"))
    ## if not os.path.exists(os.path.join("system", "actions")): 
        ## os.mkdir(os.path.join("system", "actions"))
        # ^ coming soon... ^

def SystemShutdown(doesSave, exitstatus, usrdatPort=None, usrpatPort=None):
    if doesSave:
        Save(usrdatPort, usrpatPort)
    sys.exit(exitstatus)

def vobSyntax(VersionOrBuild, Version=None, Build=None, VersionX=None, BuildX=None):
    if VersionOrBuild == "v":
        struct = f"v{Version} | Version-{VersionX}"
    if VersionOrBuild == "b":
        struct = f"b{Build} | testingVersion-{BuildX}"
    if VersionOrBuild == "DEVNULL":
        struct = None
    return struct





class BootMenu:
    def __init__(self):
        PathEnsure()
        time.sleep(2.5)
        self.bMenu()

    def SelectUser(self):
        print("BootLoader | Boot")
        DisplayUser()
        print("")
        direct = input("")
        clear()
        (a, usrdat, usrpat) = IdentifyUser(direct)
        if a:
            OprSys(usrdat, usrpat)
        else:
            print(rReturn(2, "BootLoader:UserNotFound", warnN=False, x1=direct))
            time.sleep(2)
            clear()

    def CreateUser(self):
        print("Username\n")
        username = input("")
        clear()
        if not username.isalpha() or len(username) > 15:
            print(rReturn(2, "BootLoader:InvalidUsernameInput", warnN=False, x1=username))
            time.sleep(2)
            clear()
        else:
            username = username.lower()
            print("Password\n")
            passwd = getpass("")
            DefineUserFile(DefineUserData(username, passwd))
            clear()

    def bMenu(self):
        while True:
            print("BootLoader | Main Menu")
            print("0: Shutdown")
            print("1: Boot")
            print("2: Create User Account\n")
            opt = input("")
            if opt == "0":
                SystemShutdown(False, 0)
            elif opt == "1":
                clear()
                self.SelectUser()
            elif opt == "2":
                clear()
                self.CreateUser()
            else:
                clear()
                print(rReturn(2, ".:InvalidInput", warnN=False))
                time.sleep(2)
                clear()



class OprSys:
    def __init__(self, usrdat, usrpat):
        self.UserData = usrdat
        self.UserPath = usrpat
        v = vobSyntax("DEVNULL")
        b = vobSyntax("b", Build="0.0.1", BuildX="CoreTest")

        self.SystemInfo = {
        "-version-": (v if b is None else "[ > TESTING VERSION < ]"),
        "-build-": b
        }

        self.cmdR = {
        "clear": clear,
        "shutdown": self.WinixSystemShutdown,
        "userinfo": self.WinixShowUserInfo,
        "sysinfo": self.WinixShowSystemInfo
        }

        self.Verify()

    def Verify(self):
        vcur = 0
        vtot = False
        while vcur < self.UserData["-settings-"]["-vmax-"]:
            print("Password Verification\n")
            inp = getpass("")
            clear()
            if CompareHash(inp, self.UserData["-password-"]):
                print(rReturn(0, "OprSys:VerificationSuccess", warnN=False))
                time.sleep(2)
                vtot = True
                clear()
                break
            else:
                vcur += 1
                print(rReturn(1, "OprSys:VerificationSubFailure", warnN=False))
                time.sleep(2)
                clear()
        if vtot:
            self.System()
        else:
            clear()
            print(rReturn(2, "OprSys:VerificationFailure", warnN=False))
            time.sleep(2)
            clear()

    def WinixSystemShutdown(self):
        SystemShutdown(True, 0, self.UserData, self.UserPath)

    def WinixShowUserInfo(self):
        print(f"Username: {self.UserData['-username-']}")
        print(f"Settings:\n    |Max Verification Attempts: {self.UserData['-settings-']['-vmax-']}")

    def WinixShowSystemInfo(self):
        print("Operating System Name (full): Command Line Operand System")
        print("Operating System Name (short): CLOS")
        print(f"Operating System Version: {self.SystemInfo['-version-']}")
        if not self.SystemInfo["-build-"] is None:
            print(f"Operating System Testing Version: {self.SystemInfo['-build-']}")
        print("Author and Creator: Lucas (Yisitluke on GitHub)")

    def WinixShell(self, command):
        tokens = command.split(";")
        commandBase = tokens[0]
        parameters = tokens[1:]
        execute = self.cmdR.get(commandBase)
        if execute:
            execute(*parameters)
        else:
            print(rReturn(2, "OprSys:UnknownCommand", warnN=False, x1=commandBase))

    def System(self):
        print("Command Line Operand | Winix\n")
        while True:
            command = input("")
            print("")
            self.WinixShell(command)
            print("")

BootMenu()
