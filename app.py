from flask import Flask, render_template, jsonify
import subprocess
import threading
import time
import os

app = Flask(__name__)
streamlit_process = None

@app.route('/start-math-gesture')
def start_math_gesture():
    global streamlit_process
    try:
        if streamlit_process is None:
            # Kill any existing Streamlit processes
            os.system("kill -9 $(ps aux | grep 'streamlit run main.py' | grep -v grep | awk '{print $2}')")
            
            # Start Streamlit in a new process
            streamlit_process = subprocess.Popen(
                ["streamlit", "run", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for Streamlit to start
            time.sleep(2)
            
            return jsonify({"status": "success", "message": "Math Gesture Solver Started"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 