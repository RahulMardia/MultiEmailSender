# 🚀 AI-Assisted Job Application Email Automation

A simple Python desktop application that automates sending job inquiry emails to multiple companies with a resume attached.

I built this project with the help of AI to simplify my job application process and explore how AI can accelerate everyday software development tasks.

Instead of manually composing emails, attaching a resume, and sending messages individually, this script handles the repetitive work through a simple desktop interface.

## ✨ Features

- **📧 Bulk Email Sending:** Send individual emails to multiple company email addresses.
- **📎 Automatic Resume Attachment:** Attach your resume PDF to every email.
- **⏱️ Configurable Delay:** Set a 30-second or 60-second interval between emails.
- **🖥️ Desktop GUI:** A simple interface built using Python's Tkinter library.
- **✏️ Editable Email Content:** Customize the subject and message before sending.
- **📊 Sending Status:** Track successful and failed email attempts.
- **🔐 Gmail SMTP Integration:** Send emails using Gmail SMTP and a Google App Password.
- **✅ Confirmation Before Sending:** Review the recipient count and confirm before starting.

## 🛠️ Technologies Used

- Python 3.9+
- Tkinter
- SMTP (`smtplib`)
- Email handling (`email.message`)
- SSL/TLS (`ssl`)
- Multithreading (`threading`)

## 📂 Project Structure

```text
job-email-automation/
│
├── send_job_emails_with_delay.py
└── README.md
```

## ⚙️ Installation and Setup

### 1. Install Python

Install Python 3.9 or later.

Verify the installation:

```bash
python --version
```

### 2. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd job-email-automation
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 3. Configure Gmail

The application uses Gmail SMTP to send emails.

Before running the script:

1. Enable 2-Step Verification on your Google Account.
2. Generate a Google App Password.
3. Keep the password private.

**Important:** Use a Google App Password rather than your regular Gmail password.

Google App Passwords may not be available for every account, including certain organization-managed accounts.

### 4. Run the Application

Execute:

```bash
python send_job_emails_with_delay.py
```

The desktop application will open.

### 5. Send Emails

1. Enter your Gmail address.
2. Enter your Google App Password.
3. Select your resume PDF.
4. Review the recipient list.
5. Customize the email subject and message if needed.
6. Click **Send emails** and confirm.

The application sends a separate email to each recipient, with the resume attached.

## ⏱️ Configuring the Email Delay

The script includes a configurable delay between email attempts.

Find this variable:

```python
DELAY_SECONDS = 60
```

For a 60-second delay:

```python
DELAY_SECONDS = 60
```

For a 30-second delay:

```python
DELAY_SECONDS = 30
```

A delay controls the sending pace but does not guarantee that emails will avoid spam filters or account restrictions.

## 📧 Customizing the Email

You can customize the subject and body directly in the script or edit them in the desktop interface before sending.

For example:

```python
SUBJECT = "Job Opportunities Inquiry – Full Stack Development / AI/ML"
```

Personalize your message according to the roles and companies you are targeting.

## 🔐 Security Considerations

- Never upload your Gmail password or Google App Password to GitHub.
- Never commit personal resumes or sensitive information unless you intend to make them public.
- Keep credentials out of source code and version control.
- Verify recipient addresses before sending.
- Avoid sending unsolicited messages to irrelevant or incorrect email addresses.
- Respect Gmail's sending limits and applicable email policies.

**Note:** This application uses Gmail SMTP authentication. It does not guarantee delivery, prevent spam classification, or bypass Gmail's sending restrictions.

## 🤖 How AI Helped Build This Project

AI assisted me in turning a practical problem into a working Python automation tool.

The process involved using AI to help with:

- Structuring the Python application.
- Creating a graphical user interface with Tkinter.
- Implementing email sending and resume attachment functionality.
- Adding delays between email attempts.
- Handling errors and displaying sending status.
- Improving usability and simplifying the workflow.

The experience reinforced an important lesson: AI can help developers build solutions faster, but reviewing, understanding, testing, and securing the generated code remain essential.

## 🎯 Project Objective

The goal of this project is to demonstrate how AI-assisted development and Python automation can reduce repetitive work and help developers focus more on solving problems.

This is a personal productivity project and a practical example of using AI as a development assistant.

## 🔮 Future Improvements

Potential improvements include:

- [ ] Support for multiple resume versions.
- [ ] Company-specific email templates.
- [ ] CSV import for managing recipients.
- [ ] Email delivery and failure logs.
- [ ] Secure credential storage.
- [ ] Gmail API integration using OAuth 2.0.
- [ ] Follow-up reminders for job applications.
- [ ] Recipient validation before sending.

## 👨‍💻 Author

**Rahul Mardia**

Software Developer interested in Full Stack Development, React Native, React.js, Python, and AI/ML.

---

⭐ If you find this project useful, feel free to star the repository!