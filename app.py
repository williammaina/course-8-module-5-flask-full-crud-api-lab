from flask import Flask, jsonify, request

app = Flask(__name__)

class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    # Calculate new ID
    new_id = max([e.id for e in events]) + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    event = next((e for e in events if e.id == event_id), None)
    
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    if "title" in data:
        event.title = data["title"]
        return jsonify(event.to_dict()), 200
    return jsonify({"error": "No title provided"}), 400

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    event = next((e for e in events if e.id == event_id), None)
    
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    events = [e for e in events if e.id != event_id]
    return jsonify({"message": f"Event {event_id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)