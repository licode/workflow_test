#this is the config file to display tools on the left side of the webpage
#at the top level, the menu is a list of elements. Each element can be either a string or a pair.
#string will be displayed as an anotation line in the menu
#a pair means a sub menu: the first means the root menu label, the second contains a list of tools.
#each tool is a (label, tool_config) pair. tool_config specify the parameters of the tool

menu = [
    "Early beamlines",
    ("HXN", [
        ("Upload data", "upload/upload.json"),
        ("DPC", "DPC/dpc.json"),
        ("Tomography", "Tomography/tomography.json"),
    ]),
    ("SRX", [
        ("Upload data", "upload/upload.json"),
    ]),
    ("CSX-1", []),
    ("CSX-2", []),
    ("CHX", []),
    ("XPD", []),
    ("IXS", []),
    "Additional Beamlines",
    ("FXI", []),
]

