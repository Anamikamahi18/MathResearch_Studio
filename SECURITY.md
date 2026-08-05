# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 1.0.0 | ✅ Active |

---

## Reporting a Vulnerability

If you discover a security vulnerability in **MathResearch Studio**, please do **NOT** open a public GitHub Issue. Instead, please report it responsibly by:

1. **Emailing** the maintainer directly via the contact address listed on the GitHub repository profile.
2. **Describing** the vulnerability clearly:
   - Steps to reproduce the issue.
   - Potential impact or attack surface.
   - Any suggested mitigation if known.

You will receive an acknowledgement within **72 hours**. Security issues will be investigated and, if confirmed, fixed in a patched release.

---

## Security Considerations for Deployment

### File Upload Safety
- Only PDF files are accepted by the upload interface.
- Uploaded files are stored locally in the `uploads/` directory.
- No file execution occurs on uploaded content.

### API Keys & Credentials
- Never commit `.env` files or API keys to the repository.
- Use environment variables to manage sensitive configuration (e.g. `HF_TOKEN`, `OPENAI_API_KEY`).
- The `.gitignore` file already excludes `.env` from version control.

### Local Deployment
- MathResearch Studio v1.0.0 is designed for **local research use** on a trusted machine.
- It is not hardened for public internet deployment without additional security measures (authentication, rate limiting, HTTPS, etc.).

---

## Acknowledgements

We take security seriously. Thank you for helping keep MathResearch Studio safe for all researchers.
