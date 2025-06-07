# Table of Contents

1. **What is CLOS?**
2. **Menus**
3. **How Users Work**
4. **Available Commands**
5. **Versioning System**

---

## 1, What is CLOS?

Command Line Operand System, or CLOS, is a CLI-based operating system emulator. This program includes:

+ Boot menu
+ User creation and saved data
+ User hashed passwords
+ Four commands

..thats it. This entire project is HIGHLY a work-in-progress, so there are very few things to do.

---

## 2, Menus

There are several menus, this section will tell you how to create a user and use the Winix shell.

First, how do you even run the system?: Just open a terminal where you placed the `CLOS.py` file; if you're on Linux, run:

```bash
python3 CLOS.py
```
If on Windows:
```bash
python CLOS.py
```

or, even better (for Linux):

```bash
clear && python3 CLOS.py
```
And for Windows:

```bash
cls && python CLOS.py
```
(use `Clear-Host` for PowerShell, and `cls` for Command Prompt.)

The script will automatically create a `system` directory required for the system. Ensure all of the scripts have read and write permissions, so it can read user data and create the system directory.

Now, you will be presented with this in the terminal:

```
BootLoader
0: Shutdown
1: Boot
2: Create User Account
```

0 will close the system.

1 will boot into a user (which won't work, there aren't any users yet).

2 will create a user (we want this).

Select 2. You will be prompted for username and password. Your user will use these.

Then, select 1 (Boot). Your username will appear. You now have an account!

---

## 3, How Users Work

Users are JSON files stored in `system  >  users`. Each user currently have the following format:
```
-username-: [username]
-password-: [a very long hash]
-settings-:
    -vmax- 3
```
This, as of this manual, is the current format of users. Very simple. `-username-` is your.. username, `-password-` is a hashed.. password, and `-vmax-` is your total amount of verification attempts before it kicks you back to the BootLoader.

---

## 4, Available Commands

There are four commands:

`clear`: Clears the screen.

`userinfo`: Shows your username and vmax.

`sysinfo`: Shows OS full name, short name, version and/or testing version.

`shutdown`: Saves data and closes the system.

---

## 5, Versioning System

There are two types of versioning:

+ **Version**: These are official releases, denoted as 'v`X.Y.Z`.'
+ **Builds**: These are testing stages, like "dev" versions. This is denoted as 'b`X.Y.Z`.' These are going to be a thousand times more common, as versions are far away from now.

Both follow the X.Y.Z formatting, where:

+ **X** is the major version.
+ **Y** is the minor version.
+ **Z** is the patch-fix/very minor version.

Be note that versions wont be present for a while, so builds will be expected.

---

Have fun!
