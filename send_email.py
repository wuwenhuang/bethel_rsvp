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

    subject = f"RSVP: Do you want to host on {host_date}?"

    html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.4;">
      <p><b>Do you want to host on {host_date}?</b></p>
      <p>
        <a href="{yes_link}" style="padding:10px 14px; background:#2e7d32; color:white; text-decoration:none; border-radius:6px;">Yes</a>
        &nbsp;
        <a href="{no_link}" style="padding:10px 14px; background:#c62828; color:white; text-decoration:none; border-radius:6px;">No</a>
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

    subject = f"RSVP: Do you want to be greeter on {host_date}?"

    html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.4;">
      <p><b>Do you want to host on {host_date}?</b></p>
      <p>
        <a href="{yes_link}" style="padding:10px 14px; background:#2e7d32; color:white; text-decoration:none; border-radius:6px;">Yes</a>
        &nbsp;
        <a href="{no_link}" style="padding:10px 14px; background:#c62828; color:white; text-decoration:none; border-radius:6px;">No</a>
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
