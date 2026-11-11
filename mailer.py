import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
CV_PATH = os.getenv("CV_PATH")

SUBJECT = "Candidature au poste de développeur MERN Stack"

BODY = """Bonjour,

Je suis développeur MERN Stack, maîtrisant React.js, Next.js, Node.js, Express.js, MongoDB, PostgreSQL et MySQL et php plus laravel.

Lors de mon stage, j'ai travaillé avec React.js et Keycloak pour l'authentification et la gestion des accès.

Je suis actuellement à la recherche d'un emploi en tant que développeur MERN Stack. Vous trouverez mon CV ci-dessous pour plus d'informations sur mon parcours et mes compétences.

Cordialement,
Zakaria Lafhiel"""

def send_email(to_email, company_name):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(BODY, "plain", "utf-8"))

    with open(CV_PATH, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(CV_PATH)}"')
    msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

    print(f"  Sent to {company_name} <{to_email}>")
