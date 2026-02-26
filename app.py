import os
from flask import Flask, request, abort
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
    email = request.args.get("email", default='', type=str)
    num_next_sunday = request.args.get("n", default=3, type=int)

    if not email:
        abort(400, 'no email')

    host_date = next_sunday(date.today(), num_next_sunday).isoformat()
    send_rsvp_host_email(email, host_date)

    return f"<h2>RSVP (host) Send to : {email} on {host_date}</h2>"

@app.get("/rsvp/greeter/send")
def rsvp_greeter_send():
    email = request.args.get("email", default="", type=str)
    num_next_sunday = request.args.get("n", default=3, type=int)

    if not email:
        abort(400, 'no email')

    greeter_date = next_sunday(date.today(), num_next_sunday).isoformat()
    send_rsvp_greeter_email(email, greeter_date)

    return f"<h2>RSVP (greeter) Send to : {email} on {greeter_date}</h2>"

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8500"))
    app.run(host="0.0.0.0", port=port, debug=True)
