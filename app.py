from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "tickets.json"

def load_tickets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tickets(tickets):
    with open(DATA_FILE, "w") as f:
        json.dump(tickets, f, indent=2)

@app.route("/")
def index():
    tickets = load_tickets()
    status_filter = request.args.get("status", "All")
    priority_filter = request.args.get("priority", "All")

    if status_filter != "All":
        tickets = [t for t in tickets if t["status"] == status_filter]
    if priority_filter != "All":
        tickets = [t for t in tickets if t["priority"] == priority_filter]

    return render_template("index.html", tickets=tickets,
                           status_filter=status_filter,
                           priority_filter=priority_filter)

@app.route("/create", methods=["POST"])
def create():
    tickets = load_tickets()
    new_ticket = {
        "id": len(tickets) + 1,
        "title": request.form["title"],
        "description": request.form["description"],
        "priority": request.form["priority"],
        "status": "Open",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tickets.append(new_ticket)
    save_tickets(tickets)
    return redirect(url_for("index"))

@app.route("/update/<int:ticket_id>", methods=["POST"])
def update(ticket_id):
    tickets = load_tickets()
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = request.form["status"]
            break
    save_tickets(tickets)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)