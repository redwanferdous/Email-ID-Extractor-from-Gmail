import csv
from pathlib import Path

def main():
    """Convert a .txt email list into CSV with domains."""
    inp = Path(input("Enter path to text file (emails.txt): ").strip())
    out = inp.with_suffix(".csv")

    emails = [
        l.strip() for l in inp.read_text(encoding="utf-8").splitlines()
        if l.strip() and "@" in l
    ]

    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["email", "domain"])
        for e in emails:
            domain = e.split("@")[-1]
            w.writerow([e, domain])

    print(f"✅ Saved CSV to: {out}")

if __name__ == "__main__":
    main()
