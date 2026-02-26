import os
from mailjet_rest import Client
from token_util import make_token

def send_rsvp_host_email(to_email: str, host_date: str):
    """
    Sends an RSVP email via Mailjet (mailjet_rest).

    Required env vars:
      - MAILJET_API_KEY
      - MAILJET_API_SECRET
      - FROM_EMAIL
      - BASE_URL
      - (optional) FROM_NAME
    """
    api_key = os.environ["MAILJET_API_KEY"]
    api_secret = os.environ["MAILJET_API_SECRET"]
    from_email = os.environ["FROM_EMAIL"]
    from_name = os.environ.get("FROM_NAME", "")

    mode = os.environ.get('MODE', "develop")

    base_url = os.environ["BASE_URL_DEVELOP"].rstrip("/")
    if mode == 'production':
        base_url = os.environ["BASE_URL_PRODUCTION"].rstrip("/")

    token = make_token({
        "email": to_email,
        "date": host_date,
    })

    yes_link = f"{base_url}/rsvp/host/reply?token={token}&answer=yes"
    no_link  = f"{base_url}/rsvp/host/reply?token={token}&answer=no"

    subject = f"RSVP needed: Hosting Opportunity for {host_date}"

    html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color:#111;">
      <p style="margin:0 0 12px 0;">Hi there,</p>

      <p style="margin:0 0 12px 0;">
        We’re confirming the hosting schedule for <b>{host_date}</b>.
      </p>

      <p style="margin:0 0 16px 0;">
        Are you available to host on that date?
      </p>

      <div style="margin:0 0 16px 0;">
        <a href="{yes_link}"
           style="display:inline-block; padding:10px 14px; background:#2e7d32; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:700;">
          Yes, I can host
        </a>
        <span style="display:inline-block; width:10px;"></span>
        <a href="{no_link}"
           style="display:inline-block; padding:10px 14px; background:#c62828; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:700;">
          No, I can’t
        </a>
      </div>

      <p style="margin:0 0 12px 0; color:#444; font-size:13px;">
        If the buttons don’t work, you can copy/paste one of these links:
        <br>
        Yes: <a href="{yes_link}" style="color:#1a73e8;">{yes_link}</a>
        <br>
        No: <a href="{no_link}" style="color:#1a73e8;">{no_link}</a>
      </p>

      <p style="margin:16px 0 0 0;">
        Thank you,<br>
        <span style="color:#444;">HMC Committee team</span>
      </p>

      <hr style="border:none; border-top:1px solid #eee; margin:16px 0;">

      <p style="margin:0; color:#777; font-size:12px;">
        This is an automated message to confirm availability for the hosting schedule.
      </p>
    </div>
    """

    mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    payload = {
        "Messages": [
            {
                "From": {"Email": from_email, **({"Name": from_name} if from_name else {})},
                "To": [{"Email": to_email}],
                "Subject": subject,
                "HTMLPart": html,
            }
        ]
    }

    # If you want debug output (don’t print secrets in prod)
    # print(payload)

    result = mailjet.send.create(data=payload)

    # Mailjet returns a Response-like object; safest is to check status_code + json
    if result.status_code >= 400:
        try:
            print("MAILJET ERROR status:", result.status_code)
            print("MAILJET ERROR body:", result.json())
        except Exception:
            print("MAILJET ERROR status:", result.status_code)
            print("MAILJET ERROR text:", getattr(result, "text", None))
        result.raise_for_status()

    return result.status_code

def send_rsvp_greeter_email(to_email: str, host_date: str):
    """
    Sends an RSVP email via Mailjet (mailjet_rest).

    Required env vars:
      - MAILJET_API_KEY
      - MAILJET_API_SECRET
      - FROM_EMAIL
      - BASE_URL
      - (optional) FROM_NAME
    """
    api_key = os.environ["MAILJET_API_KEY"]
    api_secret = os.environ["MAILJET_API_SECRET"]
    from_email = os.environ["FROM_EMAIL"]
    from_name = os.environ.get("FROM_NAME", "")

    mode = os.environ.get('MODE', "develop")

    base_url = os.environ["BASE_URL_DEVELOP"].rstrip("/")
    if mode == 'production':
        base_url = os.environ["BASE_URL_PRODUCTION"].rstrip("/")

    token = make_token({
        "email": to_email,
        "date": host_date,
    })

    yes_link = f"{base_url}/rsvp/greeter/reply?token={token}&answer=yes"
    no_link  = f"{base_url}/rsvp/greeter/reply?token={token}&answer=no"

    subject = f"RSVP needed: Greeter Opportunity for {host_date}"

    html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color:#111;">
      <p style="margin:0 0 12px 0;">Hi there,</p>

      <p style="margin:0 0 12px 0;">
        We’re confirming the greeter schedule for <b>{host_date}</b>.
      </p>

      <p style="margin:0 0 16px 0;">
        Are you available to serve as a greeter on that date?
      </p>

      <div style="margin:0 0 16px 0;">
        <a href="{yes_link}"
           style="display:inline-block; padding:10px 14px; background:#2e7d32; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:700;">
          Yes, I can greet
        </a>
        <span style="display:inline-block; width:10px;"></span>
        <a href="{no_link}"
           style="display:inline-block; padding:10px 14px; background:#c62828; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:700;">
          No, I can’t
        </a>
      </div>

      <p style="margin:0 0 12px 0; color:#444; font-size:13px;">
        If the buttons don’t work, copy/paste a link:
        <br>
        Yes: <a href="{yes_link}" style="color:#1a73e8;">{yes_link}</a>
        <br>
        No: <a href="{no_link}" style="color:#1a73e8;">{no_link}</a>
      </p>

      <p style="margin:16px 0 0 0;">
        Thank you,<br>
        <span style="color:#444;">Reshift Media Team</span>
      </p>

      <hr style="border:none; border-top:1px solid #eee; margin:16px 0;">

      <p style="margin:0; color:#777; font-size:12px;">
        This is an automated message to confirm availability for the greeter schedule.
      </p>
    </div>
    """

    mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    payload = {
        "Messages": [
            {
                "From": {"Email": from_email, **({"Name": from_name} if from_name else {})},
                "To": [{"Email": to_email}],
                "Subject": subject,
                "HTMLPart": html,
            }
        ]
    }

    # If you want debug output (don’t print secrets in prod)
    # print(payload)

    result = mailjet.send.create(data=payload)

    # Mailjet returns a Response-like object; safest is to check status_code + json
    if result.status_code >= 400:
        try:
            print("MAILJET ERROR status:", result.status_code)
            print("MAILJET ERROR body:", result.json())
        except Exception:
            print("MAILJET ERROR status:", result.status_code)
            print("MAILJET ERROR text:", getattr(result, "text", None))
        result.raise_for_status()

    return result.status_code
