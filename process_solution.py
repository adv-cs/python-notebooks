#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def process_notebook(input_path: Path) -> None:
    if not input_path.exists():
        print(f"Error: File '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)

    if input_path.suffix != ".ipynb":
        print(f"Error: '{input_path}' is not a .ipynb file.", file=sys.stderr)
        sys.exit(1)

    # Read the Jupyter Notebook JSON
    with open(input_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Empty source code, outputs, and execution counts for code cells
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["source"] = []
            cell["outputs"] = []
            cell["execution_count"] = None

    # Create the 'student' subdirectory in the input file's directory
    output_dir = input_path.parent / "student"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / input_path.name

    # Write the stripped notebook
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write("\n")

    print(f"Successfully saved cleared notebook to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Remove code contents from Jupyter Notebook code cells."
    )
    parser.add_argument("notebook", type=Path, help="Path to the .ipynb file")

    args = parser.parse_args()
    process_notebook(args.notebook)


if __name__ == "__main__":
    main()