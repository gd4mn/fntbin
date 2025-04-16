from typing import override
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
from PySide6.QtGui import QFont, QFontDatabase, QWindow
from PySide6.QtCore import Qt
from fontmeta import FontMeta

SCRIPT_TITLE = "fntbin"
FONT_DIRECTORY = "~/Library/Fonts"
FONT_NAME_FONT = QFont("Arial", 14)
DEFAULT_SAMPLE_SIZE = 24
FONT_PATH_FONT = QFont("Arial Bold", 11)
FONT_SIZES = [6, 8, 10, 12, 16, 24, 36, 48, 64, 72]
SAMPLE_TEXT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789"
WINDOW_MARGINS = 8
WIDGET_SPACING = 8

class FontItem(QWidget):
    def __init__(self, font:QFont()):
        super().__init__()

        self.font = font
        self.font_name = font.family()
        self.font_size = DEFAULT_SAMPLE_SIZE

        self.widget = QWidget()
        self.widget_layout = QVBoxLayout(self.widget)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_layout.setSpacing(WIDGET_SPACING)

        # font name
        font_name_label = QLabel()
        font_name_label.setFont(FONT_NAME_FONT)
        font_name_label.setText(self.font_name)
        self.widget_layout.addWidget(font_name_label)

        # sample text
        self.sample_text = QLabel()
        self.sample_text.setFont(QFont(self.font_name, self.font_size))
        self.sample_text.setText(SAMPLE_TEXT)
        self.widget_layout.addWidget(self.sample_text)

    def set_sample_font_size(self, size):
        self.font_size = size
        self.sample_text.setFont(QFont(self.font_name, self.font_size))


    def make_name(self, font_family, subfamily, path):
        if font_family == "":
            name = os.path.basename(path)
        else:
            name = font_family

        if subfamily != "":
            name += f" - {subfamily}"

        return name
    
    @override
    def __str__(self) -> str:
        return f"{self.font_name} - {self.font_size}px"


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


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{SCRIPT_TITLE} - About")
        self.setMinimumSize(320, 240)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)

        # add contents
        widget_layout.addWidget(QLabel("fntbin"))
        widget_layout.addWidget(QLabel("Version 0.1"))
        widget_layout.addWidget(QLabel("Copyright 2023"))
        widget_layout.addWidget(QLabel("Author: Albert Freeman"))
        widget_layout.addWidget(QLabel("License: GPLv3"))
        widget_layout.addWidget(QLabel("Website: URL_ADDRESS.com"))
        widget_layout.addWidget(QLabel("Website: URL_ADDRESS.com"))

        self.setFocus()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("fntbin")
        self.setMinimumSize(640, 480)

        # Create menu bar
        menu_bar = self.menuBar()
        if not DEBUG:
            menu_bar.setNativeMenuBar(False)

        # File menu
        file_menu = menu_bar.addMenu(f"{SCRIPT_TITLE}")
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
        self.set_status_message(f"Loading fonts ...")
        font_list = self.update_fonts()
        font_list_layout = QVBoxLayout(font_list_display)
        if len(font_list) > 0:
            for item in font_list:
                font_list_layout.addWidget(item)
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

    def update_fonts(self):
        fonts_item_list = []
        db = QFontDatabase()
        for font_id in db.families():
            font_item = FontItem(QFont(font_id))
            fonts_item_list.append(font_item)
            console.debug(f"Font: {font_item}")
        return fonts_item_list

    def set_status_message(self, text):
        self.status_message.setText(text)

    def set_status_well_1(self, text):
        self.well_1.setText(text)

    def set_status_well_2(self, text):
        self.well_2.setText(text)

    def show_settings(self):
        self.set_status_message("Settings dialog (not implemented)")

    def show_about(self):
        #self.set_status_message("About dialog (not implemented)")
        a = AboutWindow()
        a.show()


def main():
    app = QApplication(sys.argv)
    if DEBUG:
        app.setStyleSheet(DEBUG_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
