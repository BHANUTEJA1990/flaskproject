
from flask import Flask, request, render_template_string
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.run(host="192.0.0.1", port=10000, debug=True)
# --- CONFIGURE THESE ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "bhanutejavivekanandam@gmail.com"
SENDER_PASSWORD = "eoqkrwmzzjwlbmpq"
RECIPIENT_EMAIL = "recipient@example.com"
# -----------------------

# Load HTML form
with open("index.html", "r", encoding="utf-8") as f:
    index_html = f.read()


@app.route("/", methods=["GET"])
def index():
    return render_template_string(index_html)


@app.route("/submit", methods=["POST"])
def submit():
    # Get form data
    name = request.form.get("name")
    age = request.form.get("age")
    dob = request.form.get("dob")
    address = request.form.get("address")
    phone = request.form.get("phone")
    email = request.form.get("email")
    uploaded_file = request.files.get("file")

    # Prepare email
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = f"Form Submission: {name}"
    
    body = f"""
    Name: {name}
    Age: {age}
    DOB: {dob}
    Address: {address}
    Phone: {phone}
    Email: {email}
    """
    msg.set_content(body)

    # Attach uploaded file
    if uploaded_file:
        file_data = uploaded_file.read()
        msg.add_attachment(file_data, maintype="application",
                           subtype="octet-stream", filename=uploaded_file.filename)

    # Send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return "<h2>Form submitted successfully! Check your email.</h2>"
    except Exception as e:
        return f"<h2>Error sending email: {e}</h2>"


if __name__ == "__main__":
    app.run(debug=True)



