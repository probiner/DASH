# DASH
![Logo](https://i.imgur.com/TF40m1F.png)
## Granular utilities for SideFX Houdini.

DASH is a package for SideFX Houdini that proposes small quality of life improvements, standards and workflows through the delivery of nodes, scripts or settings.

## Introduction video. Design decisions.
[![VIDEO](https://i.imgur.com/jmwDYDT.png)](https://youtu.be/I1n2JEWlyNc)

## Characteristics
The overarching goal will be to aid creative ideation by identifying granular routines and package them into reusable resources that can just be invoked even if temporarily, like shoring or prefab in civil construction. Therefore, flexibility, extra information and user speed are prioritized over code optimization and scalability.

- Granular operations that can be reused in many setups. Not complete monolith setups.
- More VOPs than SOPs because the latter is a very targeted context (Many unique SOPs created over the years to deal with caveats now intersect too much with shipped nodes).
- Strive to support array signatures as much as possible to reduce the constant necessity to use for loop to deal with arrays.
- Menus with rich info and callback scripts that speed up the set up based on it.
- Description messages for simple overview awareness of the operation in the node network.

### Nodes
In general included nodes will:
- Have a detailed help wiki.<br/>
    ![Help](https://i.imgur.com/RQcBVbB.png)
- Have a demo HDA that can be launched at the bottom of the respective help wiki.<br/>
    ![Demo](https://i.imgur.com/yePt5ai.png)
    <video src="https://github.com/probiner/DASH/assets/1182548/6fb5d5e3-f8dd-439a-8cd5-6d8f8b2c9f97" autoplay="true"/><br/>
- Be blackboxed, i.e. can't be opened or edited. (VOP RMB error bug RFE'd)
- Be found under the submenu `DASH —` and include in their label the suffix `- DASH`.

## Installation
1) Extract the folder in the zip and rename it to `DASH` and place it in a directory where you place other Houdini packages. E.g. for Windows: `C:\users\probiner\Documents\MyHoudiniPackages\DASH`

2) Place the contained `DASH.json` in the `packages` folder of your desired houdinipath, usually in Houdini's user preferences directory, $HOME. E.g.
    - Win: `C:\users\{username}\Documents\houdini{version}\packages\DASH.json`
    - Linux: `/home/{username}/houdini{version}/packages/DASH.json`
    - Mac: `/Users/{username}/Library/Preferences/houdini/{version}/packages/DASH.json`
     
4) In the JSON file, edit the `DASH` variable to point to the package directory. Note to Windows users, you'll have to use forward slashes here. E.g. `"DASH": "C:/users/probiner/Documents/MyHoudiniPackages/DASH"`. Save the json.
5) All done! Launch Houdini and now, the nodes, desktop and toolbar should be ready to use!

## Feedback
To feedback this project you can use [github issues](https://github.com/probiner/DASH/issues), [instant messaging](https://discord.gg/tBfZxDFesT), or reach out on [Twitter](https://twitter.com/probiner)

---
#### Final Notes
"Whenever you show me your nodes I shrug because I have no idea why would I use them. Then, 6 months later I need them." - Russian friend.

Kudos to some elements of the community for all the help over the years at SideFX forums, ODforce forums, Think Procedural discord, and also work colleagues and students. Many little things here were bettered by those interactions. Thank you to the testers and motivators too :D
