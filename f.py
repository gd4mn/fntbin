from qtdbg import *
import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont, QWindow
from PySide6.QtCore import Qt
from fontmeta import FontMeta

FONT_DIRECTORY = "~/Library/Fonts"
FONT_NAME_FONT = QFont("Arial", 14)
DEFAULT_SAMPLE_SIZE = 24
FONT_PATH_FONT = QFont("Arial", 8)
FONT_SIZES = [6, 8, 10, 12, 16, 24, 36, 48, 64, 72]
SAMPLE_TEXT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789"
WINDOW_MARGINS = 8
WIDGET_SPACING = 8


class FontItem(QWidget):
    def __init__(self, path, metadata):
        super().__init__()

        if DEBUG:
            console.debug(f"Family: {metadata['font_family']} - {metadata['subfamily']}")
            console.debug(f"Full Name: {metadata['full_font_name']}")
            console.debug(f"Filename: {os.path.basename(path)}\n")

        self.font_name = metadata["full_font_name"]
        self.font_path = path
        self.font = QFont(self.font_name, DEFAULT_SAMPLE_SIZE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(WIDGET_SPACING)

        # font name
        name_label = QLabel(self.font_name)
        name_label.setFont(FONT_NAME_FONT)
        layout.addWidget(name_label)

        # font sample
        self.sample_label = QLabel(SAMPLE_TEXT)
        self.sample_label.setFont(QFont(self.font_name, DEFAULT_SAMPLE_SIZE))
        layout.addWidget(self.sample_label)

        # font path
        path_label = QLabel(self.font_path)
        path_label.setFont(FONT_PATH_FONT)
        layout.addWidget(path_label)


class FontGroup:
    def __init__(self, name, fonts):
        self.name = name
        self.fonts = fonts

        widget = QWidget()
        widget_layout = QVBoxLayout(self.widget)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(WIDGET_SPACING)

        name_label = QLabel()
        widget_layout.addWidget(name_label)
        self.fonts = []
        for font in fonts:
            self.fonts.append(FontItem(font.name, font.path))
            widget_layout.addWidget(self.fonts[-1].widget)
        name_label.setText(f"{name} ({len(fonts)})")

    def set_sample_font_size(self, size):
        for font in self.fonts:
            font.set_sample_font_size(size)


class AboutWindow(QWindow):
    def __init__(self):
        super().__init__()
        self.setTitle("About")
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # add contents
        layout.addWidget(QLabel("fntbin"))
        layout.addWidget(QLabel("Version 0.1"))
        layout.addWidget(QLabel("Copyright 2023"))
        layout.addWidget(QLabel("Author: Albert Freeman"))
        layout.addWidget(QLabel("License: GPLv3"))
        layout.addWidget(QLabel("Website: URL_ADDRESS.com"))
        layout.addWidget(QLabel("Website: URL_ADDRESS.com"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("fntbin")
        self.setMinimumSize(640, 480)

        # Create menu bar
        menu_bar = self.menuBar()
        # menu_bar.setNativeMenuBar(False)

        # File menu
        file_menu = menu_bar.addMenu(sys.argv[0])
        about_action = file_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        settings_action = file_menu.addAction("Settings")
        settings_action.triggered.connect(self.show_settings)
        file_menu.addSeparator()
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.close)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        window_layout = QVBoxLayout(central_widget)
        window_layout.setContentsMargins(WINDOW_MARGINS, 0, WINDOW_MARGINS, 0)
        window_layout.setSpacing(WIDGET_SPACING)

        # control bar
        control_bar = QWidget()
        control_bar.setFixedHeight(32)
        window_layout.addWidget(control_bar)
        bar_layout = QHBoxLayout(control_bar)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setSpacing(WIDGET_SPACING)

        # control bar widgets
        self.system_fonts_check = QCheckBox("Show system fonts")
        self.system_fonts_check.setChecked(True)
        self.system_fonts_check.stateChanged.connect(self.show_system_fonts)
        bar_layout.addWidget(self.system_fonts_check)

        action_frame = QWidget()
        action_frame.setMaximumWidth(192)
        bar_layout.addWidget(action_frame)
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(WIDGET_SPACING)

        # action bar widgets
        refresh_button = QPushButton("Refresh")
        action_layout.addWidget(refresh_button)
        add_group_button = QPushButton("Add Group")
        action_layout.addWidget(add_group_button)
        font_size_combo = QComboBox()
        font_size_combo.setMaximumWidth(64)
        font_size_combo.addItems([str(size) for size in FONT_SIZES])
        font_size_combo.currentIndexChanged.connect(self.change_font_size)
        action_layout.addWidget(font_size_combo)

        # font list
        font_list_display = QWidget()

        scroll_layout = QScrollArea()
        scroll_layout.setWidgetResizable(True)
        scroll_layout.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_layout.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_layout.setWidget(font_list_display)
        window_layout.addWidget(scroll_layout)

        # status_bar
        self.setStatusBar(None)
        status_bar = QWidget()
        status_bar.setFixedHeight(32)
        window_layout.addWidget(status_bar)
        status_bar_layout = QHBoxLayout(status_bar)
        status_bar_layout.setContentsMargins(0, 0, 0, 0)
        status_bar_layout.setSpacing(WIDGET_SPACING)

        # status bar widgets
        self.status_message = QLabel("Status message")
        status_bar_layout.addWidget(self.status_message)
        wells_frame = QWidget()
        wells_frame.setMaximumWidth(192)
        status_bar_layout.addWidget(wells_frame)
        wells_layout = QHBoxLayout(wells_frame)
        wells_layout.setContentsMargins(0, 0, 0, 0)
        wells_layout.setSpacing(WIDGET_SPACING)
        self.well_1 = QLabel("")
        wells_layout.addWidget(self.well_1)
        self.well_2 = QLabel("")
        wells_layout.addWidget(self.well_2)

        # load fonts
        self.set_status_message(f"Loading fonts from {FONT_DIRECTORY}")
        font_list = self.get_fonts(FONT_DIRECTORY)
        font_list_layout = QVBoxLayout(font_list_display)
        if len(font_list) > 0:
            for font in font_list:
                font_list_layout.addWidget(font)
        else:
            font_list_layout.addWidget(QLabel("No fonts found"))

        # signal ready
        self.set_status_message("Ready")
        self.set_status_well_2(f"<b>Fonts</b>: {len(font_list)}")

    # control bar slots
    def show_system_fonts(self, state):
        pass

    def change_font_size(self, index):
        pass

    def get_fonts(self, directory):
        directory = os.path.expanduser(directory)
        if not os.path.exists(directory):
            self.set_status_message(f"Directory {directory} does not exist")
            return

        fonts = []
        for file in os.listdir(directory):
            if file.endswith(".ttf") or file.endswith(".otf"):
                metadata = FontMeta(os.path.join(directory, file)).get_data()
                if metadata is None:
                    console.error(f"Failed to load font {file}")
                    continue
                fonts.append(FontItem(os.path.join(directory, file), metadata))
        return fonts

    def set_status_message(self, text):
        self.status_message.setText(text)

    def set_status_well_1(self, text):
        self.well_1.setText(text)

    def set_status_well_2(self, text):
        self.well_2.setText(text)

    def show_settings(self):
        self.set_status_message("Settings dialog (not implemented)")

    def show_about(self):
        self.set_status_message("About dialog (not implemented)")
        # a = AboutWindow()
        # a.show()


def main():
    app = QApplication(sys.argv)
    if DEBUG:
        app.setStyleSheet(DEBUG_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
