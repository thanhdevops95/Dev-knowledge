# 📋 Cheatsheet: Python Basics

> **Quick Reference for Python in DevOps**
>
> *Tra cứu nhanh Python cho DevOps*

---

## 📊 Data Types

```python
# Strings
name = "DevOps"
path = '/etc/nginx/nginx.conf'
multiline = """
This is a
multiline string
"""

# Numbers
count = 10              # int
percentage = 99.9       # float
port = 8080            # int

# Boolean
enabled = True
running = False

# None
result = None
```

---

## 📝 String Operations

```python
# Basic operations
s = "hello world"
s.upper()              # "HELLO WORLD"
s.lower()              # "hello world"
s.capitalize()         # "Hello world"
s.title()              # "Hello World"
s.strip()              # Remove whitespace
s.split()              # ['hello', 'world']
s.replace('hello', 'hi')  # "hi world"

# Format strings
name = "nginx"
port = 80
f"Server {name} on port {port}"    # f-string
"Server {} on port {}".format(name, port)
"Server %s on port %d" % (name, port)

# String methods
s.startswith("hello")  # True
s.endswith("world")    # True
s.find("wor")          # 6 (index)
"hello" in s           # True
len(s)                 # 11
```

---

## 📋 Lists

```python
# Create
servers = ["web1", "web2", "db1"]
ports = [80, 443, 3306]
mixed = ["nginx", 80, True]

# Access
servers[0]             # "web1"
servers[-1]            # "db1"
servers[0:2]           # ["web1", "web2"]

# Modify
servers.append("db2")  # Add to end
servers.insert(0, "lb1")  # Insert at position
servers.remove("web2") # Remove by value
servers.pop()          # Remove last
servers.pop(0)         # Remove at index

# Operations
len(servers)           # Length
servers.sort()         # Sort in place
sorted(servers)        # Return sorted copy
servers.reverse()      # Reverse in place
"web1" in servers      # Check membership

# List comprehension
ports = [80, 443, 8080]
https_ports = [p for p in ports if p != 80]
doubled = [p * 2 for p in ports]
```

---

## 📖 Dictionaries

```python
# Create
server = {
    "name": "web1",
    "ip": "192.168.1.10",
    "port": 80,
    "enabled": True
}

# Access
server["name"]         # "web1"
server.get("name")     # "web1"
server.get("location", "default")  # With default

# Modify
server["port"] = 8080  # Update
server["region"] = "us-east"  # Add new

# Methods
server.keys()          # dict_keys(['name', 'ip', ...])
server.values()        # dict_values(['web1', ...])
server.items()         # dict_items([('name', 'web1'), ...])

# Check
"name" in server       # True
server.pop("region")   # Remove and return

# Iteration
for key in server:
    print(key, server[key])

for key, value in server.items():
    print(f"{key}: {value}")

# Dict comprehension
ports = {"http": 80, "https": 443}
reversed_ports = {v: k for k, v in ports.items()}
```

---

## 🔄 Control Flow

### If/Elif/Else

```python
status = 200

if status == 200:
    print("OK")
elif status == 404:
    print("Not Found")
elif status >= 500:
    print("Server Error")
else:
    print("Unknown")

# Ternary
result = "success" if status == 200 else "failure"
```

### Loops

```python
# For loop
servers = ["web1", "web2", "web3"]

for server in servers:
    print(server)

for i, server in enumerate(servers):
    print(f"{i}: {server}")

for i in range(5):      # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):   # 1, 2, 3, 4, 5
    print(i)

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# Break and Continue
for server in servers:
    if server == "web2":
        continue        # Skip this iteration
    if server == "web3":
        break          # Exit loop
    print(server)
```

---

## 🔧 Functions

```python
# Basic function
def greet(name):
    return f"Hello, {name}!"

# Default parameters
def connect(host, port=22):
    return f"Connecting to {host}:{port}"

# *args and **kwargs
def log(*messages, level="INFO"):
    for msg in messages:
        print(f"[{level}] {msg}")

def configure(**settings):
    for key, value in settings.items():
        print(f"{key} = {value}")

# Lambda
square = lambda x: x ** 2
is_running = lambda s: s.get("status") == "running"

# Usage
greet("DevOps")
connect("192.168.1.1")
connect("192.168.1.1", 8080)
log("Starting", "Processing", level="DEBUG")
configure(host="localhost", port=3306)
```

---

## 📁 File Operations

