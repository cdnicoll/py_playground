"""Pytest configuration file for the insight module tests."""

import os
import sys
import pytest

# Add the parent directory to sys.path to make the insight module importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_transcript_content():
    """Return sample transcript content for testing."""
    return """
    This is a sample transcript.
    It contains multiple lines.
    And some sample content for testing.
    """


@pytest.fixture
def mock_file_path():
    """Return a mock file path for testing."""
    return os.path.join("samples", "test_transcript.txt")
