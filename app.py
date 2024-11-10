from flask import Flask, jsonify, request
from threading import Lock

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
    # Check for both 'action' and 'direction' in query parameters
    action = request.args.get('action')
    direction = request.args.get('direction')
    
    # Validate action and direction
    if action != "scroll" or direction not in ['up', 'down']:
        return jsonify({"error": "Invalid parameters. Use 'action=scroll' and 'direction=up' or 'down'."}), 400

    # Update shared state with action and direction
    with lock:
        state["action"] = action
        state["direction"] = direction

    return jsonify({"status": f"Action set to {action} {direction}"}), 200

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
