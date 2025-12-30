import argparse
import html
import re
import sys


PATTERN = re.compile(
    r"Sent a message on.{0,1000}?([A-Z][a-z]{2} \d{1,2})'s Top Cyber News NOW! - Ep (\d+)",
    re.DOTALL,
)


def extract_unique_titles(html_text):
    text = html.unescape(html_text)
    seen = set()
    results = []
    for match in PATTERN.finditer(text):
        date_str, episode = match.group(1), match.group(2)
        key = (date_str, episode)
        if key in seen:
            continue
        seen.add(key)
        results.append(key)
    return results


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Extract unique Top Cyber News NOW episodes where a live chat message was sent."
        )
    )
    parser.add_argument(
        "html_file",
        nargs="?",
        default="Google - My Activity.html",
        help="Path to the Google My Activity HTML export.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Output results in CSV format with a header row.",
    )
    args = parser.parse_args()

    try:
        with open(args.html_file, "r", encoding="utf-8") as handle:
            html_text = handle.read()
    except OSError as exc:
        print(f"Failed to read {args.html_file}: {exc}", file=sys.stderr)
        return 1

    results = extract_unique_titles(html_text)
    if args.csv:
        print("date,episode")
        for date_str, episode in results:
            print(f"{date_str},{episode}")
    else:
        for date_str, episode in results:
            print(f"{date_str} - Ep {episode}")
        print(f"Total Episodes: {len(results)}")
        print(f"Total CPEs: {len(results) / 2:.1f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
