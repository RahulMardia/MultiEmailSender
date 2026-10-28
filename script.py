"""
Email Outreach Desktop App

Enter your own sender email, app password, recipient addresses, subject, message,
attachment, and sending delay. No recipients or personal details are pre-filled.

Run: python send_job_emails.py
Requires Python 3.9+ and Gmail SMTP configured with an App Password.
"""
import os
import re
import smtplib
import ssl
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Outreach Sender")
        self.root.geometry("820x850")
        self.root.minsize(700, 700)
        self.sender_email = tk.StringVar()
        self.app_password = tk.StringVar()
        self.attachment_path = tk.StringVar()
        self.delay_seconds = tk.StringVar(value="60")

        outer = tk.Frame(root, padx=16, pady=14)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="Email Outreach Sender", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))
        tk.Label(outer, text="Your email address (Gmail)").pack(anchor="w")
        tk.Entry(outer, textvariable=self.sender_email).pack(fill="x", pady=(3, 9))
        tk.Label(outer, text="Google App Password (Use an App Password, not your normal Gmail password.)").pack(anchor="w")
        tk.Entry(outer, textvariable=self.app_password, show="*").pack(fill="x", pady=(3, 9))

        tk.Label(outer, text="Recipient email addresses (one per line)").pack(anchor="w")
        self.recipients_box = scrolledtext.ScrolledText(outer, height=7, wrap="word")
        self.recipients_box.pack(fill="x", pady=(3, 9))
        tk.Label(outer, text="Email subject").pack(anchor="w")
        self.subject_entry = tk.Entry(outer)
        self.subject_entry.pack(fill="x", pady=(3, 9))
        tk.Label(outer, text="Email message").pack(anchor="w")
        self.body_box = scrolledtext.ScrolledText(outer, height=10, wrap="word")
        self.body_box.pack(fill="both", expand=True, pady=(3, 9))

        tk.Label(outer, text="Attachment (optional)").pack(anchor="w")
        attachment_row = tk.Frame(outer)
        attachment_row.pack(fill="x", pady=(3, 9))
        tk.Entry(attachment_row, textvariable=self.attachment_path, state="readonly").pack(side="left", fill="x", expand=True)
        tk.Button(attachment_row, text="Choose file", command=self.choose_attachment).pack(side="left", padx=(8, 0))
        tk.Button(attachment_row, text="Clear", command=lambda: self.attachment_path.set("")).pack(side="left", padx=(6, 0))

        delay_row = tk.Frame(outer)
        delay_row.pack(fill="x", pady=(0, 10))
        tk.Label(delay_row, text="Delay between emails (seconds):").pack(side="left")
        tk.Entry(delay_row, textvariable=self.delay_seconds, width=8).pack(side="left", padx=(8, 0))
        tk.Label(delay_row, text="Example: 30 or 60", fg="#555").pack(side="left", padx=(8, 0))
        self.send_button = tk.Button(outer, text="Review and Send", command=self.confirm_and_send, font=("Segoe UI", 11, "bold"), padx=12, pady=8)
        self.send_button.pack(anchor="e")
        self.status = tk.StringVar(value="Fill in all required fields to begin.")
        tk.Label(outer, textvariable=self.status, anchor="w", fg="#333").pack(fill="x", pady=(8, 0))

    def choose_attachment(self):
        selected = filedialog.askopenfilename(title="Choose an attachment", filetypes=[("Common documents", "*.pdf *.doc *.docx"), ("All files", "*.*")])
        if selected:
            self.attachment_path.set(selected)

    def confirm_and_send(self):
        sender = self.sender_email.get().strip()
        password = self.app_password.get().strip()
        raw_recipients = self.recipients_box.get("1.0", "end").strip()
        subject = self.subject_entry.get().strip()
        body = self.body_box.get("1.0", "end").strip()
        attachment = self.attachment_path.get().strip()
        delay_text = self.delay_seconds.get().strip()
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not sender or not re.match(email_pattern, sender):
            messagebox.showerror("Check details", "Enter a valid sender email address."); return
        if not password:
            messagebox.showerror("Check details", "Enter your Google App Password."); return
        if not raw_recipients:
            messagebox.showerror("Check details", "Enter at least one recipient address."); return
        recipients = [line.strip() for line in raw_recipients.splitlines() if line.strip()]
        invalid = [addr for addr in recipients if not re.match(email_pattern, addr)]
        if invalid:
            messagebox.showerror("Invalid recipient address(es)", "Please correct these address(es):\n" + "\n".join(invalid)); return
        if not subject:
            messagebox.showerror("Check details", "Enter an email subject."); return
        if not body:
            messagebox.showerror("Check details", "Enter an email message."); return
        if attachment and not os.path.isfile(attachment):
            messagebox.showerror("Check attachment", "The selected attachment cannot be found."); return
        try:
            delay = int(delay_text)
            if delay < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Check delay", "Enter a whole number of seconds (0 or greater)."); return
        recipients = list(dict.fromkeys(recipients))
        minutes = max(0, len(recipients) - 1) * delay / 60
        proceed = messagebox.askyesno("Confirm email sending", f"Sender: {sender}\nRecipients: {len(recipients)} unique address(es)\nAttachment: {os.path.basename(attachment) if attachment else 'None'}\nDelay: {delay} seconds between emails\nEstimated delay time: about {minutes:.1f} minutes, plus connection time\n\nEach recipient gets a separate email. Contact only relevant recipients. A delay does not guarantee avoidance of spam filters or provider limits.\n\nContinue?")
        if not proceed: return
        self.send_button.configure(state="disabled")
        self.status.set("Connecting to the email server…")
        threading.Thread(target=self.send_emails, args=(sender, password, recipients, subject, body, attachment, delay), daemon=True).start()

    def send_emails(self, sender, password, recipients, subject, body, attachment, delay):
        sent, failed = [], []
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=30) as server:
                server.login(sender, password)
                for index, recipient in enumerate(recipients, start=1):
                    try:
                        msg = EmailMessage()
                        msg["From"], msg["To"], msg["Subject"] = sender, recipient, subject
                        msg.set_content(body)
                        if attachment:
                            with open(attachment, "rb") as file:
                                data = file.read()
                            name = os.path.basename(attachment)
                            ext = os.path.splitext(name)[1].lower()
                            subtype = {".pdf": "pdf", ".doc": "msword", ".docx": "vnd.openxmlformats-officedocument.wordprocessingml.document"}.get(ext, "octet-stream")
                            msg.add_attachment(data, maintype="application", subtype=subtype, filename=name)
                        server.send_message(msg)
                        sent.append(recipient)
                    except Exception as exc:
                        failed.append((recipient, str(exc)))
                    self.root.after(0, lambda i=index, total=len(recipients), addr=recipient: self.status.set(f"Processed {i}/{total}: {addr}"))
                    if delay and index < len(recipients):
                        for remaining in range(delay, 0, -1):
                            self.root.after(0, lambda i=index, total=len(recipients), sec=remaining: self.status.set(f"Processed {i}/{total}. Next email in {sec}s…"))
                            time.sleep(1)
        except Exception as exc:
            failed.append(("Email server connection/login", str(exc)))
        def finish():
            self.send_button.configure(state="normal")
            summary = f"Sent successfully: {len(sent)}\nFailed: {len(failed)}"
            if failed:
                summary += "\n\nFailure details:\n" + "\n".join(f"- {addr}: {err}" for addr, err in failed)
            self.status.set(f"Finished. Sent {len(sent)}; failed {len(failed)}.")
            messagebox.showinfo("Sending complete", summary)
        self.root.after(0, finish)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()
