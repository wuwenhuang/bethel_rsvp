import os
from flask import jsonify
from mailjet_rest import Client
from token_util import make_token

def send_rsvp_host_email(to_name: str, to_email: str, host_date: str):
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
    host_template_id = int(os.environ['MAILJET_HOST_TEMPLATE_ID'])

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

    yes_link_html_str = f"""
    <a href="{yes_link}"
           style="display:inline-block; padding:10px 14px; background:#2e7d32; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:700;">
          Yes, I can host
        </a>
    """

    no_link_html_str = f"""
    <a href="{no_link}"
           style="display:inline-block; padding:10px 14px; background:#c62828; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:700;">
          No, I can’t
        </a>
    """

    mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    payload = {
        "Messages": [
            {
                "From": {"Email": from_email, **({"Name": from_name} if from_name else {})},
                "To": [{"Email": to_email}],
                "Subject": subject,
                "TemplateID": host_template_id,
                "TemplateLanguage": True,
                "Variables": {
                    "name": to_name,
                    "date": host_date,
                    "yes_link": yes_link_html_str,
                    "no_link": no_link_html_str
                }
            }
        ]
    }

    # If you want debug output (don’t print secrets in prod)
    # print(payload)

    try:
        # ... your Mailjet send code here ...
        result = mailjet.send.create(data=payload)  # example

        # If Mailjet returned error but no exception:
        if result.status_code >= 400:
            return jsonify({
                "error": "mailjet_error",
                "status": result.status_code,
                "details": getattr(result, "json", lambda: result.text)()
            }), 502

        return jsonify({"msg": "success", "data": result.json()}), 200

    except Exception as e:
        return jsonify({
            "error": "internal_server_error",
            "details": str(e)
        }), 500

def send_rsvp_greeter_email(to_name: str, to_email: str, host_date: str):
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
    greeter_template_id = int(os.environ['MAILJET_GREETER_TEMPLATE_ID'])

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

    yes_link_html_str = f"""
        <a href="{yes_link}"
               style="display:inline-block; padding:10px 14px; background:#2e7d32; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:700;">
              Yes, I can host
            </a>
        """

    no_link_html_str = f"""
        <a href="{no_link}"
               style="display:inline-block; padding:10px 14px; background:#c62828; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:700;">
              No, I can’t
            </a>
        """

    mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    payload = {
        "Messages": [
            {
                "From": {"Email": from_email, **({"Name": from_name} if from_name else {})},
                "To": [{"Email": to_email}],
                "Subject": subject,
                "TemplateID": greeter_template_id,
                "TemplateLanguage": True,
                "Variables": {
                    "name": to_name,
                    "date": host_date,
                    "yes_link": yes_link_html_str,
                    "no_link": no_link_html_str
                }
            }
        ]
    }

    # If you want debug output (don’t print secrets in prod)
    # print(payload)

    try:
        # ... your Mailjet send code here ...
        result = mailjet.send.create(data=payload)  # example

        # If Mailjet returned error but no exception:
        if result.status_code >= 400:
            return jsonify({
                "error": "mailjet_error",
                "status": result.status_code,
                "details": getattr(result, "json", lambda: result.text)()
            }), 502

        return jsonify({"msg": "success", "data": result.json()}), 200

    except Exception as e:
        return jsonify({
            "error": "internal_server_error",
            "details": str(e)
        }), 500
