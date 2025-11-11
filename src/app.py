import os, sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal


disease_stages = [
    "recovered",
    "healthy",
    "exposed",
    "asymptomatic",
    "mild",
    "severe",
    "hospitalised",
    "intensive_care",
    "dead_home",
    "dead_hospital",
    "dead_icu",
]


class DiseaseConfigWidget(QWidget):
    config_saved = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setObjectName("configPanel")
        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 10)

        title_label = QLabel("Disease Config")
        title_label.setObjectName("title_label")
        layout.addWidget(title_label)

        layout.addWidget(QLabel("Name:"))
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("e.g., COVID-19 / Measles / Black Death")
        layout.addWidget(self.name_entry)

        layout.addWidget(QLabel("Default Lowest Stage:"))
        self.dls_combo = QComboBox()
        self.dls_combo.addItems(disease_stages)
        self.dls_combo.setCurrentText(disease_stages[0])
        layout.addWidget(self.dls_combo)

        layout.addWidget(QLabel("Max Mild Symptom Tag:"))
        self.mmst_combo = QComboBox()
        self.mmst_combo.addItems(disease_stages)
        self.mmst_combo.setCurrentText(disease_stages[0])
        layout.addWidget(self.mmst_combo)

        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.getConfigData)
        layout.addWidget(self.save_button)

        layout.addStretch(1)

    def getConfigData(self):
        config_data = {
            "name": self.name_entry.text(),
            "default_lowest_stage": self.dls_combo.currentText(),
            "max_mild_symptom_tag": self.mmst_combo.currentText(),
        }

        print("--- Configuration Data Retrieved ---")
        print(f"Name: {config_data['name']}")
        print(f"Default Lowest Stage: {config_data['default_lowest_stage']}")
        print(f"Max Mild Symptom Tag: {config_data['max_mild_symptom_tag']}")
        print("------------------------------------")

        self.config_saved.emit(config_data)


class NodeGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:#d9d9d9")

        layout = QVBoxLayout(self)
        label = QLabel("placeholder")
        layout.addWidget(label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pandemic-config-gui")
        self.resize(1280, 720)

        self.splitter = QSplitter(Qt.Horizontal)

        left_panel = DiseaseConfigWidget()
        right_panel = NodeGraphWidget()

        left_panel.config_saved.connect(self.handle_config_save)

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.setCentralWidget(self.splitter)

    def handle_config_save(self, config_data):
        print("MainWindow received saved config.")
        pass


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()

    qss_path = os.path.join(os.path.dirname(__file__), "style", "theme.qss")
    if os.path.exists(qss_path):
        try:
            with open(qss_path, "r") as f:
                _style = f.read()
                app.setStyleSheet(_style)
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
    else:
        print(
            f"Warning: Stylesheet not found at {qss_path}. Running with default theme."
        )

    window.show()
    sys.exit(app.exec_())
