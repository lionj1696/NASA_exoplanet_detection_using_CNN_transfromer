import os

DIRS = [
    "data/raw",
    "data/processed",
    "data/augmented",
    "outputs/models",
    "outputs/figures",
    "outputs/results",
]

for d in DIRS:
    os.makedirs(d, exist_ok=True)
    print(f"Created: {d}")

print("Project directory structure ready.")
