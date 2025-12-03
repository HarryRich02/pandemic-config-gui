from PyQt5 import QtWidgets as QtW
import NodeGraphQt as NGQt


class DefaultLowestStage(NGQt.BaseNode):
    __identifier__ = "symptoms"
    NODE_NAME = "DefaultLowestStage"

    def __init__(self):
        super(DefaultLowestStage, self).__init__()
        self.set_name("Lowest Stage")
        self.set_color(40, 150, 40)
        self.add_output("Completion Time")
        self.add_text_input("tag", "Value", "0")


class TransitionNode(NGQt.BaseNode):
    __identifier__ = "symptoms"
    NODE_NAME = "TransitionNode"

    def __init__(self):
        super(TransitionNode, self).__init__()
        self.set_name("Transition Node")
        self.set_color(40, 150, 40)
        self.add_input("Previous", multi_input=True)
        self.add_output("Completion Time")
        self.add_text_input("tag", "Value", "0")


class TerminalStage(NGQt.BaseNode):
    __identifier__ = "symptoms"
    NODE_NAME = "TerminalStage"

    def __init__(self):
        super(TerminalStage, self).__init__()
        self.set_name("Terminal Stage")
        self.set_color(180, 40, 40)
        self.add_input("Previous", multi_input=True)
        self.add_text_input("tag", "Value", "0")


class ConstantTime(NGQt.BaseNode):
    __identifier__ = "transitions"
    NODE_NAME = "ConstantTime"

    def __init__(self):
        super(ConstantTime, self).__init__()
        self.set_name("Constant Time")
        self.set_color(220, 160, 20)
        self.add_input("Symptom")
        self.add_output("Next")
        self.add_text_input("Val", "Value", text="0.0")


class NormalTime(NGQt.BaseNode):
    __identifier__ = "transitions"
    NODE_NAME = "NormalTime"

    def __init__(self):
        super(NormalTime, self).__init__()
        self.set_name("Normal Time")
        self.set_color(220, 160, 20)
        self.add_input("Symptom")
        self.add_output("Next")
        self.add_text_input("loc", "loc", text="0.0")
        self.add_text_input("scale", "scale", text="0.0")


class BetaTime(NGQt.BaseNode):
    __identifier__ = "transitions"
    NODE_NAME = "BetaTime"

    def __init__(self):
        super(BetaTime, self).__init__()
        self.set_name("Beta Time")
        self.set_color(220, 160, 20)
        self.add_input("Symptom")
        self.add_output("Next")
        self.add_text_input("a", "a", text="0.0")
        self.add_text_input("b", "b", text="0.0")
        self.add_text_input("loc", "loc", text="0.0")
        self.add_text_input("scale", "scale", text="0.0")


class LognormalTime(NGQt.BaseNode):
    __identifier__ = "transitions"
    NODE_NAME = "LognormalTime"

    def __init__(self):
        super(LognormalTime, self).__init__()
        self.set_name("Lognormal Time")
        self.set_color(220, 160, 20)
        self.add_input("Symptom")
        self.add_output("Next")
        self.add_text_input("s", "s", text="0.0")
        self.add_text_input("loc", "loc", text="0.0")
        self.add_text_input("scale", "scale", text="0.0")


class ExponweibTime(NGQt.BaseNode):
    __identifier__ = "transitions"
    NODE_NAME = "ExponweibTime"

    def __init__(self):
        super(ExponweibTime, self).__init__()
        self.set_name("Exponweib Time")
        self.set_color(220, 160, 20)
        self.add_input("Symptom")
        self.add_output("Next")
        self.add_text_input("a", "a", text="0.0")
        self.add_text_input("c", "c", text="0.0")
        self.add_text_input("loc", "loc", text="0.0")
        self.add_text_input("scale", "scale", text="0.0")


class NodeGraphWidget(QtW.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtW.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.graph = NGQt.NodeGraph()
        layout.addWidget(self.graph.viewer())

        self.graph.register_nodes(
            [
                DefaultLowestStage,
                TransitionNode,
                TerminalStage,
                ConstantTime,
                NormalTime,
                BetaTime,
                LognormalTime,
                ExponweibTime,
            ]
        )

        self.graph.set_background_color(38, 50, 56)
        self.graph.set_grid_color(55, 71, 79)

        self._setup_context_menu()

    def _setup_context_menu(self):
        graph_menu = self.graph.get_context_menu("graph")

        symptom_menu = graph_menu.add_menu("Symptom Nodes")

        def create_cmd(node_class):
            node_key = node_class.__identifier__ + "." + node_class.__name__
            return lambda: self.graph.create_node(node_key)

        symptom_menu.add_command("Lowest Stage", create_cmd(DefaultLowestStage))
        symptom_menu.add_command("Transition Node", create_cmd(TransitionNode))
        symptom_menu.add_command("Terminal Stage", create_cmd(TerminalStage))

        trans_menu = graph_menu.add_menu("Transition Nodes")

        trans_menu.add_command("Constant Time", create_cmd(ConstantTime))
        trans_menu.add_command("Normal Time", create_cmd(NormalTime))
        trans_menu.add_command("Beta Time", create_cmd(BetaTime))
        trans_menu.add_command("Lognormal Time", create_cmd(LognormalTime))
        trans_menu.add_command("Exponweib Time", create_cmd(ExponweibTime))
