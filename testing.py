import os
import clique
from typing import List, Tuple, Dict
from itertools import zip_longest


def find_string_differences(files: List[str]) -> Dict[str, str]:
    """
    Find common parts and differences between all strings in a list.
    Returns dictionary with original strings as keys and unique parts as values.
    The unique parts will:
    - not include file extensions
    - be stripped of whitespace
    - be stripped of dots and underscores from both ends
    - stripped of sequence numbers and padding

    Example:
    """
    if not files:
        return {}

    # convert first all files to collections and reminders
    files_collected = []
    collections, reminders = clique.assemble(files)
    for collection in collections:
        head = collection.format("{head}")
        tail = collection.format("{tail}")
        files_collected.append(head + tail)
    for reminder in reminders:
        files_collected.append(reminder)

    # Remove extensions and convert to list for processing
    processed_files = [os.path.splitext(f)[0] for f in files_collected]

    # Find common prefix using zip_longest to compare all characters at once
    prefix = ""
    for chars in zip_longest(*processed_files):
        if len(set(chars) - {None}) != 1:  # If there's more than one unique character
            break
        prefix += chars[0]

    # Find common suffix by reversing strings
    reversed_files = [f[::-1] for f in processed_files]
    suffix = ""
    for chars in zip_longest(*reversed_files):
        if len(set(chars) - {None}) != 1:
            break
        suffix = chars[0] + suffix

    # Create result dictionary
    prefix_len = len(prefix)
    suffix_len = len(suffix)
    result = {}

    for original, processed in zip(files_collected, processed_files):
        # Extract the difference
        diff = processed[prefix_len:-suffix_len] if suffix else processed[prefix_len:]
        # Clean up the difference
        diff = diff.strip()  # Remove whitespace
        diff = diff.strip("._")  # Remove dots and underscores
        result[original] = diff

    return result


# Example usage:
files = [
    "jt3dfile_0010_0050_b1c1.0001006.exr",
    "jt3dfile_0010_0050_b1c1.0001005.exr",
    "jt3dfile_0010_0050_b1c1.0001003.exr",
    "jt3dfile_0010_0050_b1c1.0001002.exr",
    "jt3dfile_0010_0050_b1c1.0001004.exr",
    "jt3dfile_0010_0050_b1c1.0001007.exr",
    "jt3dfile_0010_0050_b1c1.0001001.exr",
    "jt3dfile_0010_0050_b1c1.0001008.exr",
    "jt3dfile_0010_0050_b1c1.0001009.exr",
    "jt3dfile_0010_0050_b1c1_dsd.0001008.exr",
    "jt3dfile_0010_0050_b1c1_dsd.0001009.exr",
    "jt3dfile_0010_0050_b1c1.thumbnail.jpg",
    "jt3dfile_0010_0050_b1c1_dnxhdburnin.mov",
    "jt3dfile_0010_0050_b1c1_proresburnin.mov",
    "jt3dfile_0010_0050_b1c1_h264burnin.mp4",
]

result = find_string_differences(files)
for original, diff in result.items():
    print(f"{original}: {diff}")
