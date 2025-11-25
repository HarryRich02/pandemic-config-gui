import NodeGraphQt as NGQt
from PyQt5 import QtWidgets as QtW
from PyQt5.QtCore import pyqtSignal

# --- Constants ---
DISTRIBUTION_TYPES = ["constant", "normal", "lognormal", "beta", "exponweib", "gamma"]


# --- Nodes ---
class StageNode(NGQt.BaseNode):
    __identifier__ = "stages"
    # FIXED: Set NODE_NAME to "StageNode" to match the actual registration key found in debug
    NODE_NAME = "StageNode"

    def __init__(self):
        super(StageNode, self).__init__()
        # VISUAL: Set the display name to "Stage" so it looks clean in the UI
        self.set_name("Stage")
        self.set_color(40, 150, 40)  # Greenish

        # Standard In/Out for chaining stages
        self.add_input("prev", multi_input=True, display_name=False)
        self.add_output("next", multi_output=True, display_name=False)

        # Property for the stage name (e.g., 'exposed', 'mild')
        self.add_text_input("stage_name", "Stage Name", text="exposed")


# --- UI Widgets ---
class PropertyEditorWidget(QtW.QWidget):
    """
    Context-sensitive editor. Shows Stage config if a Node is selected,
    or Transition config (Completion Time) if a Pipe is selected.
    Stores the transition data for connections.
    """

    def __init__(self):
        super().__init__()
        self.current_pipe_id = None
        self.transition_data = {}  # Key: (node_out_id, node_in_id), Value: dict

        self.layout = QtW.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.label = QtW.QLabel("Select an item to edit")
        self.label.setStyleSheet("font-weight: bold; color: #90A4AE;")
        self.layout.addWidget(self.label)

        # --- Transition Editor Controls (Hidden by default) ---
        self.trans_container = QtW.QWidget()
        self.trans_layout = QtW.QVBoxLayout(self.trans_container)
        self.trans_layout.setContentsMargins(0, 10, 0, 0)

        self.trans_layout.addWidget(QtW.QLabel("Completion Time Type:"))
        self.type_combo = QtW.QComboBox()
        self.type_combo.addItems(DISTRIBUTION_TYPES)
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        self.trans_layout.addWidget(self.type_combo)

        # Dynamic params area
        self.params_widget = QtW.QWidget()
        self.params_layout = QtW.QFormLayout(self.params_widget)
        self.trans_layout.addWidget(self.params_widget)

        self.trans_container.hide()
        self.layout.addWidget(self.trans_container)

        self.layout.addStretch(1)

    def on_selection_changed(self, graph):
        """Slot to handle selection changes in the graph."""
        selected_nodes = graph.selected_nodes()
        selected_pipes = graph.selected_pipes()

        self.trans_container.hide()
        self.current_pipe_id = None

        if selected_nodes:
            # Handle Node Selection
            node = selected_nodes[0]
            # Safely get property, default to empty string if missing
            stage_name = node.get_property("stage_name")
            self.label.setText(f"Editing Stage: {node.name()}")

        elif selected_pipes:
            # Handle Pipe Selection
            pipe = selected_pipes[0]
            self.label.setText("Editing Transition (Completion Time)")
            self.trans_container.show()

            # Identify the pipe by the IDs of the nodes it connects
            out_node = pipe.output_port.node()
            in_node = pipe.input_port.node()

            self.current_pipe_id = (out_node.id, in_node.id)

            # Load data
            data = self.transition_data.get(self.current_pipe_id, {})
            self._load_transition_data(data)

        else:
            self.label.setText("Select an item to edit")

    def on_port_connected(self, input_port, output_port):
        """Initialize data storage when a connection is made."""
        key = (output_port.node().id, input_port.node().id)
        if key not in self.transition_data:
            # Default to constant 0
            self.transition_data[key] = {"type": "constant", "value": 0.0}

    def on_port_disconnected(self, input_port, output_port):
        """Clean up data when a connection is broken."""
        key = (output_port.node().id, input_port.node().id)
        if key in self.transition_data:
            del self.transition_data[key]

    def _load_transition_data(self, data):
        dist_type = data.get("type", "constant")
        self.type_combo.setCurrentText(dist_type)
        self._rebuild_param_fields(dist_type, data)

    def _on_type_changed(self, text):
        if not self.current_pipe_id:
            return

        if self.current_pipe_id not in self.transition_data:
            self.transition_data[self.current_pipe_id] = {}
        self.transition_data[self.current_pipe_id]["type"] = text

        self._rebuild_param_fields(text, self.transition_data[self.current_pipe_id])

    def _rebuild_param_fields(self, dist_type, current_data):
        # Clear old fields
        while self.params_layout.count():
            child = self.params_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Define fields based on type
        fields = []
        if dist_type == "constant":
            fields = ["value"]
        elif dist_type == "normal":
            fields = ["loc", "scale"]
        elif dist_type == "lognormal":
            fields = ["s", "loc", "scale"]
        elif dist_type == "beta":
            fields = ["a", "b", "loc", "scale"]
        elif dist_type == "exponweib":
            fields = ["a", "c", "loc", "scale"]

        for field in fields:
            val = current_data.get(field, "0.0")
            line_edit = QtW.QLineEdit(str(val))
            line_edit.textChanged.connect(
                lambda txt, f=field: self._update_param(f, txt)
            )
            self.params_layout.addRow(f"{field}:", line_edit)

    def _update_param(self, field, value):
        if self.current_pipe_id:
            try:
                val = float(value)
            except ValueError:
                val = value
            self.transition_data[self.current_pipe_id][field] = val


class NodeGraphWidget(QtW.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtW.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.graph = NGQt.NodeGraph()
        self.viewer = self.graph.viewer()
        layout.addWidget(self.viewer)

        # Register the node
        self.graph.register_node(StageNode)

        # Debug: Print registered nodes to console to verify the key
        print("DEBUG: Registered Nodes:", self.graph.registered_nodes())

        self.graph.set_background_color(38, 50, 56)
        self.graph.set_grid_color(55, 71, 79)

        self._setup_context_menu()

    def _setup_context_menu(self):
        graph_menu = self.graph.get_context_menu("graph")

        # Dynamically construct the node identifier to match registration
        # Since NODE_NAME is now "StageNode", this becomes "stages.StageNode"
        node_type = StageNode.__identifier__ + "." + StageNode.NODE_NAME

        graph_menu.add_command("Add Stage", lambda: self.graph.create_node(node_type))
