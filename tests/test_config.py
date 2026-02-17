
import pytest
import os
from app.core import config
from pydantic import ValidationError

# We use fixture to cleanup environment variables after tests
@pytest.fixture
def mock_env():
    original_environ = os.environ.copy()
    yield os.environ
    os.environ.clear()
    os.environ.update(original_environ)

def test_config_loading(mock_env):
    # Set environment variables
    os.environ["SECRET_KEY"] = "test_secret_override"
    os.environ["LLM_API_KEY"] = "test_llm_key_override"
    # Set required field project name as well since we are creating new instance
    # It has default values but we can override
    os.environ["PROJECT_NAME"] = "Test Project"

    # Create a new instance of Settings to load these new env vars
    # We pass _env_file=None to ignore .env file and rely purely on env vars for this test
    # (Although Env vars usually override .env, explicit is better for unit test isolation if we want to test env vars specifically)
    settings = config.Settings(_env_file=None)
    
    # Check if env vars are picked up
    assert settings.SECRET_KEY.get_secret_value() == "test_secret_override"
    assert settings.LLM_API_KEY.get_secret_value() == "test_llm_key_override"
    assert settings.PROJECT_NAME == "Test Project"


def test_missing_required_config(mock_env):
    # Unset required variables
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]
    if "LLM_API_KEY" in os.environ:
        del os.environ["LLM_API_KEY"]
        
    # We must ensure it doesn't read from .env file during this test
    # passing _env_file=None avoids reading from default .env
    
    with pytest.raises(ValidationError):
        config.Settings(_env_file=None)

def test_load_from_env_file():
    # This test verifies it CAN load from the .env file we created (dummy one)
    # We ensure specific env vars are NOT set so it falls back to .env
    
    # We need to rely on the fact that existing process env vars might interfere, 
    # so we should use mock_env fixture or manually unset them.
    # But since we are allowed to have .env file, we proceed.
    
    # We create a new Settings instance. It should read from `.env` by default (model_config)
    # UNLESS env vars are set.
    
    # Let's unset specific keys to test file loading
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]
    if "LLM_API_KEY" in os.environ:
        del os.environ["LLM_API_KEY"]
        
    settings = config.Settings()
    
    # These values must match what is in our dummy .env file
    assert settings.SECRET_KEY.get_secret_value() == "test_secret_key_12345"
    assert settings.LLM_API_KEY.get_secret_value() == "test_llm_key_12345"
