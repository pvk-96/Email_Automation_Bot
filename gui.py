from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import qdarkstyle
from contacts import ContactListManager
from template import TemplateEngine
from sender import EmailSender
from scheduler import Scheduler
import os
from datetime import datetime, timedelta

class EmailAutomationApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Automation & Tracking Tool")
        self.setGeometry(100, 100, 900, 600)
        self.contacts = []
        self.template_engine = None
        self.sender = None
        self.scheduler = Scheduler()
        self.logs = []
        self.init_ui()

    def init_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)

        self.sidebar = QtWidgets.QListWidget()
        self.sidebar.setFixedWidth(160)
        self.sidebar.addItem("Contacts")
        self.sidebar.addItem("Template")
        self.sidebar.addItem("Send/Schedule")
        self.sidebar.addItem("Logs")
        self.sidebar.setCurrentRow(0)
        main_layout.addWidget(self.sidebar)

        self.stack = QtWidgets.QStackedWidget()
        main_layout.addWidget(self.stack)

        self.contacts_page = self._create_contacts_page()
        self.template_page = self._create_template_page()
        self.send_page = self._create_send_page()
        self.logs_page = self._create_logs_page()

        self.stack.addWidget(self.contacts_page)
        self.stack.addWidget(self.template_page)
        self.stack.addWidget(self.send_page)
        self.stack.addWidget(self.logs_page)

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)

    def _create_placeholder_page(self, text):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: #aaa;")
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        return page

    def _create_template_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)

        # Template file path (default)
        self.template_path = os.path.join(os.getcwd(), "default_template.txt")
        if not os.path.exists(self.template_path):
            with open(self.template_path, 'w', encoding='utf-8') as f:
                f.write("Subject: Job Opportunity at {company}\n\nHello {name},\n\nI hope you're doing well! I wanted to reach out about a new opportunity at {company}...\n\nBest regards,\nYour Name")
        self.template_engine = TemplateEngine(self.template_path)

        # Subject
        subject_label = QtWidgets.QLabel("Subject:")
        self.subject_edit = QtWidgets.QLineEdit(self.template_engine.subject)
        layout.addWidget(subject_label)
        layout.addWidget(self.subject_edit)

        # Body
        body_label = QtWidgets.QLabel("Body:")
        self.body_edit = QtWidgets.QPlainTextEdit(self.template_engine.body)
        layout.addWidget(body_label)
        layout.addWidget(self.body_edit)

        # Save button
        save_btn = QtWidgets.QPushButton("Save Template")
        save_btn.clicked.connect(self._save_template)
        layout.addWidget(save_btn, alignment=QtCore.Qt.AlignLeft)

        # Preview
        preview_label = QtWidgets.QLabel("Preview (with sample data):")
        self.preview_area = QtWidgets.QTextEdit()
        self.preview_area.setReadOnly(True)
        layout.addWidget(preview_label)
        layout.addWidget(self.preview_area)

        # Update preview on edit
        self.subject_edit.textChanged.connect(self._update_preview)
        self.body_edit.textChanged.connect(self._update_preview)
        self._update_preview()

        return page

    def _save_template(self):
        subject = self.subject_edit.text()
        body = self.body_edit.toPlainText()
        self.template_engine.save_template(subject, body)
        QtWidgets.QMessageBox.information(self, "Template Saved", "Template saved successfully.")
        self._update_preview()

    def _update_preview(self):
        subject = self.subject_edit.text()
        body = self.body_edit.toPlainText()
        # Use sample data for preview
        sample_data = {"name": "Alice", "company": "OpenAI"}
        preview_subject = subject
        preview_body = body
        for key, value in sample_data.items():
            preview_subject = preview_subject.replace(f'{{{key}}}', value)
            preview_body = preview_body.replace(f'{{{key}}}', value)
        preview = f"Subject: {preview_subject}\n\n{preview_body}"
        self.preview_area.setPlainText(preview)

    def _create_contacts_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)

        # Upload button
        upload_btn = QtWidgets.QPushButton("Upload CSV")
        upload_btn.clicked.connect(self._upload_csv)
        layout.addWidget(upload_btn, alignment=QtCore.Qt.AlignLeft)

        # Table for contacts
        self.contacts_table = QtWidgets.QTableWidget()
        self.contacts_table.setColumnCount(3)
        self.contacts_table.setHorizontalHeaderLabels(["Name", "Email", "Company"])
        self.contacts_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.contacts_table)

        # Remove dummy data loading from here
        # self._load_contacts([
        #     {"name": "Alice", "email": "alice@example.com", "company": "OpenAI"},
        #     {"name": "Bob", "email": "bob[at]example.com", "company": "TechCorp"},
        # ])

        return page

    def _upload_csv(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Contacts CSV", "", "CSV Files (*.csv)")
        if path:
            try:
                manager = ContactListManager(path)
                contacts = manager.load_contacts()
                self._load_contacts(contacts, manager)
                QtWidgets.QMessageBox.information(self, "CSV Upload", f"Loaded {len(contacts)} contacts from file.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "CSV Error", f"Failed to load contacts:\n{e}")

    def _create_send_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)

        # SMTP settings
        smtp_group = QtWidgets.QGroupBox("SMTP Settings")
        smtp_layout = QtWidgets.QFormLayout(smtp_group)
        self.smtp_server_edit = QtWidgets.QLineEdit("smtp.gmail.com")
        self.smtp_port_edit = QtWidgets.QLineEdit("587")
        self.smtp_user_edit = QtWidgets.QLineEdit()
        self.smtp_pass_edit = QtWidgets.QLineEdit()
        self.smtp_pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        smtp_layout.addRow("Server:", self.smtp_server_edit)
        smtp_layout.addRow("Port:", self.smtp_port_edit)
        smtp_layout.addRow("Username:", self.smtp_user_edit)
        smtp_layout.addRow("Password:", self.smtp_pass_edit)
        layout.addWidget(smtp_group)

        # Recipients selection
        recipients_group = QtWidgets.QGroupBox("Recipients")
        recipients_layout = QtWidgets.QVBoxLayout(recipients_group)
        self.recipients_list = QtWidgets.QListWidget()
        self.recipients_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        recipients_layout.addWidget(self.recipients_list)
        layout.addWidget(recipients_group)

        # Load dummy data for first run (if no contacts loaded yet)
        if not self.contacts:
            self._load_contacts([
                {"name": "Alice", "email": "alice@example.com", "company": "OpenAI"},
                {"name": "Bob", "email": "bob[at]example.com", "company": "TechCorp"},
            ])
        self._refresh_recipients_list()

        # Send options
        options_group = QtWidgets.QGroupBox("Send Options")
        options_layout = QtWidgets.QFormLayout(options_group)
        self.send_now_radio = QtWidgets.QRadioButton("Send Now")
        self.schedule_radio = QtWidgets.QRadioButton("Schedule Send")
        self.send_now_radio.setChecked(True)
        self.schedule_time_edit = QtWidgets.QDateTimeEdit(datetime.now() + timedelta(minutes=1))
        self.schedule_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.schedule_time_edit.setEnabled(False)
        self.schedule_radio.toggled.connect(lambda checked: self.schedule_time_edit.setEnabled(checked))
        options_layout.addRow(self.send_now_radio)
        options_layout.addRow(self.schedule_radio, self.schedule_time_edit)
        layout.addWidget(options_group)

        # Send button
        send_btn = QtWidgets.QPushButton("Send Email(s)")
        send_btn.clicked.connect(self._send_emails)
        layout.addWidget(send_btn, alignment=QtCore.Qt.AlignLeft)

        # Status
        self.send_status = QtWidgets.QLabel()
        layout.addWidget(self.send_status)

        return page

    def _refresh_recipients_list(self):
        if not hasattr(self, 'recipients_list'):
            return
        self.recipients_list.clear()
        for contact in getattr(self, 'contacts', []):
            display = f"{contact.get('name', '')} <{contact.get('email', '')}>"
            item = QtWidgets.QListWidgetItem(display)
            item.setData(QtCore.Qt.UserRole, contact)
            self.recipients_list.addItem(item)

    def _send_emails(self):
        # Gather SMTP info
        smtp_server = self.smtp_server_edit.text().strip()
        try:
            smtp_port = int(self.smtp_port_edit.text().strip())
        except ValueError:
            self.send_status.setText("Invalid SMTP port.")
            return
        smtp_user = self.smtp_user_edit.text().strip()
        smtp_pass = self.smtp_pass_edit.text().strip()
        if not (smtp_server and smtp_port and smtp_user and smtp_pass):
            self.send_status.setText("Please fill in all SMTP fields.")
            return
        self.sender = EmailSender(smtp_server, smtp_port, smtp_user, smtp_pass)

        # Get selected recipients
        selected = self.recipients_list.selectedItems()
        if not selected:
            self.send_status.setText("No recipients selected.")
            return
        recipients = [item.data(QtCore.Qt.UserRole) for item in selected]

        # Get template
        if not self.template_engine:
            self.send_status.setText("No template loaded.")
            return
        subject = self.template_engine.subject
        body = self.template_engine.body

        # Send now or schedule
        if self.send_now_radio.isChecked():
            self._send_bulk_emails(recipients, subject, body)
        else:
            send_time = self.schedule_time_edit.dateTime().toPyDateTime()
            self.scheduler.schedule_send(send_time, self._send_bulk_emails, recipients, subject, body)
            self.send_status.setText(f"Scheduled {len(recipients)} email(s) for {send_time}.")
            self._log(f"Scheduled {len(recipients)} email(s) for {send_time}.")

    def _send_bulk_emails(self, recipients, subject, body):
        count = 0
        for contact in recipients:
            personalized_subject, personalized_body = self.template_engine.render(contact)
            success, error = self.sender.send_email(contact['email'], personalized_subject, personalized_body)
            if success:
                self._log(f"Sent to {contact['email']}")
                count += 1
            else:
                self._log(f"Failed to {contact['email']}: {error}")
        self.send_status.setText(f"Sent {count}/{len(recipients)} emails.")

    def _log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
        self._refresh_logs()

    def _create_logs_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        self.logs_area = QtWidgets.QTextEdit()
        self.logs_area.setReadOnly(True)
        layout.addWidget(self.logs_area)
        self._refresh_logs()
        return page

    def _refresh_logs(self):
        if hasattr(self, 'logs_area'):
            self.logs_area.setPlainText('\n'.join(self.logs))

    def _load_contacts(self, contacts, manager=None):
        self.contacts = contacts
        self._refresh_recipients_list()
        self.contacts_table.setRowCount(len(contacts))
        for row, contact in enumerate(contacts):
            name_item = QtWidgets.QTableWidgetItem(contact.get("name", ""))
            email_item = QtWidgets.QTableWidgetItem(contact.get("email", ""))
            company_item = QtWidgets.QTableWidgetItem(contact.get("company", ""))
            is_valid = False
            if manager:
                is_valid = manager.validate_email(contact.get("email", ""))
            else:
                is_valid = self._is_valid_email(contact.get("email", ""))
            if not is_valid:
                email_item.setForeground(QtGui.QColor("red"))
            self.contacts_table.setItem(row, 0, name_item)
            self.contacts_table.setItem(row, 1, email_item)
            self.contacts_table.setItem(row, 2, company_item)

    def _is_valid_email(self, email):
        return "@" in email and "." in email

    @staticmethod
    def run():
        app = QtWidgets.QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        window = EmailAutomationApp()
        window.show()
        sys.exit(app.exec_()) 