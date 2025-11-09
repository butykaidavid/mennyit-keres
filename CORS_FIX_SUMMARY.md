# CORS_ORIGINS JSON Parsing Error - Fix Summary

## Problem

The application was failing to start with the following error:

```
pydantic_settings.sources.SettingsError: error parsing value for field "CORS_ORIGINS" from source "EnvSettingsSource"
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

This error occurred when the `CORS_ORIGINS` environment variable was:
- Empty string
- Not set
- Not in valid JSON format
- Set to whitespace only

## Root Cause

The `CORS_ORIGINS` field in `backend/app/config/settings.py` was defined as `List[str]`, and pydantic-settings attempts to parse list types from environment variables as JSON. When the environment variable was empty or not valid JSON, the parsing would fail.

## Solution

Added a custom `field_validator` to handle multiple input formats gracefully:

1. **JSON array format**: `["http://localhost:3000","http://localhost:8000"]`
2. **Comma-separated format**: `http://localhost:3000,http://localhost:8000`
3. **Single URL**: `http://localhost:3000`
4. **Empty or unset**: Falls back to default values

## Changes Made

### 1. Updated `backend/app/config/settings.py`

Added imports:
```python
from pydantic import field_validator, ValidationInfo
import json
```

Added custom validator:
```python
@field_validator('CORS_ORIGINS', mode='before')
@classmethod
def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
    """
    Parse CORS_ORIGINS from various input formats:
    - JSON array string: '["http://localhost:3000","http://localhost:8000"]'
    - Comma-separated string: 'http://localhost:3000,http://localhost:8000'
    - Python list: ["http://localhost:3000", "http://localhost:8000"]
    - Empty string: '' (returns default)
    """
    # If already a list, return it
    if isinstance(v, list):
        return v
    
    # If empty or None, return default
    if not v or v.strip() == "":
        return ["http://localhost:3000", "http://localhost:8000"]
    
    # Try parsing as JSON
    if isinstance(v, str):
        v = v.strip()
        if v.startswith('[') and v.endswith(']'):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
        
        # Try comma-separated format
        if ',' in v:
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        
        # Single URL
        return [v]
    
    # Fallback to default
    return ["http://localhost:3000", "http://localhost:8000"]
```

### 2. Updated `docker-compose.yml`

Added explicit `CORS_ORIGINS` environment variable to the backend service:

```yaml
environment:
  # ... other variables ...
  CORS_ORIGINS: ${CORS_ORIGINS:-["http://localhost:3000","http://localhost:8000"]}
```

### 3. Updated `.env.example`

Added documentation for the multiple supported formats:

```bash
# CORS_ORIGINS can be specified in multiple formats:
# - JSON array: ["http://localhost:3000","http://localhost:8000"]
# - Comma-separated: http://localhost:3000,http://localhost:8000
# - Single URL: http://localhost:3000
# - Empty (uses default): 
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

## Testing

All test cases pass successfully:

- ✓ Empty string → Returns default
- ✓ JSON array → Parsed correctly
- ✓ Comma-separated → Parsed correctly  
- ✓ Single URL → Parsed correctly
- ✓ Python list → Returned as-is
- ✓ Whitespace → Returns default
- ✓ Comma-separated with spaces → Parsed correctly

## Benefits

1. **Robust error handling**: No more crashes from empty or invalid CORS_ORIGINS
2. **Flexible configuration**: Multiple formats supported for developer convenience
3. **Sensible defaults**: Always falls back to localhost development URLs
4. **Better DX**: Clear documentation in .env.example
5. **Production ready**: Works in containerized environments and cloud deployments

## Deployment Notes

- **Railway/Render**: Can use comma-separated format: `CORS_ORIGINS=https://app.example.com,https://www.example.com`
- **Docker**: JSON format works: `CORS_ORIGINS=["https://app.example.com"]`
- **Local development**: Leave empty or use defaults

## Backwards Compatibility

✅ This fix is fully backwards compatible. Existing configurations using JSON array format will continue to work without any changes.
