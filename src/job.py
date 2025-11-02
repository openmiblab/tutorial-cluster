import os

import numpy as np


def run(num=0):

    print(f"Running test with num = {num}")

    # --- Settings ---
    input_path = os.path.join(os.getcwd(), 'data', 'test.txt')
    output_path = os.path.join(os.getcwd(), 'build', f'test_{num}.txt')

    # --- Read the original file ---
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- Append the new string ---
    content += ' vriend'
    content += f" ({np.exp(num)})"

    # --- Make sure the output directory exists ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # --- Save the new file ---
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ File saved to: {output_path}")


