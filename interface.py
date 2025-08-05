import backend as bck
import tkinter as tk
from tkinter import ttk, colorchooser as cc
import webbrowser as web
import sys
from PIL import Image, ImageTk

ui = None
settings = None
def closeProgram():
    if settings.state() != 'withdrawn': closeSettings()
    if bck.saved != True:
        if not bck.filePrompt(): return
    bck.log.info("Closing Program")
    sys.exit()
def closeSettings():
    if not bck.settingsCheck():
        if bck.settingsPrompt():
            settings.withdraw()
            bck.log.info("Closed Settings")
            return False
    else:
        settings.withdraw()
        bck.log.info("Closed Settings")
    return True

# Main Window
ui = tk.Tk()
ui.title("MO2 Separator Generator")
ui.geometry("550x525+100+100")
ui.minsize(750,500)
ui.resizable(True, True)
ui.protocol("WM_DELETE_WINDOW", lambda: closeProgram())

# Settings Menu
settings = tk.Toplevel(ui)
settings.withdraw()
settings.title("Settings")
settings.geometry('250x200')
settings.resizable(False, False)

# Set icon
if bck.osType == "nt":
    ui.iconbitmap(bck.iconDir)
    settings.iconbitmap(bck.iconDir)
else:
    img = Image.open(bck.iconDir)
    ico = ImageTk.PhotoImage(img)
    ui.wm_iconphoto(True, ico)
    settings.wm_iconphoto(True, ico)

themeFrame = ttk.Frame(settings, padding=(0,0,10,5))
themeChoiceFrame = ttk.Frame(themeFrame)
ttk.Label(themeChoiceFrame, text="Theme: ").pack(side='left', anchor='center')
themeBox = ttk.Combobox(themeChoiceFrame, values=bck.themeGet("name"), textvariable=bck.theme)
themeBox.current(0)
themeBox.pack(side = 'left', anchor = 'center')
themeBox.bind("<<ComboboxSelected>>", lambda event: applyTheme(themeBox.get(), colorBox.get()))
themeChoiceFrame.pack(side = 'top', anchor="center")
colorChoiceFrame = ttk.Frame(themeFrame)
ttk.Label(colorChoiceFrame, text="Accent: ").pack(side='left', anchor='center')
colorBox = ttk.Combobox(colorChoiceFrame, values=['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple'], textvariable=bck.themeAccent)
colorBox.current(4)
colorBox.pack(side = 'left', anchor = 'center')
colorBox.bind("<<ComboboxSelected>>", lambda event: applyTheme(themeBox.get(), colorBox.get()))
colorChoiceFrame.pack(side = 'top', anchor="center")
themeFrame.pack(side = 'top', anchor="center")

headerFrame = ttk.Frame(settings, padding=(0,0,5,5))
headerChoiceFrame = ttk.Frame(headerFrame)
ttk.Label(headerChoiceFrame, text="Category Header: ").pack(side='left', anchor='center')
headerBox = ttk.Combobox(headerChoiceFrame, values=bck.headerGet("name"))
headerBox.bind("<<ComboboxSelected>>", lambda event: updateHeaderLabel(headerBox.get()))
headerBox.current(0)
headerBox.pack(side = 'left', anchor = 'center')
headerChoiceFrame.pack(side = 'top', anchor = 'center')
headerLabel = ttk.Label(headerFrame, text='')
headerLabel.pack(side = 'top', anchor = 'center')
headerFrame.pack(side = 'top', anchor = 'center')
def updateHeaderLabel(header):
    bck.header = header
    bck.startHeader = bck.headerGet("start", header)
    bck.endHeader = bck.headerGet("end", header)
    headerLabel.config(text=bck.startHeader + ' CATEGORY ' + bck.endHeader)

casingFrame = ttk.Frame(settings, padding=(0,0,5,10))
casingCatFrame = ttk.Frame(casingFrame)
ttk.Label(casingCatFrame, text="Category Casing: ").pack(side='left', anchor='center')
casingCatBox = ttk.Combobox(casingCatFrame, values=['Unchanged', 'Capitalize', 'UPPER', 'lower'])
casingCatBox.bind("<<ComboboxSelected>>", lambda event: bck.casingSet("cat",casingCatBox.get()))
casingCatBox.current(0)
casingCatBox.pack(side = 'left', anchor = 'center')
catCase = casingCatFrame.pack(side = 'top', anchor = 'center')
casingSubFrame = ttk.Frame(casingFrame)
ttk.Label(casingSubFrame, text="Subcategory Casing: ").pack(side='left', anchor='center')
casingSubBox = ttk.Combobox(casingSubFrame, values=['Unchanged', 'Capitalize', 'UPPER', 'lower'])
casingSubBox.bind("<<ComboboxSelected>>", lambda event: bck.casingSet("sub", casingSubBox.get()))
casingSubBox.current(0)
casingSubBox.pack(side = 'left', anchor = 'center')
casingSubFrame.pack(side = 'top', anchor = 'center')
casingFrame.pack(side = 'top', anchor = 'center')

