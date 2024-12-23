import json, os
from tkinter import messagebox as msg, filedialog as prompt

rootDir = os.path.dirname(os.path.abspath(__file__))
appdataDir = os.path.join(os.getenv('APPDATA'), "Furglitch", "MO2SE")
tempDir = os.path.join(os.getenv('TEMP'), "Furglitch", "MO2SE")
resourceDir = os.path.join(rootDir, "resources")
iconDir = os.path.join(resourceDir, "icon.png")
saved = True
categories = {}
startColor = "#000000"
endColor = "#ffffff"
gradient = []
header = ''
theme = ''
themeAccent = ''


# Menu Functions
def fileNew():
    global startColor, endColor
    if msg.askyesno("Confirm", "Are you sure you want to create a new file? This will clear all current data."):
        categories.clear()
        startColor = "#000000"
        endColor = "#ffffff"
    global saved; saved = True
    
def fileSave():
    global categories, startColor, endColor
    path = prompt.asksaveasfilename(filetypes=[("JSON", "*.json")])
    data = {"categories": categories, "gradient": {"startColor": startColor, "endColor": endColor}}
    with open(path, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)
    global saved; saved = True
        
def fileOpen():
    global categories, startColor, endColor
    path = prompt.askopenfilename(filetypes=[("JSON", "*.json")])
    with open(path, "r") as f:
        data = json.load(f)
        categories = data["categories"]
        startColor = data["gradient"]["startColor"]
        endColor = data["gradient"]["endColor"]
    global saved
    saved = True


# Button Functions
def sepAdd(type, name, parent_category):
    if type == "cat":
        if name not in categories:
            categories[name] = {"id": None, "sub": {}}
        else: warn(1, name)
    elif type == "sub":
        if parent_category in categories:
            if name not in categories[parent_category]["sub"]:
                categories[parent_category]["sub"][name] = {"id": None}
            else: warn(2, name, parent_category)
        else: warn(3, parent_category)
    else: error(1)
    global saved; saved = False

def sepRemove(type, name, children, parent):
    if type == "cat":
        if children: warn(4, name)
        else:
            if name in categories:
                del categories[name]
            else: warn(3, name)
    elif type == "sub":
        if parent in categories and name in categories[parent]["sub"]:
            del categories[parent]["sub"][name]
        else: warn(3, parent)
    else: error(1)
    global saved; saved = False
    
def outputGen():
    path = prompt.askdirectory()
    profilePath = os.path.join(path, 'profiles', 'default')
    modsPath = os.path.join(path, 'mods')
    if not os.path.exists(profilePath): os.makedirs(profilePath)
    f = open(profilePath + '/modlist.txt', "w")
    f.close()
    if not os.path.exists(modsPath): os.makedirs(modsPath)
    with open(os.path.join(profilePath + '/modlist.txt'), "r+") as l:
        lines = l.readlines()
        l.seek(0, 0)
        i = 0; j=0
        for category, details in categories.items():
            catSep = headerGet("start", header) + category+ headerGet("end", header) + '_separator'
            os.mkdir(os.path.join(modsPath, catSep))
            with open(os.path.join(modsPath, catSep, 'meta.ini'), 'w') as meta:
                meta.write(f"[General]\ncolor={gradient[j]}")
            lines.insert(0, "+"+catSep+'\n')
            j += 1
            for subcategory in details["sub"]:
                i += 1
                subSep = str(i)+'. '+subcategory+'_separator'
                os.mkdir(os.path.join(modsPath, subSep))
                lines.insert(0, "+"+subSep+'\n')
        l.writelines(lines)


# Settings Functions
def themeGet(type, theme=None):
    output = ''
    with open(os.path.join(resourceDir, 'themes.json')) as f:
        data = json.load(f)
        if type == "name":
            output = list(data.keys())
        elif type == "theme":
            output = data[theme]
        elif type == "color":
            output = data[theme][type]
    return output

def headerGet(type, header=None):
    output = ''
    with open(os.path.join(resourceDir, 'headers.json')) as f:
        data = json.load(f)
        if type == "name":
            output = list(data.keys())
        elif type == "start" or type == "end":
            output = data[header][type]
    return output

def settingsGet():
    global theme, themeAccent, header
    if not os.path.exists(appdataDir):
        os.makedirs(appdataDir)
    if not os.path.exists(appdataDir + '/MO2se.json'):
        with open(os.path.join(appdataDir, 'MO2SE.json'), "w") as f:
            data = {"theme": {"name": 'Nord', "accent": 'Blue'}, "header": 'Bracket'}
            json.dump(data, f, sort_keys=True, indent=4)
            f.close
    else:
        with open(os.path.join(appdataDir, 'MO2SE.json'), "r") as f:
            data = json.load(f)
            theme = data["theme"]["name"]
            themeAccent = data["theme"]["accent"]
            header = data["header"]

def settingsCheck():
    global theme, themeAccent, header
    with open(os.path.join(appdataDir, 'MO2SE.json'), "r") as f:
        data = json.load(f)
        if theme == data["theme"]["name"] and themeAccent == data["theme"]["accent"] and header == data["header"]: return True
        else: return False
        
# TODO add example lists

def settingsSave():
    global theme, header, themeAccent
    with open(os.path.join(appdataDir + '/MO2SE.json'), "w") as f:
        data = {"theme": {"name": theme, "accent": themeAccent}, "header": header}
        json.dump(data, f, sort_keys=True, indent=4)
    
# Gradient Processing
def hexRGB(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def stepRGB(start, end, steps):
    gradient = []
    for i in range(steps):
        t = i / (steps - 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        gradient.append((r, g, b))
    return gradient

def rgbHex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def gradientGet():
    global startColor, endColor, gradient
    startRGB = hexRGB(startColor)
    endRGB = hexRGB(endColor)
    gradRGB = stepRGB(startRGB, endRGB, len(categories))
        
    gradient = [rgbHex(rgb) for rgb in gradRGB]

# Error Handling
def warn(code, text, text2=None):
    match code:
        case 1: msg.showwarning("Warning", "Category "+text+" already exists")
        case 2: msg.showwarning("Warning", "Subcategory "+text+" already exists in Category "+text2)
        case 3: msg.showwarning("Warning", "Parent Category "+text+" does not exist")
        case 4: msg.showwarning("Warning", "Cannot remove Category "+text+" with existing Subcategories")
        
def error(code, text=None):
    match code:
        case 1: msg.showerror("Error", "Invalid Type\n\nYou shouldn't be seeing this. Please submit an issue on GitHub.")
    
def settingsPrompt():
    return msg.askyesno("Settings Not Saved", "You've adjusted your settings but haven't saved! Are you sure you want to exit?")
    
def filePrompt():
    return msg.askyesno("Changes Not Saved", "You've adjusted your separator list but haven't saved! Are you sure you want to exit?")
