import re

# Basic email extraction regex
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

# Common system / marketing / notification patterns to exclude
EXCLUDE_PATTERNS = [
    r"@cmail\d+\.com",
    r"@createsend\d*\.com",
    r"@mailchimp(app)?\.net",
    r"@sendgrid\.net",
    r"@amazonses\.com",
    r"@mailgun\.org",
    r"@mandrillapp\.com",
    r"@sendinblue\.com",
    r"@facebookmail\.com",
    r"@docs-share\.google\.com",
    r"@localhost",
    r"noreply", r"no-reply", r"do-not-reply",
    r"\+[^@]+@",  # emails with +tracking
    r"^cf[0-9a-fA-F\-]{6,}@",  # auto-generated cf IDs
]
EX_RE = re.compile("|".join(EXCLUDE_PATTERNS), re.IGNORECASE)

def extract_emails_from_text(text):
    """Extracts all potential email addresses from a text line."""
    return EMAIL_REGEX.findall(text or "")

def normalize_email(email):
    """Cleans and lowercases the email string."""
    return (email or "").strip().lower()

def is_system_email(email):
    """Checks if an email matches system/marketing patterns."""
    return bool(EX_RE.search(email or ""))
