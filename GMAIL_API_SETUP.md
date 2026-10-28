# Use real Gmail messages

`0a_gmail_collector.py` exports up to the 50 newest matching messages (the
default query is `in:inbox`) to `gmail_emails.csv`. It uses Google's Gmail API
with the read-only `gmail.readonly` scope by default. Message bodies are included
in the local CSV; do not share that file.

## One-time Google OAuth setup

1. In Google Cloud Console, create or select a project and enable the **Gmail
   API**.
2. Configure the OAuth consent screen. If the app is in Testing mode, add the
   Google account you will authorize as a test user.
3. Create an OAuth client ID with application type **Desktop app**, then
   download its JSON file. Do not paste or upload its contents anywhere.
4. Install the Gmail API dependencies from this project folder:

   ```powershell
   py -m pip install -r requirements-gmail.txt
   ```

## Export messages

Pass the path to the downloaded JSON file. For example:

```powershell
py .\0a_gmail_collector.py --credentials ".\your-downloaded-oauth-file.json"
```

The first run opens Google's authorization page. Sign in to the intended
account and approve the read-only access request. The script saves the CSV as
`gmail_emails.csv` and its OAuth token as `gmail_token.json` beside the script.
Keep both the downloaded OAuth JSON file and token private.

You can export fewer messages or use a Gmail search query:

```powershell
py .\0a_gmail_collector.py --credentials ".\your-downloaded-oauth-file.json" --max-messages 10 --query "in:inbox newer_than:30d"
```

## Apply priority and category labels in Gmail

This optional mode requests the broader `gmail.modify` permission. It applies
custom labels only; it does not send, delete, archive, or mark messages as
Gmail Spam. Both `Priority: Spam` and `Category: Spam` are custom labels that
leave messages in the Inbox. The rules are simple keyword matches and are not
a trained model, so predictions may be wrong. The script prints a preview and
requires you to type `APPLY` before making any Gmail changes. Each run is
capped at 20 messages.

```powershell
py .\0a_gmail_collector.py --credentials ".\your-downloaded-oauth-file.json" --max-messages 20 --query "in:inbox" --apply-priority-labels
```

The first run of this mode asks Google for the additional permission. Approve
it only if you want the script to add labels. This mode stores its separate
OAuth token as `gmail_modify_token.json`; the read-only exporter continues to
use `gmail_token.json`. Each processed message gets two independent labels:

- One `Priority:` label: `Urgent`, `Critical`, `High`, `Medium`, `Low`, or
  `Spam`.
- One `Category:` label: `Urgent`, `Important`, `Spam`, `Promotional`,
  `Personal`, `Work/Academic`, or `Normal`.

The script replaces prior `Priority:` and `Category:` labels from these sets
on each processed message. Category rules check spam-like wording first, then
urgency and important-action terms, promotions, work/academic terms, and
personal terms. Anything unmatched is categorized as Normal. Rules can
misclassify emails, so review the per-message preview before confirming. The
CSV keeps `priority` blank and records suggestions separately in
`predicted_priority` and `predicted_category`.

## Continue preprocessing

Run the existing preprocessing step:

```powershell
py .\1_data_preprocessing_realemails.py
```

It now chooses `gmail_emails.csv` before the generated sample dataset. The
exported `priority` cells are intentionally blank. Review and label messages
before using them as supervised training examples. The CSV and OAuth token
remain local to your computer.
