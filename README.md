# Ledgerly

> **Deliberately insecure.** Ledgerly is a small app written to be reviewed by
> [CyberReasoner](https://github.com/bineric-labs), an AI security reviewer. It contains security
> weaknesses on purpose. **Do not deploy it or reuse its code.**

Ledgerly keeps invoices and receipts for small teams: sign in by email, list and search your team's
invoices, download receipts, and edit your profile.

## Run it

```bash
pip install -r requirements.txt
flask --app ledgerly.app run
```

Sign in with `POST /login` and `{"email": "lars@fjordbyra.no"}`, then send the returned token as
`Authorization: Bearer <token>`.

The companies and people in the seed data are fictional.
