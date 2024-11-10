from flask import Flask, jsonify, request
from threading import Lock
import pyautogui
import time 
import pygetwindow as gw

app = Flask(__name__)

# Shared dictionary to hold the latest action
state = {
    "action": None,
    "direction": None,
    "coordinates": None  # New key for storing click coordinates
}
lock = Lock()  # Ensuring thread safety

# # Function to locate the Firefox window and return its top-left coordinates
# def get_firefox_window():
#     print(gw.getAllTitles())
#     for window in gw.getAllWindows():
#         if "Mozilla Firefox" in window.title:
#             return window
#     return None


# # Function to smoothly scroll up in the Firefox window
# def scroll_up_in_firefox():
#     firefox_window = get_firefox_window()
#     if firefox_window:
#         firefox_window.activate()  # Bring Firefox window to the foreground
#         for i in range(10):  # Perform 10 small scroll increments
#             pyautogui.scroll(10)  # Scroll up by a small increment
#             time.sleep(0.1)  # Sleep for 100 milliseconds between scrolls
#         print("Scrolled up smoothly in Firefox")
#     else:
#         print("Firefox window not found")
# # Function to smoothly scroll down in the Firefox window
# def scroll_down_in_firefox():
#     firefox_window = get_firefox_window()
#     if firefox_window:
#         firefox_window.activate()  # Bring Firefox window to the foreground
#         for i in range(10):  # Perform 10 small scroll increments
#             pyautogui.scroll(-10)  # Scroll down by a small increment
#             time.sleep(0.1)  # Sleep for 100 milliseconds between scrolls
#         print("Scrolled down smoothly in Firefox")
#     else:
#         print("Firefox window not found")

def scroll_up():
    time.sleep(10)
    for i in range(10):  # Perform 10 small scroll increments
        pyautogui.scroll(5)  # Scroll up by a small increment
        time.sleep(0.1)
    print("Scrolled up")

# Function to scroll down
def scroll_down():
    time.sleep(10)
    for i in range(10):  # Perform 10 small scroll increments
        pyautogui.scroll(-5)  # Scroll down by a small increment
        time.sleep(0.1)
    print("Scrolled down")

# Function to perform a click at the specified (x, y) coordinates
def click_at(x, y):
    time.sleep(10)
    pyautogui.click(x, y)  # Click at the given (x, y) coordinates y,x?
    print(f"Clicked at ({x}, {y})")

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

    if direction == "up":
        scroll_up()
    elif direction == "down":
        scroll_down()

    return jsonify({"status": f"Action set to {action} {direction}"}), 200

# Endpoint to handle click action with coordinates
@app.route('/click', methods=['GET'])
def click():
    # Get the 'x' and 'y' query parameters
    x = request.args.get('x')
    y = request.args.get('y')

    # Validate the coordinates (ensure they are integers)
    try:
        x = int(x)
        y = int(y)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid coordinates. 'x' and 'y' must be integers."}), 400

    # Update shared state with click action and coordinates
    with lock:
        state["action"] = "click"
        state["coordinates"] = {"x": x, "y": y}
    click_at(x, y)
    return jsonify({"status": f"Click action set at coordinates ({x}, {y})"}), 200

# Endpoint to check if there's an action to be performed
@app.route('/check_action', methods=['GET'])
def check_action():
    with lock:
        if state["action"]:
            # Return the current action
            response = jsonify({
                "action": state["action"],
                "direction": state.get("direction"),
                "coordinates": state.get("coordinates")
            })
            # Reset action state after retrieving
            state["action"] = None
            state["direction"] = None
            state["coordinates"] = None
            return response, 200
        else:
            # No action to perform
            return jsonify({"action": None, "direction": None, "coordinates": None}), 200

if __name__ == '__main__':
    app.run(debug=True)
