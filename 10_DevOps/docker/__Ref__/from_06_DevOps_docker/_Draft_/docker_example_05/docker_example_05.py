#!/usr/bin/env python3

import sys

print("Hello, Docker - Example 05!")
if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            print(f"Tham số dòng lệnh {i}: {sys.argv[i]}")
    else:
        print("Không có tham số dòng lệnh được cung cấp.")