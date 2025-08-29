import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QLinearGradient

class TrafficLightWidget(QWidget):
    """Custom widget with modern dark theme styling"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(80, 250)
        self.active_light = "red"

    def set_light(self, color):
        self.active_light = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw housing with gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(60, 60, 60))
        gradient.setColorAt(1, QColor(40, 40, 40))
        painter.setBrush(QBrush(gradient))
        painter.drawRoundedRect(5, 5, 70, 240, 15, 15)

        colors = {
            "red": QColor(255, 80, 80),
            "yellow": QColor(255, 255, 100),
            "green": QColor(100, 255, 100)
        }
        positions = [(15, 20), (15, 100), (15, 180)]

        for name, pos in zip(["red", "yellow", "green"], positions):
            if self.active_light == name:
                # Active light with glow effect
                gradient = QLinearGradient(pos[0], pos[1], pos[0]+50, pos[1]+50)
                gradient.setColorAt(0, colors[name])
                gradient.setColorAt(1, colors[name].darker(150))
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(pos[0], pos[1], 50, 50)
                
                # Glow effect
                painter.setBrush(QBrush(colors[name]))
                painter.setOpacity(0.3)
                painter.drawEllipse(pos[0]-5, pos[1]-5, 60, 60)
                painter.setOpacity(1.0)
            else:
                # Inactive light
                painter.setBrush(QBrush(QColor(70, 70, 70)))
                painter.drawEllipse(pos[0], pos[1], 50, 50)

class SmartTrafficLight(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚦 Smart Traffic Light System 🚦")
        self.setGeometry(100, 100, 850, 600)
        
        # Dark theme styling
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                font-family: 'Segoe UI';
            }
            QLineEdit {
                background-color: #3a3a3a;
                border: 2px solid #4a4a4a;
                border-radius: 8px;
                padding: 5px;
                color: #ffffff;
                selection-background-color: #0078d7;
            }
            QLineEdit:focus {
                border: 2px solid #0078d7;
            }
            QComboBox {
                background-color: #3a3a3a;
                border: 2px solid #4a4a4a;
                border-radius: 8px;
                padding: 5px;
                min-width: 100px;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border-left: 1px solid #4a4a4a;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #3a3a3a;
                color: #ffffff;
                selection-background-color: #0078d7;
            }
        """)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        # Title with accent color
        self.title_label = QLabel("Smart Traffic Light System")
        self.title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0063b1, stop:1 #0095ff);
                border-radius: 10px;
            }
        """)
        self.main_layout.addWidget(self.title_label)

        # Lane controls
        self.lane_layout = QHBoxLayout()
        self.lane_layout.setSpacing(25)
        self.lane_inputs = {}
        self.traffic_lights = {}

        for i in range(1, 5):
            lane_box = QWidget()
            lane_box.setStyleSheet("background-color: #3a3a3a; border-radius: 10px;")
            lane_vbox = QVBoxLayout(lane_box)
            lane_vbox.setSpacing(15)
            lane_vbox.setContentsMargins(15, 15, 15, 15)

            lane_label = QLabel(f"Lane {i}")
            lane_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            lane_label.setAlignment(Qt.AlignCenter)
            lane_label.setStyleSheet("color: #ffffff;")

            lane_input = QLineEdit()
            lane_input.setPlaceholderText("0")
            lane_input.setFixedWidth(70)
            lane_input.setAlignment(Qt.AlignCenter)
            lane_input.setFont(QFont("Segoe UI", 12))

            self.lane_inputs[f"Lane {i}"] = lane_input
            lane_light = TrafficLightWidget()
            self.traffic_lights[f"Lane {i}"] = lane_light

            lane_vbox.addWidget(lane_label, alignment=Qt.AlignCenter)
            lane_vbox.addWidget(lane_input, alignment=Qt.AlignCenter)
            lane_vbox.addWidget(lane_light, alignment=Qt.AlignCenter)
            self.lane_layout.addWidget(lane_box)

        # Emergency controls
        self.emergency_container = QWidget()
        self.emergency_container.setStyleSheet("background-color: #3a3a3a; border-radius: 10px;")
        self.emergency_layout = QHBoxLayout(self.emergency_container)
        self.emergency_layout.setContentsMargins(20, 15, 20, 15)
        self.emergency_layout.setSpacing(20)
        
        self.emergency_label = QLabel("🚨 Emergency Vehicle in Lane:")
        self.emergency_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.emergency_label.setStyleSheet("color: #ff6b6b;")
        
        self.emergency_dropdown = QComboBox()
        self.emergency_dropdown.addItems(["None", "Lane 1", "Lane 2", "Lane 3", "Lane 4"])
        self.emergency_dropdown.setFont(QFont("Segoe UI", 11))
        
        self.emergency_layout.addWidget(self.emergency_label)
        self.emergency_layout.addWidget(self.emergency_dropdown)
        self.emergency_layout.setAlignment(Qt.AlignCenter)

        # Status and controls
        self.status_container = QWidget()
        self.status_container.setStyleSheet("background-color: #3a3a3a; border-radius: 10px;")
        status_layout = QVBoxLayout(self.status_container)
        status_layout.setContentsMargins(20, 15, 20, 15)
        status_layout.setSpacing(15)

        self.timer_label = QLabel("⏳ Time Left: 10s")
        self.timer_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("color: #ffffff;")

        self.start_button = QPushButton("🚦 Start Simulation")
        self.start_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.start_button.setFixedHeight(50)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #0095ff;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0078d7;
            }
            QPushButton:pressed {
                background-color: #0063b1;
            }
        """)
        self.start_button.clicked.connect(self.start_simulation)

        status_layout.addWidget(self.timer_label)
        status_layout.addWidget(self.start_button)

        # Add all widgets to main layout
        self.main_layout.addLayout(self.lane_layout)
        self.main_layout.addWidget(self.emergency_container, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.status_container)
        self.setLayout(self.main_layout)

        # Timer and simulation variables
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lights)
        self.time_left = 10
        self.current_lane_index = 0
        self.sorted_lanes = []
        self.emergency_handling = False

    def start_simulation(self):
        """Start traffic simulation based on vehicle count."""
        try:
            self.lane_counts = {f"Lane {i}": int(self.lane_inputs[f"Lane {i}"].text()) for i in range(1, 5)}
            self.sorted_lanes = sorted(self.lane_counts, key=self.lane_counts.get, reverse=True)

            self.current_lane_index = 0
            self.time_left = 10
            self.emergency_handling = False
            self.timer.start(1000)
            self.update_lights()
            self.start_button.setEnabled(False)
        except ValueError:
            self.timer_label.setText("❌ Invalid Input! Enter numbers only.")
            for lane_input in self.lane_inputs.values():
                lane_input.setStyleSheet("border: 2px solid #ff6b6b;")

    def update_lights(self):
        """Update the traffic light cycle and handle emergency vehicles if detected."""
        emergency_lane = self.emergency_dropdown.currentText()

        if emergency_lane != "None" and not self.emergency_handling:
            self.emergency_handling = True
            self.timer.stop()
            self.clear_lights()
            self.traffic_lights[emergency_lane].set_light("green")
            self.timer_label.setText(f"🚨 Emergency! Clearing {emergency_lane}...")
            QTimer.singleShot(5000, self.resume_normal_cycle)
            return

        if self.current_lane_index >= len(self.sorted_lanes):
            self.timer.stop()
            self.timer_label.setText("✅ Simulation Complete!")
            self.start_button.setEnabled(True)
            return

        current_lane = self.sorted_lanes[self.current_lane_index]
        next_lane_index = self.current_lane_index + 1

        self.clear_lights()
        self.traffic_lights[current_lane].set_light("green")
        if next_lane_index < len(self.sorted_lanes):
            self.traffic_lights[self.sorted_lanes[next_lane_index]].set_light("yellow")

        self.timer_label.setText(f"⏳ {current_lane}: {self.time_left}s")

        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.time_left = 10
            self.current_lane_index += 1

    def clear_lights(self):
        """Set all lights to red."""
        for lane, light in self.traffic_lights.items():
            light.set_light("red")

    def resume_normal_cycle(self):
        """Resume normal traffic cycle after emergency is cleared."""
        self.emergency_handling = False
        self.timer_label.setText("🔄 Resuming normal cycle...")
        self.emergency_dropdown.setCurrentIndex(0)
        self.timer.start(1000)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style for all widgets
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = SmartTrafficLight()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()