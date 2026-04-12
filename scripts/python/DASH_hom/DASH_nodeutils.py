import hou

def arg_default(var, default):
    """ Sentinel default value. returns default if the variable is None """
    return default if var is None else var

def default_hda_color(node):
    color = hou.Color((1, .9, .8)) #peachy yellow
    node.setColor(color)

def vopvex_color(sel=None, colors=None, rainbow=None, keep_color=None, comment=None, vops=None, wrangles=None):
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
    vops = arg_default(vops, True)
    wrangles = arg_default(wrangles, True)


    if comment is None:
        comment = 0    
    for node in sel:        
        if isinstance(node, hou.SopNode) and node.type().name() == "attribwrangle" and wrangles :            
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

        if isinstance(node, hou.SopNode) and node.type().name() == "attribvop" and vops :            
            runon = node.parm("bindclass").eval()            
            if node.isEditableInsideLockedHDA() :
                if ((node.color() == hou.Color((.8, .8, .8)) or node.color() == hou.Color((.839, .839, .839)) ) if keep_color else 1) :
                    if rainbow:    
                        color = hou.Color((0,1,1))
                        color.setHSV((runon/5.0*290+0,.6,.9))
                    else:                    
                        color = hou.Color(colors[runon])
                    node.setColor(color)

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

def createNodeHelp():
    """
    Create Houdini Help markup from a template. Fill out the appropriate information.
    """
    def nQuot(amount):
        return "\""*amount
            
    def nEqls(amount):
        return "="*amount

    def nLine(amount):
        return "\n"*amount

    def nSpace(amount):
        return " "*amount

    # Template generator for a particular ParmTemplateGroup
    def allParmTemplates(group_or_folder, multiparm = None):
        if multiparm == None: multiparm = 1
        for parm_template in group_or_folder.parmTemplates():
            yield parm_template

            if(multiparm) :
                if (parm_template.type() == hou.parmTemplateType.Folder):
                    for sub_parm_template in allParmTemplates(parm_template):
                        yield sub_parm_template
            else:
                if (parm_template.type() == hou.parmTemplateType.Folder and
                parm_template.isActualFolder()):
                    for sub_parm_template in allParmTemplates(parm_template):
                        yield sub_parm_template

    # Build Parameter template text helper.
    def parmTempHelp(parmTemp, siblings=None):
        """Creates wiki text for both single and menu parameters."""
        arg_default(siblings,"") 
        help = parmTemp.label() + ":\n"
        help += siblings
        help += nSpace(4) + "#id: " + parmTemp.name() + "\n"
        help += nSpace(4) + "Description for " + str(parmTemp.label()) + nLine(1)
        
        if(hasattr(parmTemp, "menuLabels")):
            parmlabels = parmTemp.menuLabels()
            if parmlabels:
                for label in parmlabels:
                    help += nLine(1) + nSpace(4) + label + ":" + nLine(1)
                    help += nSpace(8) + "Menu option description." + nLine(1)
        help += nLine(1)
        return help

    def pageicon(path):
        """Generate icon path for #icon property from HDA definition icon path."""
        contexts = ["OBJ_", "SOP_", "VOP_", "LOP_", "CHOP_", "COP2_", "LOP", "SHOP_", "TOP_", "ROP_"]
        contexts_matches = [path.startswith(context) for context in contexts]

        if "opdef:" in path and "?" in path:
            path = "opdef:.?" + path.split("?")[1]
        elif sum(contexts_matches)>0:
            path = "/".join(path.split("_"))
        return path
        
    sel = hou.selectedNodes()
    tmpls = []
    if(len(sel)==1):
        node = sel[0]
        tp = node.type()
        df = tp.definition()
        if df == None:
            print("Select a HDA, please!")  # Selection is not HDA
            return ""
        assetname = tp.name()
        assetnamecat = tp.nameWithCategory()
        slashid = assetnamecat.find("/")
        name = assetnamecat[slashid+1:]
        name = name.split("::")[0]
        description = tp.description().strip("- - - ") # DASH PACKAGE SPECIFIC. SHOULD NOT INTERFERE

        # Asset Name, Description and Overview
        help = ""
        #help += "#icon: opdef:.?DASH-{op}-icon.svg".format(op=name) + nLine(1) # DASH SPECIFIC
        help += "#icon: " + pageicon(df.icon()) + nLine(1)
        help += nLine(1) + nEqls(1) + " " + description + " " + nEqls(1) + nLine(2)       # = Operator Name =
        help += nQuot(3) + "Quick asset description." + nQuot(3) + nLine(2)               # """Quick asset description."""
        help += nEqls(2) + " Overview " + nEqls(2) + nLine(2)                             # == Overview ==
        help += "Explanation of the node's purpose and operation." + nLine(2)             #  Overview explanation
 
        # Inputs
        # FOR A VOP NODE
        if(isinstance(node, hou.VopNode)):
            names = node.inputNames()
            if(names):
                help += "@inputs" + nLine(2)
                for name in names:
                    help += "`" + name + "`:" + nLine(1)
                    help += nSpace(4) + "What the input is for." + nLine(2)
        # FOR OTHER CATEGORIES
        else:
            labels = node.inputLabels()
            if(labels):
                help += "@inputs" + nLine(2)
                for label in labels:
                    help += label + ":" + nLine(1)
                    help += nSpace(4) + "What the input is for." + nLine(2)

        # Parameters                                                                       # @parameters
        group = node.parmTemplateGroup()
        tmpls = allParmTemplates(group)
        labels  = [tmpl.label() + "_folder" if isinstance(tmpl, hou.FolderParmTemplate) else tmpl.label() for tmpl in allParmTemplates(group)] # ADD '_folder' to label in list to guarantee disambiguation with normal parms
        labels.append("__empty_LAST") # Add this to label list to have valid index in last entry.
        
        isLasts = [labels[i] != labels[i+1] for i in range(len(labels)-1)]

        if group.entries() :
            help += "@parameters" + nLine(2)
            index = -1
            previous = ""
            for t in tmpls :
                index += 1
                if isinstance(t, hou.SeparatorParmTemplate): # Ignore Separators
                    previous = ""
                    continue

                if isinstance(t, hou.FolderParmTemplate):
                    fldtype = t.folderType().name()
                    if fldtype == "MultiparmBlock" :
                        help += parmTempHelp(t)
                    elif fldtype == "Tabs" :
                        help += nEqls(2) + t.label().title() + nEqls(2) + nLine(2)
                    else:
                        help += nEqls(3) + t.label().title() + nEqls(3) + nLine(2)
                else:   
                    isLast = isLasts[index]
                    if isLast:
                        new = parmTempHelp(t, siblings = previous)
                        previous = ""
                        help += new # Commit new parameter
                    else:
                        previous += nSpace(4) + "#id: " + t.name() + nLine(1) # add repeated

        # Outputs
        # FOR A VOP NODE                                                                             # @outputs
        if(isinstance(node, hou.VopNode)): 
            names = node.outputNames()
            if(names):
                help += "@outputs" + nLine(2)
                for name in names:
                    help += "`" + name + "`:" + nLine(1)
                    help += nSpace(4) + "#id:" + name + nLine(1) 
                    help += nSpace(4) + "What the output is for." + nLine(2)
        # FOR OTHER CATEGORIES
        else:                               
            labels = node.outputLabels()
            if(labels):
                help += "@outputs" + nLine(2)
                for label in labels:
                    help += label + ":" + nLine(1)
                    help += nSpace(4) + "What the output is for." + nLine(2)

        return help
    else:
        print("Select a single node, please!")  # Selection is empty or with more than one node.
        return ""
