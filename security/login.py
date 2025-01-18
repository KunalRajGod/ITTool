import bcrypt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

class LoginWindow(QWidget):
    login_successful = pyqtSignal()
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Universal PC & Mac Repair Tool")
        title_font = QFont()
        title_font.setPointSize(24)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(40)
        layout.addWidget(self.username_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        layout.addWidget(self.password_input)
        
        # Login button
        login_button = QPushButton("Login")
        login_button.setMinimumHeight(40)
        login_button.clicked.connect(self.attempt_login)
        layout.addWidget(login_button)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if self.verify_credentials(username, password):
            self.error_label.setText("")
            self.login_successful.emit()
        else:
            self.error_label.setText("Invalid username or password")
            
    def verify_credentials(self, username, password):
        stored_user = self.db_manager.get_user(username)
        if not stored_user:
            return False
            
        stored_password = stored_user['password']
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')
            
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)