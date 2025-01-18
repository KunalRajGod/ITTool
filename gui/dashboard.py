from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, 
    QProgressBar, QScrollArea, QFrame, QHBoxLayout, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import os
import sys
import platform
import psutil
import subprocess
import socket
import time

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.scan_system import SystemScanner
from modules.repair import SystemRepair

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.scanner = SystemScanner()
        self.repair = SystemRepair()
        self.info_frame = None
        self.info_refresh_timer = None
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout()
        self.setMinimumSize(1000, 800)

        # Title
        title = QLabel("System Diagnostic Tool")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                padding: 20px;
                color: #2c3e50;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # System Details Button
        self.details_button = QPushButton("Show System Details")
        self.details_button.setStyleSheet("""
            QPushButton {
                background-color: #00ACC1;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 8px;
                min-height: 45px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #0097A7;
            }
            QPushButton:pressed {
                background-color: #00838F;
            }
        """)
        self.details_button.clicked.connect(self.toggle_system_info)
        layout.addWidget(self.details_button)

        # System Info Frame (initially hidden)
        self.info_frame = self.create_system_info_frame()
        self.info_frame.hide()
        layout.addWidget(self.info_frame)
        
        # Button Container
        button_layout = QHBoxLayout()
        
        # Scan Button
        self.scan_button = QPushButton("Start Diagnosis")
        self.scan_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                font-size: 16px;
                border-radius: 8px;
                min-height: 45px;
                margin: 10px;
                width: 200px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.scan_button.clicked.connect(self.start_scan)
        button_layout.addWidget(self.scan_button)

        # Fix Button
        self.fix_button = QPushButton("Fix Issues")
        self.fix_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 12px;
                font-size: 16px;
                border-radius: 8px;
                min-height: 45px;
                margin: 10px;
                width: 200px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.fix_button.clicked.connect(self.start_repair)
        self.fix_button.hide()
        button_layout.addWidget(self.fix_button)
        
        layout.addLayout(button_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 8px;
                text-align: center;
                height: 30px;
                margin: 10px;
                padding: 2px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 6px;
            }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Results Area
        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 8px;
                min-height: 300px;
                margin: 10px;
            }
        """)
        
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_widget.setLayout(self.results_layout)
        self.results_scroll.setWidget(self.results_widget)
        layout.addWidget(self.results_scroll)

        self.setLayout(layout)

    def create_system_info_frame(self):
        """Create system information display frame"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Get System Information
        info = self.get_system_info()
        
        for category, items in info.items():
            # Create category section
            category_frame = QFrame()
            category_frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 8px;
                    padding: 10px;
                    margin-bottom: 10px;
                }
            """)
            
            category_layout = QVBoxLayout()
            
            # Category Header
            header = QLabel(category)
            header.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #2c3e50;
                    padding: 5px;
                    border-bottom: 2px solid #3498db;
                    margin-bottom: 10px;
                }
            """)
            category_layout.addWidget(header)
            
            # Create grid for items
            grid = QGridLayout()
            grid.setSpacing(10)
            row = 0
            
            if isinstance(items, dict):
                for key, value in items.items():
                    if isinstance(value, dict):
                        # Sub-section for nested dictionaries
                        subheader = QLabel(key)
                        subheader.setStyleSheet("""
                            QLabel {
                                font-weight: bold;
                                color: #34495e;
                                padding: 5px 0;
                            }
                        """)
                        grid.addWidget(subheader, row, 0, 1, 2)
                        row += 1
                        
                        for subkey, subvalue in value.items():
                            key_label = QLabel(f"{subkey}:")
                            key_label.setStyleSheet("""
                                QLabel {
                                    color: #2c3e50;
                                    padding-left: 15px;
                                }
                            """)
                            
                            value_label = QLabel(str(subvalue))
                            value_label.setStyleSheet("""
                                QLabel {
                                    color: #2c3e50;
                                    font-weight: 500;
                                }
                            """)
                            
                            grid.addWidget(key_label, row, 0)
                            grid.addWidget(value_label, row, 1)
                            row += 1
                    else:
                        key_label = QLabel(f"{key}:")
                        key_label.setStyleSheet("""
                            QLabel {
                                color: #2c3e50;
                            }
                        """)
                        
                        value_label = QLabel(str(value))
                        value_label.setStyleSheet("""
                            QLabel {
                                color: #2c3e50;
                                font-weight: 500;
                            }
                        """)
                        
                        grid.addWidget(key_label, row, 0)
                        grid.addWidget(value_label, row, 1)
                        row += 1
            
            category_layout.addLayout(grid)
            category_frame.setLayout(category_layout)
            main_layout.addWidget(category_frame)
        
        # Add stretch at the end to push everything up
        main_layout.addStretch()
        frame.setLayout(main_layout)
        
        return frame

    def get_system_info(self):
        """Get detailed system information"""
        def format_bytes(bytes):
            gb = bytes / (1024 ** 3)
            return f"{gb:.2f} GB"

        # CPU Info
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            cpu_speed = f"{cpu_freq.current/1000:.2f} GHz"
        else:
            cpu_speed = "Unknown"

        # Memory Info
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        info = {
            "System": {
                "Operating System": f"{platform.system()} {platform.release()}",
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "Hostname": socket.gethostname()
            },
            "CPU": {
                "Physical Cores": psutil.cpu_count(logical=False),
                "Total Cores": psutil.cpu_count(logical=True),
                "Current Speed": cpu_speed,
                "Current Usage": f"{psutil.cpu_percent()}%"
            },
            "Memory": {
                "Total RAM": format_bytes(mem.total),
                "Used RAM": format_bytes(mem.used),
                "Available RAM": format_bytes(mem.available),
                "RAM Usage": f"{mem.percent}%",
                "Total Swap": format_bytes(swap.total),
                "Used Swap": format_bytes(swap.used),
                "Swap Usage": f"{swap.percent}%"
            }
        }

        # Storage Information
        storage_info = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                storage_info[f"Drive {partition.mountpoint}"] = {
                    "Total": format_bytes(usage.total),
                    "Used": format_bytes(usage.used),
                    "Free": format_bytes(usage.free),
                    "Usage": f"{usage.percent}%"
                }
            except:
                continue
        info["Storage"] = storage_info

        # Network Information
        network_info = {}
        try:
            # Get primary IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            network_info["IP Address"] = s.getsockname()[0]
            s.close()
        except:
            network_info["IP Address"] = "Not available"

        # Get network interfaces
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    network_info[f"Interface {interface}"] = addr.address

        info["Network"] = network_info

        # macOS Specific Information
        if platform.system() == "Darwin":
            try:
                # Get macOS version info
                output = subprocess.check_output(['sw_vers']).decode()
                mac_info = {}
                for line in output.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        mac_info[key.strip()] = value.strip()
                
                # Get System Hardware Info
                output = subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode()
                for line in output.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        if key and not key.startswith('*'):
                            mac_info[key] = value.strip()

                info["macOS Details"] = mac_info
            except:
                info["macOS Details"] = {"Note": "Additional macOS details unavailable"}

        return info

    def toggle_system_info(self):
        """Toggle system information display"""
        if self.info_frame.isHidden():
            # Update system info before showing
            new_info_frame = self.create_system_info_frame()
            old_info_frame = self.info_frame
            layout = self.layout()
            layout.replaceWidget(old_info_frame, new_info_frame)
            old_info_frame.deleteLater()
            self.info_frame = new_info_frame
            self.info_frame.show()
            self.details_button.setText("Hide System Details")
            
            # Start periodic updates
            if not self.info_refresh_timer:
                self.info_refresh_timer = QTimer()
                self.info_refresh_timer.timeout.connect(self.update_system_info)
                self.info_refresh_timer.start(5000)  # Update every 5 seconds
        else:
            self.info_frame.hide()
            self.details_button.setText("Show System Details")
            # Stop updates
            if self.info_refresh_timer:
                self.info_refresh_timer.stop()
                self.info_refresh_timer = None

    def update_system_info(self):
        """Update system information display"""
        if not self.info_frame.isHidden():
            new_info_frame = self.create_system_info_frame()
            old_info_frame = self.info_frame
            layout = self.layout()
            layout.replaceWidget(old_info_frame, new_info_frame)
            old_info_frame.deleteLater()
            self.info_frame = new_info_frame
            self.info_frame.show()

    def start_scan(self):
        """Start system scan"""
        self.scan_button.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.clear_results()
        self.scanner.start_scan()
        self.update_scan_progress()

    def update_scan_progress(self):
        """Update scan progress"""
        progress = self.scanner.get_progress()
        self.progress_bar.setValue(progress)
        
        if progress < 100:QTimer.singleShot(100, self.update_scan_progress)
        else:
            self.scan_complete()
            
    def scan_complete(self):
        """Handle scan completion"""
        issues = self.scanner.get_results()
        
        if not issues:
            self.add_message("✅ No issues found - System is healthy!", "success")
        else:
            for issue in issues:
                severity = issue.get('severity', 'medium')
                self.add_message(
                    f"⚠️ {issue['description']}", 
                    "error" if severity == 'high' else "warning"
                )
            self.fix_button.show()
            
        self.scan_button.setEnabled(True)
        
    def start_repair(self):
        """Start system repair"""
        self.fix_button.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.clear_results()
        
        try:
            self.repair.fix_issues(self.scanner.get_results())
            self.update_repair_progress()
        except Exception as e:
            self.add_message(f"Error during repair: {str(e)}", "error")
            self.fix_button.setEnabled(True)
            
    def update_repair_progress(self):
        """Update repair progress"""
        progress = self.repair.get_progress()
        self.progress_bar.setValue(progress)
        
        if progress < 100:
            QTimer.singleShot(100, self.update_repair_progress)
        else:
            self.repair_complete()
            
    def repair_complete(self):
        """Handle repair completion"""
        results = self.repair.get_results()
        
        for result in results:
            success = result.get('success', False)
            message = result.get('result', 'Unknown result')
            self.add_message(
                f"{'✅' if success else '❌'} {message}", 
                "success" if success else "error"
            )
            
        self.fix_button.setEnabled(True)
        
    def clear_results(self):
        """Clear all results from the display"""
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
    def add_message(self, message, message_type="info"):
        """Add a message to the results area"""
        colors = {
            "error": ("#FFF5F5", "#C53030", "#FEB2B2"),  # Red theme
            "warning": ("#FFFAF0", "#C05621", "#FBD38D"),  # Orange theme
            "success": ("#F0FFF4", "#2F855A", "#9AE6B4"),  # Green theme
            "info": ("#EBF8FF", "#2C5282", "#90CDF4")  # Blue theme
        }
        bg_color, text_color, border_color = colors.get(message_type, colors["info"])
        
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 15px;
                margin: 5px 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setStyleSheet(f"""
            color: {text_color};
            font-size: 14px;
            font-weight: 500;
        """)
        label.setWordWrap(True)
        layout.addWidget(label)
        
        frame.setLayout(layout)
        self.results_layout.addWidget(frame)
        
    def set_dark_theme(self):
        """Apply dark theme to the application"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QProgressBar {
                border: 2px solid #3d3d3d;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)

    def set_light_theme(self):
        """Apply light theme to the application"""
        self.setStyleSheet("")  # Reset to default light theme

    def closeEvent(self, event):
        """Handle application close event"""
        if self.info_refresh_timer:
            self.info_refresh_timer.stop()
        event.accept()

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
def get_system_info(self):
        """Get detailed system information"""
        def format_bytes(bytes):
            gb = bytes / (1024 ** 3)
            return f"{gb:.2f} GB"

        info = {}

        # macOS Specific Information
        if platform.system() == "Darwin":  # macOS
            try:
                # Get macOS version and build info
                sw_vers = subprocess.check_output(['sw_vers']).decode().strip()
                mac_info = {}
                for line in sw_vers.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        mac_info[key.strip()] = value.strip()

                info["macOS System"] = {
                    "Product Name": mac_info.get("ProductName", "Unknown"),
                    "Version": mac_info.get("ProductVersion", "Unknown"),
                    "Build": mac_info.get("BuildVersion", "Unknown")
                }

                # Get Hardware details
                system_profiler = subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode().strip()
                hardware_info = {}
                for line in system_profiler.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key and not key.startswith('*'):
                            hardware_info[key] = value

                info["Hardware"] = {
                    "Model Name": hardware_info.get("Model Name", "Unknown"),
                    "Model Identifier": hardware_info.get("Model Identifier", "Unknown"),
                    "Processor": hardware_info.get("Processor Name", "Unknown"),
                    "Processor Speed": hardware_info.get("Processor Speed", "Unknown"),
                    "Number of Processors": hardware_info.get("Number of Processors", "Unknown"),
                    "Total Number of Cores": hardware_info.get("Total Number of Cores", "Unknown"),
                    "Memory": hardware_info.get("Memory", "Unknown"),
                    "Serial Number": hardware_info.get("Serial Number (system)", "Unknown")
                }

                # Get Memory Information
                mem = psutil.virtual_memory()
                swap = psutil.swap_memory()
                info["Memory Status"] = {
                    "Total RAM": format_bytes(mem.total),
                    "Used RAM": format_bytes(mem.used),
                    "Available RAM": format_bytes(mem.available),
                    "RAM Usage": f"{mem.percent}%",
                    "Total Swap": format_bytes(swap.total),
                    "Used Swap": format_bytes(swap.used),
                    "Swap Usage": f"{swap.percent}%"
                }

                # Get Storage Information
                info["Storage"] = {}
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        info["Storage"][f"Volume {partition.mountpoint}"] = {
                            "Total": format_bytes(usage.total),
                            "Used": format_bytes(usage.used),
                            "Free": format_bytes(usage.free),
                            "Usage": f"{usage.percent}%"
                        }
                    except:
                        continue

                # Get Network Information
                info["Network"] = {}
                
                # Get primary IP
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    s.connect(("8.8.8.8", 80))
                    info["Network"]["Primary IP"] = s.getsockname()[0]
                except:
                    info["Network"]["Primary IP"] = "Not available"
                finally:
                    s.close()

                # Get all network interfaces
                for interface, addresses in psutil.net_if_addrs().items():
                    for addr in addresses:
                        if addr.family == socket.AF_INET:
                            info["Network"][f"Interface {interface}"] = addr.address

                # Get Wi-Fi information
                try:
                    airport = subprocess.check_output(
                        ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I']
                    ).decode()
                    wifi_info = {}
                    for line in airport.split('\n'):
                        if ': ' in line:
                            key, value = line.split(': ', 1)
                            wifi_info[key.strip()] = value.strip()
                    
                    if wifi_info:
                        info["Wi-Fi"] = {
                            "Network Name": wifi_info.get(" SSID", "Not connected"),
                            "Signal Strength": wifi_info.get(" agrCtlRSSI", "Unknown"),
                            "Channel": wifi_info.get(" channel", "Unknown"),
                            "Transmit Rate": wifi_info.get(" lastTxRate", "Unknown")
                        }
                except:
                    info["Wi-Fi"] = {"Status": "Unable to get Wi-Fi information"}

            except Exception as e:
                info["Error"] = {"Message": f"Error getting system information: {str(e)}"}

        return info

    # Set application style
app.setStyle('Fusion')
    
window = DashboardWindow()
window.show()
    
sys.exit(app.exec())