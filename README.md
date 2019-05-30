# What's toolbox
Toolbox is a collection of small useful and often used scripts to avoid rewriting 
## Modules:
- **`Downloader.py`**
    - makes it easy to download from URLS
    - shows progress in terminal
    - makes file names writeable (checks for invalid characters)
    - change file name or download path

## Requirements
- **`requests`**

---
## How to use systemwide

### **Linux**
Add toolbox to PYTHONPATH

If you're using bash (on a Mac or GNU/Linux distro), add this to your ~/.bashrc

    export PYTHONPATH="${PYTHONPATH}:/path/to/toolbox"

[Stack Overflow answer](https://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath)
#
### **Windows**

Under system variables create a new Variable called PythonPath. In this variable I have 

    C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Lib\lib-tk;C:\other-folders-on-the-path

![alt text](https://i.stack.imgur.com/ZGp36.png "Logo Title Text 1")

[Stack Overflow answer](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages)

---
## TO DO
- use urlib instead requests to make it python standalone
- ~~add unit tests~~