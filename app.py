from flask import Flask, jsonify, request
from threading import Lock
import time

app = Flask(__name__)

# Shared dictionary to hold the latest action
state = {
    "action": None,
    "direction": None
}
lock = Lock()  # Ensuring thread safety

# Endpoint to set scroll action to up or down using query parameters
@app.route('/scroll', methods=['GET'])
def scroll():
    direction = request.args.get('direction')  # Get 'direction' from query parameters
    
    if direction not in ['up', 'down']:
        return jsonify({"error": "Invalid direction. Use 'up' or 'down'."}), 400
    
    with lock:
        state["action"] = "scroll"
        state["direction"] = direction
    
    return jsonify({"status": f"Action set to scroll {direction}"}), 200

# Endpoint to check if there's an action to be performed
@app.route('/check_action', methods=['GET'])
def check_action():
    with lock:
        if state["action"]:
            # Return the current action
            response = jsonify({"action": state["action"], "direction": state["direction"]})
            # Reset action state after retrieving
            state["action"] = None
            state["direction"] = None
            return response, 200
        else:
            # No action to perform
            return jsonify({"action": None, "direction": None}), 200

if __name__ == '__main__':
    app.run(debug=True)
