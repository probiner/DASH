# DASH
![Logo](https://i.imgur.com/gH3wFkx.png)
## Granular utilities for SideFX Houdini.

DASH is a package for SideFX Houdini that proposes small quality of life improvements, standards and workflows through the delivery of nodes, scripts or settings.

The overarching goal will be to aid creative ideation by identifying granular routines and package them into reusable resources that can just be invoked, like shoring or prefab in civil construction. Therefore, flexibility, rich access to information and user speed are prioritized over optimization and scalability of code performance. It will be up to the users to create highly performant alternatives for their specific cases.

## Contents

In general included nodes will:
- Have a detailed help wiki.
![Help](https://i.imgur.com/RQcBVbB.png)
- Have a demo HDA that can be access at the bottom of their help.
![Demo](https://i.imgur.com/yePt5ai.png)
<video src="https://github.com/probiner/DASH/assets/1182548/6fb5d5e3-f8dd-439a-8cd5-6d8f8b2c9f97" autoplay="true"/><br/>
- Be blackboxed. Can't be opened or edited. (There are some side effects to this in VOPs, like error on RMB. RFE'd, as well as making reporting harder)

#### Firt Release

- 4 x SOPs (in `DASH_all_nodes.hip`)
- 7 x VOPs (in `DASH_all_nodes.hip`)
- 1 x Desktop, `DASH_SingleMonitorBuild`
- 1 x Shelf with 2 scripts. `Color SOP Wrangles` and `Delete Parm Channels`

First release is small and a revamp of assets I've first published on Orbolt. Its also representative of the type of nodes and principles that will be strived for in further releases:
- Small granular nodes that can be reused in many setups. Not full setup monolithic nodes.
- More VOPs than SOPs because the latter is a very targeted context (Many SOP nodes I created over the years intersect a lot with the shipped nodes, now).
- VOPs with array signatures to reduce the constant need to use for loop to deal with arrays.
- Menus with info and callback scripts that speed up the set up.
- Description messages for quicker overview awareness of the node operation in the node network.

## Installation
1) Place the DASH folder in a directory where you place other Houdini packages, e.g. `C:\users\user01\Documents\MyHoudiniPackages\Dash`
2) Place the contained DASH.json in the Houdini user directory, inside packages directory, e.g, `C:\users\user01\Documents\houdini20.0\packages\DASH.json`
3) Edit the `DASH` variable to point to package directory. Windows users will be forced here to use forward slashes. E.g. `"DASH": "C:/users/user01/Documents/MyHoudiniPackages/Dash"`. Save.
4) All done. Launch Houdini and the nodes, desktop and toolbar should now be ready to use.

## Feedback
To feedback this project you can use [github issues](https://github.com/probiner/DASH/issues), [instant messaging](https://discord.gg/URutVd4us7), or reach out on [Twitter](https://twitter.com/probiner)

---
#### Final Notes
"Whenever you show me your nodes I shrug because I have no idea why I would use them. Then, 6 months later I need them. - Russian friend.

Kudos to some elements of the community for all the help over the years in SideFX forums, ODforce forums, Think Procedural Discord, and also work colleagues. Many little things here were bettered by those interactions.

Thank you to the testers and motivators :D

