import os

import numpy as np


INPUT_PATH = os.path.join(os.getcwd(), 'data')
OUTPUT_PATH = os.path.join(os.getcwd(), 'build')


def run(data=INPUT_PATH, build=OUTPUT_PATH, num=0):

    print(f"Running test with num = {num}")

    # --- Settings ---
    input_file = os.path.join(data, 'test.txt')
    output_file = os.path.join(build, f'test_{num}.txt')

    # --- Read the original file ---
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # --- Append the new string ---
    content += f"({np.sum(num)})"

    # --- Make sure the output directory exists ---
    os.makedirs(build, exist_ok=True)

    # --- Save the new file ---
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ File saved to: {output_file}")