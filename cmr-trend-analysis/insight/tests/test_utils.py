"""Tests for the utils module."""

from utils import load_transcript, get_sample_path
import os
import pytest
from unittest.mock import patch, mock_open

import sys
# Add the parent directory to the path so we can import the utils module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestLoadTranscript:
    """Tests for the load_transcript function."""

    @patch("builtins.open", new_callable=mock_open, read_data="Test transcript content")
    def test_load_transcript_success(self, mock_file):
        """Test that load_transcript returns the content of the file."""
        # Call the function
        result = load_transcript("fake_path.txt")

        # Check that the file was opened
        mock_file.assert_called_once_with("fake_path.txt", "r")

        # Check that the function returned the content
        assert result == "Test transcript content"

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_load_transcript_file_not_found(self, mock_print, mock_file):
        """Test that load_transcript handles FileNotFoundError."""
        # Call the function
        result = load_transcript("nonexistent_file.txt")

        # Check that the function returned None
        assert result is None

        # Check that the appropriate error messages were printed
        mock_print.assert_any_call(
            "Error: File not found at nonexistent_file.txt")
        mock_print.assert_any_call(
            "Make sure you're running the script from the correct directory")

    @patch("builtins.open", side_effect=Exception("Test exception"))
    @patch("builtins.print")
    def test_load_transcript_general_exception(self, mock_print, mock_file):
        """Test that load_transcript handles general exceptions."""
        # Call the function
        result = load_transcript("problematic_file.txt")

        # Check that the function returned None
        assert result is None

        # Check that the appropriate error message was printed
        mock_print.assert_called_with("Error reading file: Test exception")


class TestGetSamplePath:
    """Tests for the get_sample_path function."""

    @patch("os.path.dirname")
    @patch("os.path.abspath")
    @patch("os.path.join")
    def test_get_sample_path(self, mock_join, mock_abspath, mock_dirname):
        """Test that get_sample_path constructs the path correctly."""
        # Set up the mocks with generic paths that don't depend on specific machine
        mock_abspath.return_value = "/path/to/utils.py"
        mock_dirname.return_value = "/path/to"
        mock_join.side_effect = lambda *args: "/".join(args)

        # Call the function
        result = get_sample_path("test.txt")

        # Check that the path was constructed correctly
        # Don't test the specific path that was passed to abspath
        # Just check that it was called once
        assert mock_abspath.call_count == 1
        mock_dirname.assert_called_once_with("/path/to/utils.py")

        # Check the first join call (for samples_dir)
        assert mock_join.call_args_list[0][0] == ("/path/to", "samples")

        # Check the second join call (for the final path)
        assert mock_join.call_args_list[1][0][0] == "/path/to/samples"
        assert mock_join.call_args_list[1][0][1] == "test.txt"

        # The final result should be the path to the sample file
        assert result == "/path/to/samples/test.txt"
