#!/usr/bin/env python3
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, QObject
import sys

class SignalEmitter(QObject):
    # Define custom signals
    number_signal = Signal(int)
    text_signal = Signal(str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Example")
        
        # Create central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Create emitter
        self.emitter = SignalEmitter()
        
        # Create UI elements
        self.counter = 0
        self.number_label = QLabel("Number: 0")
        self.text_label = QLabel("Text: None")
        self.button = QPushButton("Send Signals")
        
        # Add widgets to layout
        layout.addWidget(self.number_label)
        layout.addWidget(self.text_label)
        layout.addWidget(self.button)
        
        # Connect signals
        self.button.clicked.connect(self.send_signals)
        self.emitter.number_signal.connect(self.update_number)
        self.emitter.text_signal.connect(self.update_text)
    
    def send_signals(self):
        self.counter += 1
        self.emitter.number_signal.emit(self.counter)
        self.emitter.text_signal.emit(f"Signal sent {self.counter} times")
    
    def update_number(self, value):
        self.number_label.setText(f"Number: {value}")
    
    def update_text(self, text):
        self.text_label.setText(f"Text: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 150)
    window.show()
    sys.exit(app.exec())