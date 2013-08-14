import json
from my_test import tool_config
from main.tool.views import Tool

class ToolBox:
    def __init__(self, tool_dir):
        self._tool_dir = tool_dir
        self.init_tools()

    def init_tools(self):
        self.tools = {}
        self.tool_index = {} # this is an assitant dictionary
        self.content = []
        self.parse(tool_config.menu, self.content, 0)
        self.content = "\n".join(self.content)
        self.tool_index.clear()

    def parse(self, menu, content, step):
        if not menu:
            return
        if step == 0:
            content.append("<ul class='treeview' id='tree'>")
        else:
            content.append("<ul style='display: none;'>")
        for item in menu:
            if type(item) == str:
                content.append("<li>" + self.fontwrap(step, item) + "</li>")
            else:
                name = item[0]
                if type(item[1]) == str:
                    tool = self.load_config(item[1])
                    content.append("<li><a href = '/tool/" + tool.id + "'>" + self.fontwrap(step, name) + "</a></li>")
                else:
                    content.append("<li class='expandable'>")
                    content.append("<span>" + self.fontwrap(step, name) + "</span>")
                    self.parse(item[1], content, step + 1)
                    content.append("</li>")
        content.append("</ul>")

    def fontwrap(self, step, label):
        return "<h" + str(step + 2) + ">" + label + "</h" + str(step + 2) + ">"

    def load_config(self, config_file):
        #avoid multiple loading of same tool
        if config_file in self.tool_index:
            return self.tool_index[config_file]
        print config_file
        config = json.load(open(self._tool_dir + config_file))
        tool = Tool(config)
        self.tools[tool.id] = tool
        self.tool_index[config_file] = tool
        return tool



toolbox = ToolBox("tools/")

def get_tool(id):
    return toolbox.tools[id]
