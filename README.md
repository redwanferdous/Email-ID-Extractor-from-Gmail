# Gmail Email Extraction Toolkit

A lightweight, open-source toolkit to extract, clean, and analyze email addresses from exported Gmail data (Google Takeout MBOX files).

## Features
- Extracts emails from `.mbox` or plain text files
- Deduplicates automatically
- Filters out system / tracking / notification addresses
- Outputs CSV + domain summary
- Works in Google Colab or locally

## Quickstart (Google Colab)
```bash
from google.colab import drive
drive.mount('/content/drive')
!pip install tqdm pandas openpyxl
!git clone https://github.com/yourusername/gmail-email-extraction-toolkit.git
!python gmail-email-extraction-toolkit/scripts/extract_emails.py --input "/content/drive/MyDrive/sample.mbox" --output "/content/drive/MyDrive/output/emails.txt"
```
Then convert to CSV:
```bash
!python gmail-email-extraction-toolkit/scripts/make_csv.py --input "/content/drive/MyDrive/output/emails.txt"
```

## Ethics & Privacy
Use this tool only on mailboxes you own or have permission to analyze.

## License
MIT License