```python
# Read file
with open("/etc/hosts", "r") as f:
    content = f.read()       # Read all
    
with open("/etc/hosts", "r") as f:
    lines = f.readlines()    # List of lines

with open("/etc/hosts", "r") as f:
    for line in f:           # Line by line
        print(line.strip())

# Write file
with open("output.txt", "w") as f:
    f.write("Hello World\n")

# Append to file
with open("log.txt", "a") as f:
    f.write("New log entry\n")

# Check file exists
import os
os.path.exists("/etc/hosts")    # True
os.path.isfile("/etc/hosts")    # True
os.path.isdir("/etc")           # True
```

---

## 📂 OS Module

```python
import os

# Environment variables
os.environ["HOME"]              # Get env var
os.environ.get("API_KEY", "")   # With default
os.getenv("PATH")               # Alternative

# File system
os.getcwd()                     # Current directory
os.chdir("/tmp")                # Change directory
os.listdir("/etc")              # List directory
os.mkdir("new_dir")             # Create directory
os.makedirs("a/b/c", exist_ok=True)  # Create nested
os.remove("file.txt")           # Delete file
os.rmdir("empty_dir")           # Delete empty dir

# Path operations
os.path.join("/etc", "nginx", "nginx.conf")
os.path.basename("/etc/nginx/nginx.conf")  # "nginx.conf"
os.path.dirname("/etc/nginx/nginx.conf")   # "/etc/nginx"
os.path.splitext("file.txt")    # ("file", ".txt")
os.path.abspath(".")            # Absolute path

# Execute commands
os.system("ls -la")             # Simple execution
```

---

## 💻 Subprocess Module

```python
import subprocess

# Run command
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)

# Run with shell
result = subprocess.run("ls -la | grep py", shell=True, capture_output=True, text=True)

# Check output
output = subprocess.check_output(["hostname"])
print(output.decode())

# With error handling
try:
    result = subprocess.run(["ls", "/nonexistent"], check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")

# Popen for more control
process = subprocess.Popen(
    ["ping", "-c", "3", "google.com"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()
```

---

## 🌐 Requests (HTTP)

```python
import requests

# GET request
response = requests.get("https://api.github.com")
print(response.status_code)     # 200
print(response.json())          # Parse JSON

# With headers
headers = {"Authorization": "Bearer token123"}
response = requests.get("https://api.example.com", headers=headers)

# POST request
data = {"name": "server1", "type": "web"}
response = requests.post("https://api.example.com/servers", json=data)

# Error handling
response = requests.get("https://api.example.com")
response.raise_for_status()     # Raise exception if error

# Timeout
response = requests.get("https://api.example.com", timeout=5)
```

---

## 📋 JSON Handling

```python
import json

# Parse JSON string
json_string = '{"name": "server1", "port": 80}'
data = json.loads(json_string)
print(data["name"])

# Convert to JSON string
data = {"name": "server1", "port": 80}
json_string = json.dumps(data)
json_pretty = json.dumps(data, indent=2)

# Read JSON file
with open("config.json", "r") as f:
    config = json.load(f)

# Write JSON file
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

## 📋 YAML Handling

```python
import yaml  # pip install pyyaml

# Read YAML file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Write YAML file
data = {
    "server": {
        "host": "localhost",
        "port": 8080
    }
}
with open("output.yaml", "w") as f:
    yaml.dump(data, f, default_flow_style=False)

# Parse YAML string
yaml_string = """
servers:
  - name: web1
    port: 80
  - name: web2
    port: 443
"""
data = yaml.safe_load(yaml_string)
```

---

## ⚠️ Error Handling

```python
# Try/Except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

# Multiple exceptions
try:
    file = open("missing.txt")
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Cleanup code")

# Raise exception
def validate_port(port):
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid port: {port}")
    return port
```

---

## 🧩 Common Patterns

### Config Parser

```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
host = config.get("database", "host")
port = config.getint("database", "port")
```

### Argument Parser

```python
import argparse

parser = argparse.ArgumentParser(description="My DevOps script")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-c", "--config", default="config.yaml")
parser.add_argument("host", help="Target host")
args = parser.parse_args()

print(args.host, args.verbose, args.config)
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.info("Script started")
logger.warning("Low disk space")
logger.error("Connection failed")
```

---

## 🔗 Quick Reference

| Task | Code |
|------|------|
| Read file | `open(f).read()` |
| Write file | `open(f, 'w').write(s)` |
| Run command | `subprocess.run([...])` |
| HTTP GET | `requests.get(url)` |
| Parse JSON | `json.loads(s)` |
| Parse YAML | `yaml.safe_load(s)` |
| Env variable | `os.getenv('KEY')` |
| File exists | `os.path.exists(f)` |
| List dir | `os.listdir(d)` |
| Current dir | `os.getcwd()` |

---

**[← Back to README](./README.md)**
