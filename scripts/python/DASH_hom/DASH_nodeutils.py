import hou

def arg_default(var, default):
    """ Sentinel default value. returns default if the variable is None """
    return default if var is None else var

def default_hda_color(node):
    color = hou.Color((1, .9, .8)) #peachy yellow
    node.setColor(color)

def attwrangle_color(sel=None, colors=None, rainbow=None, keep_color=None, comment=None):
    """
    Change color of attribute wrangle SOPs according to the Run class. 'colors':list of vector RGB. 'rainbow', 'keep_color', 'comment': boolean.
    """
    sel = arg_default(sel, hou.selectedNodes())
    if len(sel) == 0: #Apply to all if nothing is selected
        sel = hou.node("/obj/").allSubChildren()
    colors = arg_default(colors, [(.55, .45, .3), (.765, 1, .576), (0.48, 0.75, 1), (0.75, 0.55, 0.95), (0.354, 0.304, 0.354)])
    rainbow = arg_default(rainbow, False)
    keep_color = arg_default(keep_color, True)
    comment = arg_default(comment, False)

    if comment is None:
        comment = 0    
    for node in sel:        
        if isinstance(node, hou.SopNode) and node.type().name() == "attribwrangle" :            
            runon = node.parm("class").eval()            
            if node.isEditableInsideLockedHDA() :
                if ((node.color() == hou.Color((.8, .8, .8)) or node.color() == hou.Color((.839, .839, .839)) ) if keep_color else 1) :
                    if rainbow:    
                        color = hou.Color((0,1,1))
                        color.setHSV((runon/5.0*290+0,.6,.9))
                    else:                    
                        color = hou.Color(colors[runon])
                    node.setColor(color)

                # Comment
                if comment:
                    firstline = node.parm("snippet").eval().split("\n")[0]
                    if "//" in firstline or "/*" in firstline:
                        comment = node.comment()                    
                        firstline = firstline.replace("//", "").replace("/*", "").lstrip()
                        if firstline not in comment:
                            comment = comment if comment == "" else comment + "\n" 
                            node.setComment(comment + firstline)
                            node.setGenericFlag(hou.nodeFlag.DisplayComment,True)

def delete_parm_channels(sel=None, defaults=None):
    """
    Delete nodes's parameter channels. Animation, etc,
    """
    sel = arg_default(sel, hou.selectedNodes())
    revert_defaults = arg_default(defaults, False)
    
    for node in sel:
        parms = node.parms()
        for parm in parms:
            parm.deleteAllKeyframes()
            if revert_defaults:
                parm.revertToDefaults()


def sticky_notes_io():
    """
    Export and Import of sticky notes text. Original purpose: Spell/Grammer check them.
    """
    import fnmatch

    ## GET ALL CURRENT STICKIES IN THE SCENE
    root = hou.node("/")
    all = root.allSubChildren(True, False)
    nets = [net for net in all if net.isNetwork() is True and net.isLockedHDA() is False]
    allitems = [net.allItems() for net in nets]
    allitems = list(sum(allitems, ()))
    stickies = [sticky for sticky in allitems if fnmatch.fnmatch(sticky.name(), "__stickynote*")]
    stickiespaths = [sticky.path() for sticky in stickies]

    # GET CURRENT TEXT IN CLIPBOARD
    text = hou.ui.getTextFromClipboard()

    # CHECK HOW MANY CURRENT STICKIES ARE MISSING IN THAT TEXT
    missing = []
    for path in stickiespaths:
        notfirst = text.find(path+"\n") != 0
        notother = "\n-----\n"+path+"\n" not in text
        
        if notfirst and notother:
            missing += [path]
       
    ## EXPORT IF: text is emprty OR there's no info about the existing stickies; Export.
    itsempty = text == ""
    allmissing = len(missing) == len(stickiespaths)

    if len(stickies) == 0:
        print(" ")
        print("No available Stickies.")    

    elif itsempty or allmissing: # EXPORT

        invalid = ""
        if(text != ""):
            invalid = "(Invalid Clipboard)"
        
        stickies = [sticky.path() + "\n" + sticky.text() for sticky in stickies]
        text = "\n-----\n".join(stickies)
        hou.ui.copyTextToClipboard(text)

        # END MESSAGE FOR EXPORT
        stickiescount = len(stickies)
        print(" ")
        print(f"▲EXported Stickies: {stickiescount}. {invalid}")
        
    else: # IMPORT
        print(" ")
        clipstickies = text.split("\n-----\n")
        successful = 0
        failedpaths = [] # PATHS IMPORT WITHOUT MATCHING STICKY
        sucessfullpaths = [] # PATHS SUCCESSFULLY IMPORTED
        for sticky in clipstickies:
            lines = sticky.split("\n")
            path = lines[0]
            item = hou.item(path)
            if item:
                content = "\n".join(lines[1:])
                item.setText(content)
                successful += 1
                sucessfullpaths += [path]
            else:
                failedpaths += [path]
            
        
        # EMPTY CLIPBOARD
        hou.ui.copyTextToClipboard("")
        
        # END MESSAGE FOR IMPORT
        print(f"▼IMported Stickies: {successful}. (Clipboard Emptied)")
        
        # REPORT MISSING MESSAGE
        #missing = [stickiespath for stickiespath in stickiespaths if stickiespath not in sucessfullpaths]
        if missing:
            missingtext = "\n".join(missing)
            print("EXISTING STICKIES WITHOUT INFO IN IMPORT:\n" + missingtext)

        # REPORT FAILED PATHS
        if failedpaths:
            failedpathstext = "\n".join(failedpaths)
            print("INFO IN IMPORT FOR NONEXISTING STICKIES:\n" + failedpathstext)
