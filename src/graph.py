from PyQt5 import QtWidgets as QtW
import NodeGraphQt as NGQt


class StartNode(NGQt.BaseNode):
    __identifier__ = "stages"
    NODE_NAME = "Start State"

    def __init__(self):
        super(StartNode, self).__init__()
        self.set_color(40, 150, 40)
        self.add_output("Next Stage")


class TransitionNode(NGQt.BaseNode):
    __identifier__ = "stages"
    NODE_NAME = "Transition"

    def __init__(self):
        super(TransitionNode, self).__init__()
        self.set_color(220, 160, 20)
        self.add_input("From Stage")
        self.add_output("To Stage")

        self.add_text_input("Prob", "Probability", text="0.1")


class EndNode(NGQt.BaseNode):
    __identifier__ = "stages"
    NODE_NAME = "End State"

    def __init__(self):
        super(EndNode, self).__init__()
        self.set_color(180, 40, 40)
        self.add_input("From Stage")


class NodeGraphWidget(QtW.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtW.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.graph = NGQt.NodeGraph()

        layout.addWidget(self.graph.viewer())

        self.graph.register_nodes([StartNode, TransitionNode, EndNode])
        self.graph.set_background_color(38, 50, 56)
        self.graph.set_grid_color(55, 71, 79)

        self._setup_context_menu()

    def _setup_context_menu(self):
        graph_menu = self.graph.get_context_menu("graph")
        stage_menu = graph_menu.add_menu("stages")

        func_start = lambda: self.graph.create_node(
            StartNode.__identifier__ + "." + StartNode.__name__
        )

        func_transition = lambda: self.graph.create_node(
            TransitionNode.__identifier__ + "." + TransitionNode.__name__
        )

        func_end = lambda: self.graph.create_node(
            EndNode.__identifier__ + "." + EndNode.__name__
        )

        stage_menu.add_command(StartNode.NODE_NAME, func_start)
        stage_menu.add_command(TransitionNode.NODE_NAME, func_transition)
        stage_menu.add_command(EndNode.NODE_NAME, func_end)
