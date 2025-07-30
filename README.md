# 📤 Email Automation & Tracking Tool

A modern, professional Python app to send **personalized bulk emails** with scheduling, template editing, and contact management—all in a beautiful PyQt5 dark mode GUI.

---

## 🚀 Features
- Upload and manage contacts from CSV
- Compose, edit, and preview email templates with placeholders
- Send personalized emails in bulk or schedule for later
- Live logs of sent emails and errors
- Modern dark mode UI (QDarkStyle)

---

## 📸 Screenshots

| Contacts Management | Template Editor | Scheduler | File Selection |
|--------------------|----------------|-----------|---------------|
| ![Contacts](email_tool/ss/contacts.png) | ![Template](email_tool/ss/template.png) | ![Scheduler](email_tool/ss/scheduler.png) | ![File Selection](email_tool/ss/file-selection.png) |

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pvk-96/Email_Automation_Bot.git
   cd Email_Automation_Bot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ Quick Start

1. **Run the app:**
   ```bash
   cd email_tool
   python main.py
   ```
2. **Upload your contacts CSV** (see below for how to export from Google Contacts)
3. **Edit your email template** (use `{name}` and `{company}` placeholders)
4. **Enter your SMTP details** (see below for Gmail setup)
5. **Select recipients and send or schedule emails!**

---

## 📧 Gmail SMTP Setup (IMPORTANT)

> **You must use an [App Password](https://myaccount.google.com/apppasswords) for Gmail SMTP. Your regular Gmail password will NOT work.**

### How to get an App Password:
1. Go to your [Google Account Security page](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled
3. After enabling, go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and "Other" (give it a name like "EmailBot")
5. Copy the 16-character app password and use it in the app (not your regular Gmail password)

**SMTP Settings Example:**
- Server: `smtp.gmail.com`
- Port: `587`
- Username: `yourname@gmail.com`
- Password: *(your app password)*

---

## 👥 Exporting Contacts from Google Contacts

1. Go to [Google Contacts](https://contacts.google.com/)
2. Select the contacts you want to export
3. Click **Export** (left sidebar)
4. Choose **CSV** format (Google CSV or Outlook CSV both work)
5. Save the file and upload it in the app

**Sample CSV columns supported:**
- `First Name`, `Last Name`, `E-mail 1 - Value`, `Organization Name`, etc.

---

## 📝 Usage Tips
- Use `{name}` and `{company}` in your template for personalization
- You can schedule emails for future delivery
- All actions and errors are logged in the Logs tab

---

## 🤝 Connect
- **GitHub:** [pvk-96](https://github.com/pvk-96)
- **LinkedIn:** [Praneeth Varma Kopperla](https://linkedin.com/praneeth-varma-kopperla)
- **Email:** praneethvarmakopperla@gmail.com

---

## 📄 License
MIT — free to use and adapt with credit. 
