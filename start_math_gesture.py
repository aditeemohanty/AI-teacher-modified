import subprocess
import webbrowser
import time

def start_streamlit():
    # Start the Streamlit app
    subprocess.Popen(["streamlit", "run", "main.py"])
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    # Open the browser
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    start_streamlit() 