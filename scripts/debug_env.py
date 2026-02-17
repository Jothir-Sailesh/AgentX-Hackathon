import sys
import os

with open("debug_results.txt", "w", encoding="utf-8") as f:
    f.write(f"Python executable: {sys.executable}\n")
    f.write(f"Python version: {sys.version}\n")
    f.write(f"Current working directory: {os.getcwd()}\n")
    f.write(f"sys.path: {sys.path}\n")

    try:
        import pydantic
        f.write(f"✅ pydantic version: {pydantic.VERSION}\n")
    except ImportError as e:
        f.write(f"❌ Failed to import pydantic: {e}\n")

    try:
        import pydantic_settings
        f.write(f"✅ pydantic_settings imported successfully\n")
    except ImportError as e:
        f.write(f"❌ Failed to import pydantic_settings: {e}\n")

    try:
        sys.path.append(os.getcwd())
        from app.core.config import settings
        f.write(f"✅ app.core.config imported successfully\n")
    except ImportError as e:
        f.write(f"❌ Failed to import app.core.config: {e}\n")
    except Exception as e:
        f.write(f"❌ Error importing app.core.config: {e}\n")

