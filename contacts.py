import csv
import re

class ContactListManager:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load_contacts(self):
        contacts = []
        with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Try to extract name
                name = row.get('Name') or row.get('First Name') or row.get('File As') or ''
                if not name:
                    # Combine first, middle, last if available
                    name = ' '.join(filter(None, [row.get('First Name'), row.get('Middle Name'), row.get('Last Name')])).strip()
                # Try to extract email
                email = row.get('E-mail 1 - Value') or row.get('email') or row.get('Email') or ''
                # Try to extract company
                company = row.get('Organization Name') or row.get('company') or row.get('Company') or ''
                contacts.append({
                    'name': name,
                    'email': email,
                    'company': company
                })
        return contacts

    def validate_email(self, email):
        # Simple regex for email validation
        if not email:
            return False
        pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None 