sbuttonFrame = ttk.Frame(settings)
ttk.Button(sbuttonFrame, text="Save", command=lambda: bck.settingsSave()).pack(side="left")
ttk.Button(sbuttonFrame, text="Exit", command=lambda: closeSettings()).pack(side="right")
sbuttonFrame.pack(side="bottom", anchor="center")
settings.protocol("WM_DELETE_WINDOW", lambda: closeSettings())

# Navigation Bar
nav = tk.Menu(ui)
fileBar = tk.Menu(nav, tearoff=0)
fileBar.add_command(label="New", command=lambda: fileNew())
fileBar.add_command(label="Open", command=lambda: fileOpen())
fileBar.add_command(label="Save", command=lambda: bck.fileSave())
fileBar.add_separator()
fileBar.add_command(label="Settings", command=lambda: showSettings())
fileBar.add_separator()
fileBar.add_command(label="Exit", command=lambda: closeProgram())
nav.add_cascade(label="File", menu=fileBar)
editBar = tk.Menu(nav, tearoff=0)
editBar.add_command(label="Collapse All", command=lambda: treeCollapse())
editBar.add_command(label="Expand All", command=lambda: treeExpand())
nav.add_cascade(label="View", menu=editBar)
exampleBar = tk.Menu(nav, tearoff=0)
nav.add_cascade(label="Examples", menu=exampleBar)
settingsBar = tk.Menu(nav, tearoff=0)
aboutBar = tk.Menu(nav, tearoff=0)
aboutBar.add_command(label="License", command=lambda: web.open_new_tab("https://choosealicense.com/licenses/gpl-3.0/"))
aboutBar.add_command(label="GitHub", command=lambda: web.open_new_tab("https://github.com/Furglitch/ModOrganizer-SeparatorGenerator"))
nav.add_cascade(label="About", menu=aboutBar)
ui.config(menu=nav)

