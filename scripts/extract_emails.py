#!/usr/bin/env python3
import argparse, sqlite3, sys
from pathlib import Path
from scripts.filters import extract_emails_from_text, normalize_email, is_system_email

def init_db(db_path):
    """Initialize SQLite database to store unique emails."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE IF NOT EXISTS emails (email TEXT PRIMARY KEY, is_system INT)")
    return conn

def store_batch(conn, batch):
    """Insert a batch of emails into the database."""
    conn.executemany("INSERT OR IGNORE INTO emails VALUES (?,?)", batch)
    conn.commit()

def process_file(input_path, conn, batch_size=2000, keep_system=False):
    """Process text or mbox file line by line to extract unique emails."""
    total, unique = 0, 0
    batch = []
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            total += 1
            for e in extract_emails_from_text(line):
                e = normalize_email(e)
                sysflag = is_system_email(e)
                if not keep_system and sysflag:
                    continue
                batch.append((e, 1 if sysflag else 0))
            if len(batch) >= batch_size:
                store_batch(conn, batch)
                batch.clear()
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM emails")
                unique = cur.fetchone()[0]
                print(f"[{total:,} lines] unique={unique:,}", file=sys.stderr)
    if batch:
        store_batch(conn, batch)
    return total, unique

def dump_emails(conn, out_path):
    """Export all unique emails to text file."""
    with open(out_path, "w", encoding="utf-8") as f:
        for (email,) in conn.execute("SELECT email FROM emails ORDER BY email"):
            f.write(email + "\n")

def main():
    p = argparse.ArgumentParser(description="Extract unique email addresses from text or mbox files.")
    p.add_argument("--input", "-i", required=True, help="Input file path (.mbox or .txt)")
    p.add_argument("--output", "-o", required=True, help="Output text file for emails")
    p.add_argument("--db", default="emails.sqlite", help="SQLite database file")
    p.add_argument("--batch-size", type=int, default=2000, help="Number of lines per batch commit")
    p.add_argument("--keep-system", action="store_true", help="Keep system/auto-generated emails")
    args = p.parse_args()

    conn = init_db(args.db)
    lines, uniq = process_file(args.input, conn, args.batch_size, args.keep_system)
    dump_emails(conn, args.output)
    print(f"\n✅ Done. Processed {lines:,} lines. Unique emails: {uniq:,}")

if __name__ == "__main__":
    main()
