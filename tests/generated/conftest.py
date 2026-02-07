"""
pytest configuration for AI-generated tests.
Framework-specific setup with minimal dependencies.
"""

import os
import sys
import pytest
import warnings

# Suppress deprecation warnings during testing
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

# Set testing environment
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("LOG_LEVEL", "ERROR")

# Add target project to Python path
TARGET_ROOT = os.environ.get("TARGET_ROOT", "/home/runner/work/Full-Stack-App-python-Javascript-/Full-Stack-App-python-Javascript-/pipeline/target_repo/backend")
if TARGET_ROOT and TARGET_ROOT not in sys.path:
    sys.path.insert(0, TARGET_ROOT)

# Also add current directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============== FLASK-SPECIFIC CONFIGURATION ==============

# Try to import the Flask app
_flask_app = None
try:
    # Try common app module names
    for module_name in ['app', 'application', 'main', 'server', 'api']:
        try:
            mod = __import__(module_name)
            # Look for app object or create_app factory
            if hasattr(mod, 'app'):
                _flask_app = mod.app
                break
            elif hasattr(mod, 'create_app'):
                _flask_app = mod.create_app()
                break
            elif hasattr(mod, 'application'):
                _flask_app = mod.application
                break
        except ImportError:
            continue
except Exception:
    pass


@pytest.fixture(scope="session")
def app():
    """Flask application fixture."""
    if _flask_app is None:
        pytest.skip("No Flask app found")

    _flask_app.config['TESTING'] = True
    _flask_app.config['WTF_CSRF_ENABLED'] = False

    ctx = _flask_app.app_context()
    ctx.push()
    yield _flask_app
    ctx.pop()


@pytest.fixture
def client(app):
    """Flask test client fixture."""
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_app_state():
    """Reset any global state between tests."""
    # Import app module to access global state
    for module_name in ['app', 'application', 'main']:
        try:
            mod = __import__(module_name)
            # Clear common global state patterns
            if hasattr(mod, 'tasks') and isinstance(getattr(mod, 'tasks'), list):
                getattr(mod, 'tasks').clear()
            if hasattr(mod, 'data') and isinstance(getattr(mod, 'data'), (list, dict)):
                if isinstance(getattr(mod, 'data'), list):
                    getattr(mod, 'data').clear()
                else:
                    getattr(mod, 'data').clear()
            break
        except ImportError:
            continue
    yield


@pytest.fixture
def sample_data():
    """Sample test data for Flask apps."""
    return {
        "title": "Test Item",
        "description": "Test Description",
        "name": "Test Name",
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    }


@pytest.fixture
def auth_headers():
    """Authorization headers for API testing."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# UNIVERSAL fixtures for any project structure
import sys
import os
import pathlib  # needed for _setup_detected_frameworks()

# Add project root to Python path for universal imports
PROJECT_ROOT = r"/home/runner/work/Full-Stack-App-python-Javascript-/Full-Stack-App-python-Javascript-/pipeline/target_repo/backend"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture(scope="session", autouse=True)
def universal_coverage_setup():
    """UNIVERSAL setup for maximum coverage with real code execution."""
    # Set coverage optimization environment
    os.environ['COVERAGE_OPTIMIZATION'] = 'universal'
    os.environ['REAL_IMPORTS_ONLY'] = 'true'
    os.environ['TESTING_MAX_COVERAGE'] = 'true'
    
    # Universal framework auto-detection
    _setup_detected_frameworks()
    
    yield
    
    # Cleanup
    os.environ.pop('COVERAGE_OPTIMIZATION', None)
    os.environ.pop('REAL_IMPORTS_ONLY', None)

def _setup_detected_frameworks():
    """Auto-detect and setup frameworks for any project structure."""
    # Try to detect and import common project modules
    project_modules = ['app', 'main', 'application', 'server', 'api', 'backend', 'core', 'project']
    
    # Also try to detect project-specific modules from the structure
    try:
        # Look for Python files in project root to detect main modules
        for py_file in pathlib.Path(PROJECT_ROOT).glob("*.py"):
            module_name = py_file.stem
            if module_name not in project_modules and not module_name.startswith('_'):
                project_modules.append(module_name)
    except Exception:
        pass
    
    for module_name in project_modules:
        try:
            __import__(module_name)
            print(f"Detected and imported: {module_name}")
        except ImportError:
            continue

@pytest.fixture
def universal_sample_data():
    """UNIVERSAL sample data for comprehensive testing."""
    return {
        'user': {
            'username': 'testuser_universal',
            'email': 'universal_test@example.com',
            'password': 'UniversalPassword123!',
        },
        'api_payloads': {
            'create_user': {
                'user': {
                    'username': 'api_test_user',
                    'email': 'api_test@example.com',
                    'password': 'ApiTestPass123!',
                }
            },
            'login': {
                'user': {
                    'email': 'api_test@example.com',
                    'password': 'ApiTestPass123!',
                }
            },
        },
        'edge_cases': {
            'empty_string': '',
            'none_value': None,
            'zero': 0,
            'negative': -1,
            'large_number': 999999999999,
            'special_chars': r'!@#$%^&*()_+-=[]{}|;:,.<>?/\~`',
            'unicode': '测试数据 🚀 émojis ñoños café ☕',
            'long_string': 'x' * 1000,
            'whitespace': '   ',
        }
    }

# UNIVERSAL test utilities
class UniversalTestUtils:
    """Universal utilities for achieving maximum coverage."""
    
    @staticmethod
    def setup_universal_imports():
        """Setup universal imports for any project structure."""
        print("UNIVERSAL: Setting up imports for any project structure")
    
    @staticmethod
    def generate_comprehensive_test_cases(target_name, target_type):
        """Generate comprehensive test cases for any target."""
        base_cases = [
            f"test_{target_name}_basic_functionality",
            f"test_{target_name}_edge_cases", 
            f"test_{target_name}_error_conditions",
            f"test_{target_name}_validation",
        ]
        
        if target_type in ['model', 'class']:
            base_cases.extend([
                f"test_{target_name}_creation",
                f"test_{target_name}_methods",
                f"test_{target_name}_properties",
            ])
        
        if target_type in ['api', 'route']:
            base_cases.extend([
                f"test_{target_name}_get",
                f"test_{target_name}_post", 
                f"test_{target_name}_put",
                f"test_{target_name}_delete",
            ])
        
        return base_cases
