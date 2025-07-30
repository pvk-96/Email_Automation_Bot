import re

class TemplateEngine:
    def __init__(self, template_path):
        self.template_path = template_path
        self.subject = ''
        self.body = ''
        self.load_template()

    def load_template(self):
        with open(self.template_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if lines and lines[0].startswith('Subject:'):
            self.subject = lines[0].replace('Subject:', '').strip()
            self.body = ''.join(lines[1:]).strip()
        else:
            self.subject = ''
            self.body = ''.join(lines).strip()

    def save_template(self, subject, body):
        with open(self.template_path, 'w', encoding='utf-8') as f:
            f.write(f'Subject: {subject}\n\n{body}')
        self.subject = subject
        self.body = body

    def parse_placeholders(self, text):
        return re.findall(r'\{(\w+)\}', text)

    def render(self, data):
        subject = self.subject
        body = self.body
        for key, value in data.items():
            subject = subject.replace(f'{{{key}}}', str(value))
            body = body.replace(f'{{{key}}}', str(value))
        return subject, body 