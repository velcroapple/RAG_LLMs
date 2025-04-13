import os
import subprocess
import platform
import time
import socket
def print_step(msg):
    print("\n" + "="*50)
    print(f" {msg}")
    print("="*50 + "\n")

# --- STEP 1: Install Requirements ---
print_step("Installing Python packages from requirements.txt")
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

# --- STEP 2: Start Docker Qdrant ---
print_step("Starting Qdrant Docker container on port 6333")
subprocess.run([
    "docker", "run", "-d",
    "-p", "6333:6333",
    "--name", "rag_qdrant",
    "qdrant/qdrant"
], stderr=subprocess.DEVNULL)
import socket

def is_qdrant_running(host="localhost", port=6333):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        return result == 0

# --- AFTER docker run ---
print_step("Verifying if Qdrant is running on port 6333...")

if is_qdrant_running():
    print(" Qdrant server is UP on http://localhost:6333")
else:
    print(" Qdrant failed to start. Please check Docker or try restarting the script.")
    exit(1)

# Wait a few seconds for Qdrant to come up
time.sleep(5)

# --- STEP 3: Embed & Upload to Qdrant ---
print_step("Running embedder.py to upload chunks to Qdrant")
subprocess.run(["python", "embedder.py"], check=True)

# --- STEP 4: Download Mistral (Ollama) ---
print_step("Checking if Mistral is available in Ollama")
try:
    subprocess.run(["ollama", "list"], check=True, stdout=subprocess.DEVNULL)
except FileNotFoundError:
    print(" Ollama is not installed. Please download it from https://ollama.com/download and rerun this script.")
    exit(1)

print_step("Downloading Mistral model (if not already installed)")
subprocess.run(["ollama", "pull", "mistral"], check=True)

# --- STEP 5: Launch Streamlit App ---
print_step("Launching Streamlit app (in your browser)")
subprocess.run(["streamlit", "run", "streamlit.py"], check=True)