# Navigation Functions
def showSettings():
    global ui, settings
    settings.deiconify()
    x = ui.winfo_x() + (ui.winfo_width() // 2) - (settings.winfo_width() // 2)
    y = ui.winfo_y() + (ui.winfo_height() // 2) - (settings.winfo_height() // 2)
    settings.geometry("+%d+%d" % (x,y))
    bck.log.info("Opened Settings")
def fileNew():
    bck.fileNew()
    updateList()
def fileOpen():
    bck.fileOpen()
    updateList()
def treeCollapse():
    for category in bck.categories: separatorList.item(bck.categories[category]["id"], open=False)
def treeExpand():
    for category in bck.categories: separatorList.item(bck.categories[category]["id"], open=True)

# Separator List
listFrame = ttk.Frame(ui)
separatorList = ttk.Treeview(listFrame, columns=("Name"), show="tree headings", selectmode='browse')
separatorList.heading("Name", text="Name", anchor="n",)
separatorList.column("#0", width=20, stretch="no")
separatorList.column("Name", stretch="yes")
separatorList.pack(side="top", fill='both', expand=True)
scroll = ttk.Scrollbar(separatorList, orient='vertical', command=separatorList.yview)
scroll.place(relx=0.971, rely=0.0, relheight=1, relwidth=0.03)
separatorList.configure(yscrollcommand=scroll.set)
listFrame.pack(side="top", fill='both', expand=True)
def updateList():
    expanded_categories = set()
    for category_id in separatorList.get_children():
        if separatorList.item(category_id, 'open'): expanded_categories.add(separatorList.item(category_id, 'values')[0].strip())
    separatorList.delete(*separatorList.get_children())
    for category in bck.categories:
        categoryID = separatorList.insert("", "end", text="", values=(category,))
        bck.categories[category]["id"] = categoryID
        for subcategory in bck.categories[category]["sub"]:
            subcategoryID = separatorList.insert(categoryID, "end", text="", values=(f"\u00A0\u00A0\u00A0\u00A0{subcategory}",))
            bck.categories[category]["sub"][subcategory]["id"] = subcategoryID
        if category in expanded_categories: separatorList.item(categoryID, open=True)
    subBox.config(values=list(bck.categories.keys()))
    updateColor("start", bck.startColor)
    updateColor("end", bck.endColor)
    bck.log.info("Updated separator list")

# Buttons
buttonFrame = ttk.Frame(ui)
ttk.Button(buttonFrame, text="Move ↑", width=7, command=lambda: moveSeparator("up")).pack(side="left", fill="y")
ttk.Button(buttonFrame, text="Move ↓", width=7, command=lambda: moveSeparator("down")).pack(side="right", fill="y")
ttk.Button(buttonFrame, text="Generate Files", command=lambda: bck.outputGen()).pack(side="bottom", fill='x')
ttk.Button(buttonFrame, text="Remove Separator", command=lambda: remSeparator()).pack(side="bottom", fill="x")
ttk.Button(buttonFrame, text="Add Separator", command=lambda: addSeparator(categoryType.get(), nameBox.get())).pack(side="bottom", fill="x")
buttonFrame.pack(side="bottom", fill='x')
def addSeparator(type, name):
    if type == "sub": parentCategory = subBox.get()
    else: parentCategory = None
    bck.sepAdd(type, name, parentCategory)
    updateList()
    if type == "sub" and parentCategory:
        parentID = bck.categories[parentCategory]["id"]
        separatorList.item(parentID, open=True)
        newID = bck.categories[parentCategory]["sub"][name]["id"]
    else: newID = bck.categories[name]["id"]
    separatorList.selection_set(newID)
def remSeparator():
    selection = separatorList.selection()
    if selection:
        item = separatorList.item(selection, "values")[0].strip()
        parent = separatorList.parent(selection)
        children = separatorList.get_children(selection)
        if children: child = True
        else: child = False
        if parent:
            bck.sepRemove("sub", item, child, separatorList.item(parent, "values")[0].strip())
        else:
            bck.sepRemove("cat", item, child, None)
        if subBox.get() == item:
            subBox.set('')
    updateList()
def moveSeparator(direction):
    selection = separatorList.selection()
    if selection:
        parentID = separatorList.parent(selection)
        index = separatorList.index(selection)
        siblings = separatorList.get_children(parentID)
        if direction == "up" and index > 0:
            separatorList.move(selection, parentID, index - 1)
            bck.log.info(f"Moved {separatorList.item(selection, 'values')[0].strip()} up")
        elif direction == "down" and index < len(siblings) - 1:
            separatorList.move(selection, parentID, index + 1)
            bck.log.info(f"Moved {separatorList.item(selection, 'values')[0].strip()} down")
        separatorList.selection_set(selection)
    new_categories = {}
    for category_id in separatorList.get_children():
        category_name = separatorList.item(category_id, "values")[0].strip()
        new_categories[category_name] = {"id": category_id, "sub": {}}
        for subcategory_id in separatorList.get_children(category_id):
            subcategory_name = separatorList.item(subcategory_id, "values")[0].strip()
            new_categories[category_name]["sub"][subcategory_name] = {"id": subcategory_id}
    bck.categories = new_categories

        
# Input Frame
inputFrame = ttk.Frame(ui)
inputFrame.pack(side="bottom", pady=10, fill='x')
typeFrame = ttk.Frame(inputFrame)
typeFrame.pack(anchor="w", side="left", padx=15)
catFrame = ttk.Frame(typeFrame)
categoryType = tk.StringVar(value="cat")
catCheck = ttk.Radiobutton(catFrame, text="Category", variable=categoryType, value="cat", command=lambda: changeLabel("cat"))
catCheck.pack(anchor="w", side="left")
catFrame.pack(anchor="w", side="top")
subFrame = ttk.Frame(typeFrame)
subCheck = ttk.Radiobutton(subFrame, text="Subcategory of ", variable=categoryType, value="sub", command=lambda: changeLabel("sub"))
subCheck.pack(anchor="w", side="left")
subBox = ttk.Combobox(subFrame, width=15, values=list(bck.categories.keys()))
subBox.pack(anchor="w", side="left")
subFrame.pack(anchor="w", side="top")
textFrame = ttk.Frame(typeFrame)
nameLabel = ttk.Label(textFrame, text="Category Name: ", width=18, anchor="w")
nameLabel.pack(anchor="w", side="left")
nameBox = ttk.Entry(textFrame, width=18)
nameBox.pack(anchor="w", side="left")
textFrame.pack(anchor="w", side="top")
def changeLabel(var):
    if var == "cat":
        nameLabel.config(text="Category Name: ")
    elif var == "sub":
        nameLabel.config(text="Subcategory Name: ")

# Gradient Selection
gradientFrame = ttk.Frame(inputFrame)
gradientFrame.pack(anchor="e", side="right", padx=15)
startColor = tk.StringVar(value=bck.startColor)
endColor = tk.StringVar(value=bck.endColor)
ttk.Label(gradientFrame, text="Category Separator Gradient").pack(anchor="center", side="top")
gradientStartFrame = ttk.Frame(gradientFrame)
gradientStartFrame.pack(anchor="e", side="top")
gradientEndFrame = ttk.Frame(gradientFrame)
gradientEndFrame.pack(anchor="e", side="bottom")
startIndicator = tk.Label(gradientStartFrame, bg=startColor.get(), width=2, height=1, highlightbackground="gray", highlightthickness=1)
startIndicator.pack(anchor="w", side="left")
startLabel = ttk.Label(gradientStartFrame, text=f"Start Color: {startColor.get()}", width=20)
startLabel.pack(anchor="center", side="left")
ttk.Button(gradientStartFrame, text="Choose Start Color", command=lambda: chooseColor("start"), width=20).pack(anchor="e", side="left")
endIndicator = tk.Label(gradientEndFrame, bg=endColor.get(), width=2, height=1, highlightbackground="gray", highlightthickness=1)
endIndicator.pack(anchor="w", side="left")
endLabel = ttk.Label(gradientEndFrame, text=f"End Color: {endColor.get()}", width=20)
endLabel.pack(anchor="center", side="left")
ttk.Button(gradientEndFrame, text="Choose End Color", command=lambda: chooseColor("end"), width=20).pack(anchor="e", side="left")
def chooseColor(type):
    color = cc.askcolor()[1]
    if color is not None:
        updateColor(type, color)

def updateColor(type, color):
    if color is None:
        if type == "start":
            color = "#000000"
        elif type == "end":
            color = "#ffffff"
    if type == "start":
        startIndicator.config(bg=color)
        startLabel.config(text=f"Start Color: {color}")
        bck.startColor = color
    elif type == "end":
        endIndicator.config(bg=color)
        endLabel.config(text=f"End Color: {color}")
        bck.endColor = color
    bck.gradientGet()
    bck.log.info(f"Updated {type} color to {color}")

def applyTheme(theme_name, color):
    theme = bck.themeGet("theme", theme_name)
    global nav
    match color:
        case "Red": accent = theme['accent1']
        case "Orange": accent = theme['accent2']
        case "Yellow": accent = theme['accent3']
        case "Green": accent = theme['accent4']
        case "Blue": accent = theme['accent5']
        case "Purple": accent = theme['accent6']
    style = ttk.Style()
    style.theme_use('default')
    ui.config(bg=theme["background1"])
    settings.config(bg=theme["background1"])
    style.configure('TFrame', background=theme['background1'])
    style.configure('TLabel', background=theme['background1'], foreground=theme['foreground1'])
    style.configure('TButton', background=theme['background2'], foreground=theme['foreground1'])
    style.map('TButton', background=[('active', accent)])
    style.configure('TEntry', fieldbackground=theme['background3'], foreground=theme['foreground1'])
    style.configure('TRadiobutton', background=theme['background1'], foreground=theme['foreground1'])
    style.map('TRadiobutton', background=[('active', accent)])
    style.configure('TCombobox', background=theme['background2'], arrowcolor=theme['foreground1'], fieldbackground=theme['background3'], foreground=theme['foreground1'])
    style.configure('Treeview', background=theme['background3'], fieldbackground=theme['background2'], foreground=theme['foreground1'])
    style.configure('Heading', background=theme['background1'], foreground=theme['foreground1'])
    style.map('Treeview', background=[('selected', theme['background4'])])
    style.map('Heading', background=[('active', accent)])
    style.configure('Vertical.TScrollbar', background=theme['background2'], troughcolor=theme['background1'], arrowcolor=theme['foreground1'])
    style.map('Vertical.TScrollbar', background=[('active', accent)])
    bck.theme = themeBox.get()
    bck.themeAccent = colorBox.get()
    bck.log.info(f"Applied theme {theme_name} with accent {color}")
    
    

bck.settingsGet()
themeBox.set(bck.theme)
colorBox.set(bck.themeAccent)
headerBox.set(bck.header)
casingCatBox.set(bck.catCasing)
casingSubBox.set(bck.subCasing)
bck.exampleGet(exampleBar, separatorList, subBox, startIndicator, endIndicator, startLabel, endLabel)
applyTheme(bck.theme, bck.themeAccent)
updateHeaderLabel(headerBox.get())
ui.mainloop()