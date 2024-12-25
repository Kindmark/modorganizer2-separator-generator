import json, os, sys, logging as log
from datetime import datetime as dt
from tkinter import messagebox as msg, filedialog as prompt

rootDir = os.path.dirname(os.path.abspath(__file__))
initDir = os.path.dirname(os.path.abspath(sys.argv[0]))
appdataDir = os.path.join(os.getenv('APPDATA'), "Furglitch", "MO2SE")
logDir = os.path.join(appdataDir, 'logs', f'{dt.now().strftime('%Y-%m-%d %H%M%S')}.log')
resourceDir = os.path.join(rootDir, "resources")
iconDir = os.path.join(resourceDir, "icon.ico")

saved = True
categories = {}
examples = {}
startColor = "#000000"
endColor = "#ffffff"
gradient = []
header = 'Bracket'
theme = 'Nord'
themeAccent = 'Blue'
catCasing = 'Unchanged'
subCasing = 'Unchanged'

# Logging
if not os.path.exists(os.path.join(appdataDir, 'logs')): os.makedirs(os.path.join(appdataDir, 'logs'))
open(logDir, "w").close()
log.basicConfig(
    filename=logDir,
    level=log.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log.info("MO2SE Started")

# Menu Functions
def fileNew():
    global startColor, endColor
    if msg.askyesno("Confirm", "Are you sure you want to create a new file? This will clear all current data."):
        categories.clear()
        startColor = "#000000"
        endColor = "#ffffff"
        log.info("Data cleared for new file")
    global saved; saved = True
    
def fileSave():
    global categories, startColor, endColor
    path = prompt.asksaveasfilename(initialdir=initDir, filetypes=[("JSON", "*.json")], defaultextension=".json")
    if path:
        data = {"categories": categories, "gradient": {"startColor": startColor, "endColor": endColor}}
        with open(path, "w") as f: json.dump(data, f, indent=4)
        global saved; saved = True
        log.info(f"File Saved: {path}")
        
def fileOpen(path=None):
    global categories, startColor, endColor, saved
    if not saved:
        if not msg.askyesno("Changes Not Saved", "You've adjusted your separator list but haven't saved!\nAre you sure you want to open this file?"):
            return
    if path is None: path = prompt.askopenfilename(initialdir=initDir, filetypes=[("JSON", "*.json")], defaultextension=".json")
    if path:
        with open(path, "r") as f:
            data = json.load(f)
            categories.clear()
            categories.update(data["categories"])
            startColor = data["gradient"]["startColor"]
            endColor = data["gradient"]["endColor"]
        saved = True
        log.info(f"File Opened: {path}")
    else: return

def exampleGet(bar, list, subBox, startIndicator, endIndicator, startLabel, endLabel):
    global examples
    path = os.path.join(resourceDir, "examples")
    for file in os.listdir(path):
        filepath = os.path.join(path,file)
        if file.endswith('.json') and os.path.isfile(filepath):
            bar.add_command(label=file.removesuffix(".json"), command=lambda filepath=filepath: exampleOpen(filepath, list, subBox, startIndicator, endIndicator, startLabel, endLabel))
            log.info(f"Example Found: {file.removesuffix('.json')}")

def exampleOpen(path, tree, subBox, startIndicator, endIndicator, startLabel, endLabel):
    global startColor, endColor, categories, saved
    if not saved:
        if not msg.askyesno("Unsaved Changes", "You have unsaved changes. Are you sure you want to open an example?"):
            return
    saved = True
    log.info(f"Example Selected: {os.path.basename(path).removesuffix('.json')}")
    fileOpen(path)
    expanded_categories = set()
    for category_id in tree.get_children():
        if tree.item(category_id, 'open'): expanded_categories.add(tree.item(category_id, 'values')[0].strip())
    tree.delete(*tree.get_children())
    for category, details in categories.items():
        categoryID = tree.insert("", "end", text="", values=(category,))
        categories[category]["id"] = categoryID
        for subcategory in details["sub"]:
            subcategoryID = tree.insert(categoryID, "end", text="", values=(f"\u00A0\u00A0\u00A0\u00A0{subcategory}",))
            categories[category]["sub"][subcategory]["id"] = subcategoryID
        if category in expanded_categories: tree.item(categoryID, open=True)
    subBox.config(values=list(categories.keys()))
    startIndicator.config(bg=startColor)
    startLabel.config(text=f"Start Color: {startColor}")
    endIndicator.config(bg=endColor)
    endLabel.config(text=f"End Color: {endColor}")

# Button Functions
def sepAdd(type, name, parent_category=None):
    if type == "cat":
        if name not in categories:
            categories[name] = {"id": None, "sub": {}}
            log.info(f"Category Added: {name}")
        else: warn(1, name)
    elif type == "sub" and parent_category is not None:
        if parent_category in categories:
            if name not in categories[parent_category]["sub"]:
                categories[parent_category]["sub"][name] = {"id": None}
                log.info(f"Subcategory Added: {name} in Category {parent_category}")
            else: warn(2, name, parent_category)
        else: warn(3, parent_category)
    else: error(1, type)
    global saved; saved = False

def sepRemove(type, name, children, parent):
    if type == "cat":
        if children: warn(4, name)
        else:
            if name in categories:
                del categories[name]
                log.info(f"Category Removed: {name}")
            else: warn(3, name)
    elif type == "sub":
        if parent in categories and name in categories[parent]["sub"]:
            del categories[parent]["sub"][name]
            log.info(f"Subcategory Removed: {name} in Category {parent}")
        else: warn(3, parent)
    else: error(1, type)
    global saved; saved = False
    
def outputGen():
    global gradient
    gradientGet()
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
            catSep = headerGet("start", header) + applyCasing("cat", category) + headerGet("end", header) + '_separator'
            os.mkdir(os.path.join(modsPath, catSep))
            with open(os.path.join(modsPath, catSep, 'meta.ini'), 'w') as meta:
                meta.write(f"[General]\ncolor={gradient[j]}")
            lines.insert(0, "+"+catSep+'\n')
            j += 1
            for subcategory in details["sub"]:
                i += 1
                subSep = str(i)+'. ' + applyCasing("sub", subcategory) + '_separator'
                os.mkdir(os.path.join(modsPath, subSep))
                lines.insert(0, "+"+subSep+'\n')
        l.writelines(lines)
    log.info(f"Output Generated at {path}")


# Settings Functions
def themeGet(type, theme=None):
    output = ''
    with open(os.path.join(resourceDir, 'themes.json')) as f:
        data = json.load(f)
        if type == "name":
            output = list(data.keys())
            log.info(f"Themes Loaded: {output}")
        elif type == "theme":
            output = data[theme]
            log.info(f"Theme {theme} info loaded: {output}")
        elif type == "color":
            output = data[theme][type]
            log.info(f"Theme {theme} color loaded: {type} - {output}")
    return output

def headerGet(type, header=None):
    output = ''
    with open(os.path.join(resourceDir, 'headers.json')) as f:
        data = json.load(f)
        if type == "name":
            output = list(data.keys())
            log.info(f"Headers Loaded: {output}")
        elif type == "start" or type == "end":
            output = data[header][type]
            log.info(f"Headers {header} loaded: {type} - {output}")
    return output

def applyCasing(type, text):
    global catCasing, subCasing
    if type == "cat":
        if catCasing == "Capitalize": return text.title()
        elif catCasing == "UPPER": return text.upper()
        elif catCasing == "lower": return text.lower()
        else: return text
    if type == "sub":
        if subCasing == "Capitalize": return text.title()
        elif subCasing == "UPPER": return text.upper()
        elif subCasing == "lower": return text.lower()
    else: return text
    
def casingSet(type, case):
    global catCasing, subCasing
    if type == "cat":
        catCasing = case
        log.info(f"Category Casing Set: {case}")
    if type == "sub":
        subCasing = case
        log.info(f"Subcategory Casing Set: {case}")

def settingsGet():
    global theme, themeAccent, header, catCasing, subCasing
    if not os.path.exists(os.path.join(appdataDir, 'MO2SE.json')):
        data = {"theme": {"name": theme, "accent": themeAccent}, "header": header, "casing": {"cat": catCasing, "sub": subCasing}}  
        f = open(os.path.join(appdataDir, 'MO2SE.json'), "w")
        json.dump(data, f, indent=4)
        f.close()
        log.info("Default Settings File Created")
    else:
        with open(os.path.join(appdataDir, 'MO2SE.json'), "r") as f:
            data = json.load(f)
            if data["theme"]["name"] in themeGet("name"): theme = data["theme"]["name"]
            else: theme = "Nord"
            if data["theme"]["accent"] in ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']: themeAccent = data["theme"]["accent"]
            else: themeAccent = "Blue"
            if data["header"] in headerGet("name"): header = data["header"]
            else: header = "Bracket"
            if data["casing"]["cat"] in ['Unchanged', 'Capitalize', 'UPPER', 'lower']: catCasing = data["casing"]["cat"]
            else: catCasing = "Unchanged"
            if data["casing"]["sub"] in ['Unchanged', 'Capitalize', 'UPPER', 'lower']: subCasing = data["casing"]["sub"]
            else: subCasing = "Unchanged"
            log.info(f"Settings Loaded: Theme {theme}, ThemeAccent {themeAccent}, Header {header}, Category Casing {catCasing}, Subcategory Casing {subCasing}")

def settingsCheck():
    global theme, themeAccent, header, catCasing, subCasing
    with open(os.path.join(appdataDir, 'MO2SE.json'), "r") as f:
        data = json.load(f)
        if theme == data["theme"]["name"] and themeAccent == data["theme"]["accent"] and header == data["header"] and catCasing == data["casing"]["cat"] and subCasing == data["casing"]["sub"]:
            log.info("Settings match saved settings")
            return True
        else:
            log.info("Settings do not match saved settings")
            return False

def settingsSave():
    global theme, header, themeAccent, casing
    with open(os.path.join(appdataDir + '/MO2SE.json'), "w") as f:
        data = {"theme": {"name": theme, "accent": themeAccent}, "header": header, "casing": {"cat": catCasing, "sub": subCasing}}  
        json.dump(data, f, sort_keys=True, indent=4)
    log.info(f"Settings Saved: Theme {theme}, Theme Accent {themeAccent}, Header {header}, Category Casing {catCasing}, Subcategory Casing {subCasing}")
    
# Gradient Processing
def hexRGB(hex):
    hex = hex.lstrip('#')
    log.info(f"Hex Converted to RGB: {hex}")
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def stepRGB(start, end, steps):
    if steps == 1: return [start]
    gradient = []
    for i in range(steps):
        t = i / (steps - 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        gradient.append((r, g, b))
    log.info(f"Generated RGB Gradient from {startColor} to {endColor} with {steps} steps")
    return gradient

def rgbHex(rgb):
    log.info(f"RGB Converted to Hex: {rgb}")
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def gradientGet():
    global startColor, endColor, gradient
    if len(categories) == 0: return
    startRGB = hexRGB(startColor)
    endRGB = hexRGB(endColor)
    gradRGB = stepRGB(startRGB, endRGB, len(categories))
        
    gradient = [rgbHex(rgb) for rgb in gradRGB]
    log.info(f"Gradient Generated: {gradient}")

# Error Handling
def warn(code, text, text2=None):
    match code:
        case 1:
            msg.showwarning("Warning", f"Category already exists: {text}")
            log.warning(f"Category Already Exists: {text}")
        case 2:
            msg.showwarning("Warning", f"Subcategory already exists: {text} in Category {text2}")
            log.warning(f"Subcategory Already Exists: {text} in Category {text2}")
        case 3:
            msg.showwarning("Warning", f"Category {text} does not exist")
            log.warning(f"Category Does Not Exist: {text}")
        case 4:
            msg.showwarning("Warning", f"Cannot remove Category with existing subcategories: {text}")
            log.warning(f"Cannot Remove Category with Existing Subcategories: {text}")
        
def error(code, text=None):
    match code:
        case 1:
            msg.showerror("Error", "Invalid Type\n\nYou shouldn't be seeing this. Please submit an issue on GitHub.")
            log.error(f"Invalid Type: {text}")
    
def settingsPrompt():
    log.info("Prompt: Settings Not Saved")
    return msg.askyesno("Settings Not Saved", "You've adjusted your settings but haven't saved! Are you sure you want to exit?")
    
def filePrompt():
    log.info("Prompt: Changes Not Saved")
    return msg.askyesno("Changes Not Saved", "You've adjusted your separator list but haven't saved! Are you sure you want to exit?")
