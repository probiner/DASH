import hou

def default(var, default):
    """ Sentinel default value. returns default if the variable is None """
    return default if var is None else var

def default_hda_color(node):
    color = hou.Color((1, .9, .8)) #peachy yellow
    node.setColor(color)

def attwrangle_color(sel=None, colors=None, rainbow=None, keepcolor=None, comment=None):
    """
    Change color of attribute wrangle SOPs according to the Run class. 'colors':list of vector RGB. 'rainbow', 'keepcolor', 'comment': boolean.
    """
    sel = default(sel, hou.selectedNodes())
    if len(sel) == 0: #Apply to all if nothing is selected
        sel = hou.node("/obj/").allSubChildren()
    colors = default(colors, [(.55, .45, .3), (.765, 1, .576), (0.48, 0.75, 1), (0.75, 0.55, 0.95), (0.354, 0.304, 0.354)])
    rainbow = default(rainbow, 0)
    keepcolor = default(keepcolor, 1)
    comment = default(comment, 0)

    if comment is None:
        comment = 0    
    for node in sel:        
        if isinstance(node, hou.SopNode) and node.type().name() == "attribwrangle" :            
            runon = node.parm("class").eval()            
            if node.isEditableInsideLockedHDA() :
                if ((node.color() == hou.Color((.8, .8, .8)) or node.color() == hou.Color((.839, .839, .839)) ) if keepcolor else 1) :
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

def delete_parm_channels(sel=None, revert_defaults=None):
    """
    Delete nodes's parameter channels. Animation, etc,
    """
    sel = default(sel, hou.selectedNodes())
    revert_defaults = default(revert_defaults, 0)
    
    for node in sel:
        parms = node.parms()
        for parm in parms:
            parm.deleteAllKeyframes()
            if revert_defaults:
                parm.revertToDefaults()
