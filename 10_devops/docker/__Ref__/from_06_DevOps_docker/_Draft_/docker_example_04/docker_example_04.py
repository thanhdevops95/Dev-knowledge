#!/usr/bin/env python3
import requests

print("Hello, Docker - Example 04!")
response = requests.get("https://api.github.com")
print("Status Code:", response.status_code)
print("Response Body:", response.text)