import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        "TESTING": True,
        "MODEL_PATH": "test_model.pkl",
        "MODEL_INFO_PATH": "test_model_info.pkl"
    } 