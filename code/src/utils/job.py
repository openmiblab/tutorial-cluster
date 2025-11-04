import os

import numpy as np



def run(data=None, build=None, num=0):

    if (data is None) or (build is None):
        raise ValueError('Please provide data and build directories.')

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