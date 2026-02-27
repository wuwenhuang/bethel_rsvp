import os
import json
from flask import Flask, request, abort, jsonify
from dotenv import load_dotenv
from datetime import date, timedelta

from send_email import send_rsvp_host_email, send_rsvp_greeter_email
from token_util import read_token
from sheets import upsert_response

load_dotenv()

app = Flask(__name__)

@app.get("/")
def home():
    return "Welcome"

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/rsvp/host/reply")
def rsvp_host_reply():
    token = request.args.get("token", "")
    answer = (request.args.get("answer", "") or "").lower().strip()

    if answer not in ("yes", "no"):
        abort(400, "answer must be yes or no")

    try:
        payload = read_token(token)
    except Exception:
        abort(400, "invalid token")

    email = payload.get("email")
    host_date = payload.get("date")
    if not email or not host_date:
        abort(400, "token missing fields")

    upsert_response(email, host_date, answer, 'Host')

    return f"<h2>Recorded: {answer.upper()} for {host_date}</h2>"

@app.get("/rsvp/greeter/reply")
def rsvp_greeter_reply():
    token = request.args.get("token", "")
    answer = (request.args.get("answer", "") or "").lower().strip()

    if answer not in ("yes", "no"):
        abort(400, "answer must be yes or no")

    try:
        payload = read_token(token)
    except Exception:
        abort(400, "invalid token")

    email = payload.get("email")
    host_date = payload.get("date")
    if not email or not host_date:
        abort(400, "token missing fields")

    upsert_response(email, host_date, answer, 'Greeter')

    return f"<h2>Recorded: {answer.upper()} for {host_date}</h2>"

@app.get("/rsvp/host/send")
def rsvp_host_send():
    num_next_sunday = request.args.get("n", default=3, type=int)
    host_date = next_sunday(date.today(), num_next_sunday).isoformat()

    host_json_path = os.environ["PATH_HOST_LIST_JSON"]

    hosts = get_lists(host_json_path)
    hosts_email_lists = []
    for person in hosts:
        name = person.get("name")
        email = person.get("email")
        print(f"Name: {name}, Email: {email}")

        if not email:
            abort(400, 'no email')

        if not name:
            abort(400, 'no name')

        hosts_email_lists.append([name, email])
        result = send_rsvp_host_email(name, email, host_date)
        if not result["ok"]:
            # show a useful error on the page
            return (
                f"<h2>Failed sending RSVP (host) to {email} on {host_date}</h2>"
                f"<pre>{json.dumps(result, indent=2, default=str)}</pre>",
                500 if result.get("kind") == "exception" else 502,
            )

    return f"<h2>RSVP (host) Send to : {json.dumps(hosts_email_lists)} on {host_date}</h2>"

@app.get("/rsvp/greeter/send")
def rsvp_greeter_send():
    num_next_sunday = request.args.get("n", default=3, type=int)
    greeter_date = next_sunday(date.today(), num_next_sunday).isoformat()

    greeter_json_path = os.environ["PATH_GREETER_LIST_JSON"]

    greeters = get_lists(greeter_json_path)
    greeters_email_lists = []
    for person in greeters:
        name = person.get("name")
        email = person.get("email")
        print(f"Name: {name}, Email: {email}")

        if not email:
            abort(400, 'no email')

        if not name:
            abort(400, 'no name')

        greeters_email_lists.append([name, email])
        result = send_rsvp_greeter_email(name, email, greeter_date)
        if not result["ok"]:
            # show a useful error on the page
            return (
                f"<h2>Failed sending RSVP (greeter) to {email} on {greeter_date}</h2>"
                f"<pre>{json.dumps(result, indent=2, default=str)}</pre>",
                500 if result.get("kind") == "exception" else 502,
            )

    return f"<h2>RSVP (greeter) Send to : {json.dumps(greeters_email_lists)} on {greeter_date}</h2>"

def next_sunday(d: date, n: int = 1) -> date:
    """
    Return the n-th upcoming Sunday after date d.
    - n=1 => the next Sunday strictly after d
    - n=2 => the Sunday after that, etc.
    """
    if n < 1:
        raise ValueError("n must be >= 1")

    # Python: Monday=0 ... Sunday=6
    days_until_next = (6 - d.weekday()) % 7
    if days_until_next == 0:
        days_until_next = 7  # if d is Sunday, "next" means a week later

    return d + timedelta(days=days_until_next + 7 * (n - 1))

def get_lists(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        people_list = json.load(f)

    return people_list

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8500"))
    app.run(host="0.0.0.0", port=port, debug=True)

@app.errorhandler(400)
def handle_400(e):
    return jsonify(error=str(e.description)), 400

@app.errorhandler(500)
def handle_500(e):
    return jsonify(error=str(e.description)), 500
