"""Export Gmail messages and optionally apply confirmed keyword-rule labels."""

import argparse
import base64
import csv
import html
import re
from datetime import datetime
from email.utils import getaddresses, parseaddr, parsedate_to_datetime
from pathlib import Path
from typing import Any


READ_ONLY_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
LABEL_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
FIELDS = [
    "email_id",
    "sender",
    "subject",
    "body",
    "time_of_day",
    "recipient_count",
    "source",
    "priority",
    "predicted_priority",
    "predicted_category",
]
MAX_MESSAGES = 50
MAX_LABEL_MESSAGES = 20

LABEL_RULES = {
    "Urgent": (
        "urgent",
        "asap",
        "immediate attention",
        "deadline today",
        "due today",
        "action required today",
    ),
    "Critical": (
        "security alert",
        "account compromised",
        "unauthorized sign-in",
        "unauthorized login",
    ),
    "High": (
        "action required",
        "approval needed",
        "payment due",
        "invoice due",
        "meeting request",
        "interview",
        "please respond",
    ),
    "Low": (
        "newsletter",
        "weekly digest",
        "unsubscribe",
        "sale",
        "discount",
        "promotion",
        "special offer",
    ),
    "Spam": (
        "you won a prize",
        "claim your prize",
        "claim your reward",
        "verify your account immediately",
        "account will be suspended",
        "suspicious login",
        "password expired",
        "gift card winner",
        "get rich quick",
        "crypto investment guaranteed",
    ),
}

CATEGORY_RULES = {
    "Urgent": LABEL_RULES["Urgent"],
    "Important": (
        "action required",
        "approval needed",
        "payment due",
        "invoice due",
        "please respond",
        "assignment due",
        "exam",
        "interview",
    ),
    "Spam": LABEL_RULES["Spam"],
    "Promotional": (
        "newsletter",
        "weekly digest",
        "unsubscribe",
        "sale",
        "discount",
        "promotion",
        "special offer",
        "coupon",
        "limited time offer",
    ),
    "Work/Academic": (
        "meeting",
        "project",
        "assignment",
        "course",
        "class",
        "professor",
        "university",
        "work",
        "team",
        "colleague",
        "office",
        "lecture",
    ),
    "Personal": (
        "family",
        "friend",
        "mom",
        "dad",
        "birthday",
        "dinner",
        "wedding",
        "personal",
        "catch up",
    ),
}


def decode_part(part: dict[str, Any]) -> str:
    """Decode a Gmail API MIME body part."""
    encoded = part.get("body", {}).get("data")
    if not encoded:
        return ""

    padding = "=" * (-len(encoded) % 4)
    return base64.urlsafe_b64decode(encoded + padding).decode("utf-8", errors="replace")


