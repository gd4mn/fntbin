#!/usr/bin/env python3
from qdbg import *
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QSystemTrayIcon,
    QMenu,
    QCheckBox,
    QSlider,
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QIcon, QAction
import sys


DEFAULT_SAMPLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz0123456789"
DEFAULT_SPACING = 8


class D4mnAccordion(QWidget):
    def __init__(self, collection_name="Not named."):
        super().__init__()
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)

        self.collapsed = False

        accordion_layout = QVBoxLayout(self)
        accordion_layout.setContentsMargins(0, DEFAULT_SPACING, 0, DEFAULT_SPACING)
        accordion_layout.setSpacing(DEFAULT_SPACING)

        self.header = QPushButton(collection_name)
        self.header.setCheckable(True)
        self.header.setChecked(False)
        self.header.clicked.connect(self.toggle_collapse)

        accordion_layout.addWidget(self.header)

        self.contents_layout = QVBoxLayout()
        self.contents_widget = QWidget()
        self.contents_widget.setLayout(self.contents_layout)

        accordion_layout.addWidget(self.contents_widget)

        self.update()

    def toggle_collapse(self):
        self.collapsed = not self.collapsed
        self.update()

    def add_widget(self, widget):
        self.contents_layout.addWidget(widget)

    def update(self):
        if self.collapsed:
            self.contents_widget.show()
        else:
            self.contents_widget.hide()
        super().update()


class FontCard(QWidget):
    def __init__(self, font_name="Comic Sans", font_size=13):
        super().__init__()
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)

        self.font_name = font_name
        self.font_sample_size = font_size
        self.sample_font = QFont(self.font_name, self.font_sample_size)

        # Create a vertical layout for the panel
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(DEFAULT_SPACING)
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)

        # Create a label for the font name
        self.font_label = QLabel(font_name)
        self.layout.addWidget(self.font_label)

        # Create a label for the font sample
        self.font_sample = QLabel(DEFAULT_SAMPLE)
        self.font_sample.setFont(QFont(self.font_name, self.font_sample_size))
        self.layout.addWidget(self.font_sample)

        self.update()

    def update(self):
        self.font_sample.setFont(QFont(self.font_name, self.font_sample_size))
        super().update()


class FontSizeSignal(QWidget):
    font_size = Signal(int)

class ControlBar(QWidget):
    font_size = Signal(int)

    def __init__(self):
        super().__init__()
        self.setFixedHeight(36)
        self.emitter = FontSizeSignal()
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(DEFAULT_SPACING, 0, DEFAULT_SPACING, 0)
        self.layout.setSpacing(DEFAULT_SPACING)

        self.show_system_fonts = QCheckBox("Show System Fonts")
        self.layout.addWidget(self.show_system_fonts)
        self.show_system_fonts.setChecked(True)

        size_widget = QWidget()
        size_widget_layout = QHBoxLayout(size_widget)
        size_widget_layout.setContentsMargins(0, 0, 0, 0)
        size_widget_layout.setSpacing(DEFAULT_SPACING)

        self.font_size_label = QLabel("Font Size:")
        size_widget_layout.addWidget(self.font_size_label)

        self.font_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_size_slider.setRange(6, 72)
        self.font_size_slider.setValue(12)
        size_widget_layout.addWidget(self.font_size_slider)

        self.font_size_label = QLabel("12")
        size_widget_layout.addWidget(self.font_size_label)

        self.layout.addWidget(size_widget)
        self.font_size_slider.valueChanged.connect(self.update_font_size)

    def update_font_size(self, value):
        self.font_size_label.setText(str(value))
        self.font_size.emit(value)
        if DEBUG:
            console.debug(f"Font size: {value}")


class StatusBar(QWidget):
    def __init__(self):
        super().__init__()
        if DEBUG:
            self.setStyleSheet(DEBUG_FILL_STYLE)

        self.setFixedHeight(24)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(DEFAULT_SPACING, 0, DEFAULT_SPACING, 0)
        self.layout.setSpacing(DEFAULT_SPACING)

        self.status_label = QLabel("Status: Ready")
        self.layout.addWidget(self.status_label)

        self.well_area = QWidget()
        self.well_area_layout = QHBoxLayout(self.well_area)
        self.well_area_layout.setContentsMargins(0, 0, 0, 0)
        self.well_area_layout.setSpacing(DEFAULT_SPACING)

        self.well_1 = QLabel("Well 1: 0")
        self.well_area_layout.addWidget(self.well_1)
        self.well_2 = QLabel("Well 2: 0")
        self.well_area_layout.addWidget(self.well_2)

        self.layout.addWidget(self.well_area)

    @property
    def status(self):
        return self.status_label.text()

    @status.setter
    def status(self, value):
        self.status_label.setText(f"Status: {value}")

    @property
    def well_1_value(self):
        return self.well_1.text()

    @well_1_value.setter
    def well_1_value(self, value):
        self.well_1.setText(f"Well 1: {value}")

    @property
    def well_2_value(self):
        return self.well_2.text()

    @well_2_value.setter
    def well_2_value(self, value):
        self.well_2.setText(f"Well 2: {value}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FntBin")
        self.setStatusBar(None)

        # Set up the main window
        self.setMinimumSize(640, 480)
        self.setMaximumWidth(960)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(DEFAULT_SPACING)

        # Add a custom control bar
        self.control_bar = ControlBar()
        self.layout.addWidget(self.control_bar)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Create container widget for scroll area
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(DEFAULT_SPACING, 0, DEFAULT_SPACING, 0)
        self.scroll_layout.setSpacing(DEFAULT_SPACING)

        # Set up scroll area
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Add a custom status bar
        self.status_bar = StatusBar()
        self.layout.addWidget(self.status_bar)

        # Add some sample font panels
        for i in range(20):
            font_panel = FontCard("Arial", 12)
            self.scroll_layout.addWidget(font_panel)

        for i in range(5):
            collection_card = D4mnAccordion(f"Collection {i}")
            for j in range(5):
                font_panel = FontCard("Arial", 12)
                collection_card.add_widget(font_panel)
            self.scroll_layout.addWidget(collection_card)

        self.status_bar.status = "Ready"
        self.status_bar.well_1_value = 10
        self.status_bar.well_2_value = 20


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load and apply stylesheet
    
    
    
    #with open("/Users/albertfreeman/Projects/fntbin/fntbin.qss", "r") as f:
    #   app.setStyleSheet(f.read())
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
