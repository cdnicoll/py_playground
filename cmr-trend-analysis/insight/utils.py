"""Utility functions for the insight agent."""

import os
from typing import Optional


def load_transcript(file_path: str) -> Optional[str]:
    """
    Load transcript text from a file.

    Args:
        file_path: Path to the transcript file

    Returns:
        The transcript content as a string, or None if loading fails
    """
    try:
        with open(file_path, "r") as file:
            transcript_content = file.read()
            print(
                f"Successfully loaded transcript ({len(transcript_content)} characters)")
            return transcript_content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        print("Make sure you're running the script from the correct directory")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def get_sample_path(filename: str) -> str:
    """
    Get the absolute path to a sample file.

    Args:
        filename: Name of the sample file

    Returns:
        Absolute path to the sample file
    """
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the samples directory
    samples_dir = os.path.join(current_dir, "samples")
    # Return the path to the specified file
    return os.path.join(samples_dir, filename)