def text_parts(payload: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Collect non-attachment plain-text and HTML bodies from a MIME payload."""
    plain_text: list[str] = []
    html_text: list[str] = []

    def visit(part: dict[str, Any]) -> None:
        if part.get("filename"):
            return

        mime_type = part.get("mimeType", "").lower()
        if mime_type == "text/plain":
            content = decode_part(part)
            if content:
                plain_text.append(content)
        elif mime_type == "text/html":
            content = decode_part(part)
            if content:
                html_text.append(content)

        for child in part.get("parts", []):
            visit(child)

    visit(payload)
    return plain_text, html_text


def extract_body(payload: dict[str, Any]) -> str:
    """Prefer plain text, falling back to a basic HTML-to-text conversion."""
    plain_text, html_text = text_parts(payload)
    if plain_text:
        return "\n".join(plain_text).strip()
    if not html_text:
        return ""

    body = "\n".join(html_text)
    body = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body)).strip()


def header_values(payload: dict[str, Any]) -> dict[str, str]:
    return {
        header.get("name", "").lower(): header.get("value", "")
        for header in payload.get("headers", [])
    }


def time_of_day(message: dict[str, Any], headers: dict[str, str]) -> str:
    timestamp = message.get("internalDate")
    if timestamp:
        hour = datetime.fromtimestamp(int(timestamp) / 1000).hour
    elif headers.get("date"):
        try:
            hour = parsedate_to_datetime(headers["date"]).astimezone().hour
        except (TypeError, ValueError, OverflowError):
            return "unknown"
    else:
        return "unknown"

    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    return "evening"


def message_to_row(message: dict[str, Any]) -> dict[str, Any]:
    payload = message.get("payload", {})
    headers = header_values(payload)
    sender = parseaddr(headers.get("from", ""))[1] or headers.get("from", "")
    recipient_headers = [
        headers.get("to", ""),
        headers.get("cc", ""),
        headers.get("bcc", ""),
    ]
    recipients = {
        address.lower()
        for _, address in getaddresses(recipient_headers)
        if address
    }

    return {
        "email_id": message.get("id", ""),
        "sender": sender,
        "subject": headers.get("subject", ""),
        "body": extract_body(payload),
        "time_of_day": time_of_day(message, headers),
        "recipient_count": max(1, len(recipients)),
        "source": "Gmail",
        "priority": "",
        "predicted_priority": "",
        "predicted_category": "",
    }


def predict_priority(row: dict[str, Any]) -> str:
    """Apply transparent keyword rules; unmatched messages default to Medium."""
    text = f"{row['subject']} {row['body']}".casefold()
    for priority in ("Spam", "Urgent", "Critical", "High", "Low"):
        if any(
            re.search(
                rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])",
                text,
            )
            for keyword in LABEL_RULES[priority]
        ):
            return priority
    return "Medium"


def predict_category(row: dict[str, Any]) -> str:
    """Assign one user-facing category using explicit keyword rules."""
    text = f"{row['subject']} {row['body']}".casefold()
    for category in (
        "Spam",
        "Urgent",
        "Important",
        "Promotional",
        "Work/Academic",
        "Personal",
    ):
        if any(
            re.search(
                rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])",
                text,
            )
            for keyword in CATEGORY_RULES[category]
        ):
            return category
    return "Normal"


def apply_priority_labels(service: Any, rows: list[dict[str, Any]]) -> None:
    label_results = service.users().labels().list(userId="me").execute()
    labels = {
        label["name"]: label["id"]
        for label in label_results.get("labels", [])
    }

    priorities = ("Urgent", "Critical", "High", "Medium", "Low", "Spam")
    categories = (
        "Urgent",
        "Important",
        "Spam",
        "Promotional",
        "Personal",
        "Work/Academic",
        "Normal",
    )
    for priority in priorities:
        name = f"Priority: {priority}"
        if name not in labels:
            label = (
                service.users()
                .labels()
                .create(
                    userId="me",
                    body={
                        "name": name,
                        "labelListVisibility": "labelShow",
                        "messageListVisibility": "show",
                    },
                )
                .execute()
            )
            labels[name] = label["id"]

    for category in categories:
        name = f"Category: {category}"
        if name not in labels:
            label = (
                service.users()
                .labels()
                .create(
                    userId="me",
                    body={
                        "name": name,
                        "labelListVisibility": "labelShow",
                        "messageListVisibility": "show",
                    },
                )
                .execute()
            )
            labels[name] = label["id"]

    for row in rows:
        priority = row["predicted_priority"]
        category = row["predicted_category"]
        label_ids = [
            labels[f"Priority: {priority}"],
            labels[f"Category: {category}"],
        ]
        old_priority_labels = [
            labels[f"Priority: {name}"]
            for name in priorities
            if name != priority
        ]
        old_category_labels = [
            labels[f"Category: {name}"]
            for name in categories
            if name != category
        ]
        service.users().messages().modify(
            userId="me",
            id=row["email_id"],
            body={
                "addLabelIds": label_ids,
                "removeLabelIds": old_priority_labels + old_category_labels,
            },
        ).execute()


def authorize(credentials_path: Path, token_path: Path, scopes: list[str]) -> Any:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    credentials = None
    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(str(token_path))

    if credentials and credentials.has_scopes(scopes):
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

    if (
        not credentials
        or not credentials.has_scopes(scopes)
        or not credentials.valid
    ):
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), scopes)
        credentials = flow.run_local_server(port=0)

    token_path.write_text(credentials.to_json(), encoding="utf-8")
    return credentials


def collect_messages(
    service: Any, query: str, max_messages: int
) -> list[dict[str, Any]]:
    response = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_messages)
        .execute()
    )

    rows = []
    for message_ref in response.get("messages", []):
        message = (
            service.users()
            .messages()
            .get(userId="me", id=message_ref["id"], format="full")
            .execute()
        )
        rows.append(message_to_row(message))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export up to 50 recent Gmail messages to a local CSV."
    )
    parser.add_argument(
        "--credentials",
        type=Path,
        default=Path(__file__).with_name("credentials.json"),
        help="Path to the downloaded Google OAuth Desktop App JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("gmail_emails.csv"),
        help="Local CSV output path (default: gmail_emails.csv).",
    )
    parser.add_argument(
        "--query",
        default="in:inbox",
        help='Gmail search query (default: "in:inbox").',
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=MAX_MESSAGES,
        help=f"Number of newest matching messages to export (1-{MAX_MESSAGES}).",
    )
    parser.add_argument(
        "--apply-priority-labels",
        action="store_true",
        help=(
            "Apply keyword-rule priority labels to Gmail. Requires gmail.modify "
            "authorization and is capped at 20 messages."
        ),
    )
    args = parser.parse_args()

    if not args.credentials.is_file():
        parser.error(
            f"OAuth credentials file not found: {args.credentials}. "
            "Download a Desktop App OAuth JSON file and pass it with --credentials."
        )
    if not 1 <= args.max_messages <= MAX_MESSAGES:
        parser.error(f"--max-messages must be between 1 and {MAX_MESSAGES}.")
    if args.apply_priority_labels and args.max_messages > MAX_LABEL_MESSAGES:
        parser.error(
            f"Applying labels is limited to {MAX_LABEL_MESSAGES} messages per run."
        )

    from googleapiclient.discovery import build

    token_name = (
        "gmail_modify_token.json"
        if args.apply_priority_labels
        else "gmail_token.json"
    )
    token_path = Path(__file__).with_name(token_name)
    scopes = LABEL_SCOPES if args.apply_priority_labels else READ_ONLY_SCOPES
    credentials = authorize(args.credentials, token_path, scopes)
    service = build("gmail", "v1", credentials=credentials, cache_discovery=False)
    rows = collect_messages(service, args.query, args.max_messages)

    if args.apply_priority_labels:
        for row in rows:
            row["predicted_priority"] = predict_priority(row)
            row["predicted_category"] = predict_category(row)
        priority_counts: dict[str, int] = {}
        category_counts: dict[str, int] = {}
        for row in rows:
            priority = row["predicted_priority"]
            category = row["predicted_category"]
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
        print("\nPriority label suggestions:")
        for priority, count in sorted(priority_counts.items()):
            print(f"  Priority: {priority}: {count}")
        print("\nCategory label suggestions:")
        for category, count in sorted(category_counts.items()):
            print(f"  Category: {category}: {count}")
        print("\nMessage-by-message preview:")
        for row in rows:
            subject = row["subject"] or "(no subject)"
            print(
                f"  {row['email_id']} | Priority: {row['predicted_priority']} "
                f"| Category: {row['predicted_category']} | {subject}"
            )
        print("\nThese rules are approximate; review before applying.")
        confirmation = input(
            f"Apply priority and category labels to these {len(rows)} Gmail messages? "
            "Type APPLY to continue: "
        )
        if confirmation != "APPLY":
            raise SystemExit("Cancelled; no Gmail labels were applied.")
        apply_priority_labels(service, rows)
        print(
            "Custom priority and category labels applied. "
            "Gmail Spam status was not changed."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} Gmail messages to {args.output.resolve()}")
    print(
        "priority is blank; predicted_priority and predicted_category are "
        "rule-based suggestions."
    )
    print("The CSV contains message text. Keep it private and stored securely.")


if __name__ == "__main__":
    main()
