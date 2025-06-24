"""Integration tests for the utils module."""

from utils import load_transcript, get_sample_path
import os
import pytest
import tempfile
from pathlib import Path

import sys
# Add the parent directory to the path so we can import the utils module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestLoadTranscriptIntegration:
    """Integration tests for the load_transcript function."""

    def test_load_transcript_with_real_file(self):
        """Test load_transcript with a real temporary file."""
        # Create a temporary file with some content
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(
                "This is a test transcript file.\nWith multiple lines.")
            temp_path = temp_file.name

        try:
            # Test loading the file
            content = load_transcript(temp_path)

            # Verify the content was loaded correctly
            assert content == "This is a test transcript file.\nWith multiple lines."
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)

    def test_load_transcript_nonexistent_file(self):
        """Test load_transcript with a nonexistent file."""
        # Use a path that definitely doesn't exist
        nonexistent_path = "/path/to/nonexistent/file_that_does_not_exist.txt"

        # Test loading the nonexistent file
        content = load_transcript(nonexistent_path)

        # Verify that None is returned
        assert content is None


class TestGetSamplePathIntegration:
    """Integration tests for the get_sample_path function."""

    def test_get_sample_path_structure(self):
        """Test that get_sample_path returns a path with the correct structure."""
        # Call the function
        path = get_sample_path("test.txt")

        # Convert to Path object for easier manipulation
        path_obj = Path(path)

        # Check that the path ends with samples/test.txt
        assert path_obj.name == "test.txt"
        assert path_obj.parent.name == "samples"

        # The path should be absolute
        assert os.path.isabs(path)
