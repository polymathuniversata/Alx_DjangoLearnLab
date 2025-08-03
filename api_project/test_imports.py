import sys
import os

print("Python Path:")
for path in sys.path:
    print(f"- {path}")

print("\nCurrent Directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))
