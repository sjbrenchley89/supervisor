# Home Assistant Hub Connection - Integration Guide

This guide covers the Home Assistant Hub connection setup across all 5 repositories in the `claude/home-assistant-hub-connect-8aeedl` branch.

## Overview

All repositories are configured to connect to your Home Assistant Hub at:
- **URL**: `http://192.168.1.121:8123`
- **Purpose**: Integration testing, development, and configuration management

## Repository Setup Status

| Repository | Setup Status | Configuration |
|-----------|--------------|-----------------|
| `supervisor` | ✅ Complete | Python module + tests |
| `home-assistant-configuration` | ✅ Complete | YAML configuration |
| `home-assistant.io` | ✅ Complete | Documentation integration |
| `sb_home_assistant_2026` | ✅ Complete | Development environment |
| `-claude-code` | ✅ Complete | Code base setup |

## Files Added/Modified

### All Repositories
- `.env.example` - Environment variable template (use as reference)
- `HA_HUB_SETUP.md` - Repository-specific setup guide
- `.gitignore` - Updated to ignore `.env` file

### Supervisor Repository (Python-specific)
- `supervisor/ha_hub_connection.py` - Python configuration module
- `.github/workflows/ha-hub-integration-test.yml` - CI/CD workflow
- `HA_HUB_INTEGRATION_GUIDE.md` - This guide

## Setup Checklist

### Step 1: Local Environment Setup (All Repositories)

```bash
# For each repository
cd /home/user/<repository-name>
cp .env.example .env
# Edit .env with your credentials
```

### Step 2: Add Credentials

Edit each `.env` file with:
```env
HA_HUB_URL=http://192.168.1.121:8123
HA_HUB_TOKEN=<your_token_here>
```

### Step 3: Verify Setup

```bash
# Check .env is in gitignore
cat .gitignore | grep "^\.env"

# Verify .env is not tracked
git status
# Should NOT show .env
```

### Step 4: GitHub Secrets Setup (Optional - for CI/CD)

1. Navigate to each repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Create two secrets:
   - `HA_HUB_URL`: `http://192.168.1.121:8123`
   - `HA_HUB_TOKEN`: Your long-lived access token

## Usage Examples

### Python (Supervisor)

```python
from supervisor.ha_hub_connection import ha_hub_config

# Check configuration
if ha_hub_config.is_configured:
    print(f"Connected to: {ha_hub_config.url}")
    
# Test connection
import asyncio
is_connected = asyncio.run(ha_hub_config.test_connection())
```

### Bash (Any Repository)

```bash
# Access via environment variables
curl -H "Authorization: Bearer $HA_HUB_TOKEN" \
  "$HA_HUB_URL/api/states"
```

### YAML (Configuration)

```yaml
# In automation or script configurations
service: homeassistant.update_entity
data:
  entity_id: sensor.my_sensor
```

## Integration Testing

### Test Structure

```
tests/
├── integration/
│   └── test_ha_hub_connection.py
└── fixtures/
    └── ha_hub.py
```

### Example Test

```python
@pytest.mark.integration
@pytest.mark.skipif(
    not ha_hub_config.is_configured, 
    reason="HA Hub not configured"
)
async def test_hub_connection():
    """Test connection to Home Assistant Hub."""
    assert await ha_hub_config.test_connection()
```

## Security Best Practices

1. **Never commit `.env`** - Always use `.env.example` as template
2. **Rotate tokens** - Delete old tokens from Home Assistant regularly
3. **Use different tokens** for:
   - Local development
   - CI/CD testing
   - Production deployments
4. **Monitor token usage** - Check Home Assistant logs for unusual activity
5. **Revoke immediately** - If a token is compromised

## Troubleshooting

### Connection Fails

**Symptom**: `Connection refused` or `Network unreachable`

**Solutions**:
1. Verify Home Assistant is running: Visit URL in browser
2. Check firewall allows port 8123
3. Verify IP address is correct: `ping 192.168.1.121`
4. Check network connectivity

### Token Errors

**Symptom**: `401 Unauthorized` or `Invalid token`

**Solutions**:
1. Verify token hasn't expired (1 year default)
2. Generate new token from Home Assistant
3. Ensure token is correctly copied (no extra spaces)
4. Check token wasn't deleted from Home Assistant

### Missing Environment Variables

**Symptom**: `HA_HUB_URL not configured` error

**Solutions**:
1. Ensure `.env` file exists: `ls -la .env`
2. Ensure `.env` has correct format
3. Reload environment: `source .env` or restart shell
4. For CI/CD: Verify GitHub secrets are configured

## Environment Variable Details

### HA_HUB_URL

- **Type**: URL string
- **Format**: `http://ip:port` or `https://domain`
- **Example**: `http://192.168.1.121:8123`
- **Required**: Yes

### HA_HUB_TOKEN

- **Type**: JWT token string
- **Generated**: In Home Assistant user profile
- **Valid for**: 1 year (default)
- **Required**: Yes

## CI/CD Integration

### GitHub Actions

The workflow file at `.github/workflows/ha-hub-integration-test.yml` will:

1. Run on branch pushes
2. Check HA Hub secrets are configured
3. Test connection to Home Assistant
4. Run integration tests
5. Scan for hardcoded secrets

**To enable**:
1. Add GitHub secrets to repository
2. Push changes to the branch
3. Workflow runs automatically

### Running Locally

```bash
# Run like GitHub Actions would
export HA_HUB_URL="http://192.168.1.121:8123"
export HA_HUB_TOKEN="your_token"

# Run tests
pytest tests/integration/ -v

# Run linting
ruff check .
```

## Next Steps

1. ✅ Copy `.env.example` to `.env` in each repository
2. ✅ Add your credentials to `.env`
3. ✅ Verify `.env` is not tracked: `git status`
4. ✅ Test connection: See HA_HUB_SETUP.md in each repository
5. ✅ (Optional) Add GitHub secrets for CI/CD
6. ✅ Run tests: `pytest tests/integration/ -v`

## Support & Questions

For issues or questions about Home Assistant Hub connection:

1. Check `HA_HUB_SETUP.md` in your repository
2. Review Home Assistant logs: `http://192.168.1.121:8123/config/logs`
3. Check GitHub Actions workflow output
4. Review `supervisor/ha_hub_connection.py` for Python usage

## Related Documentation

- [Home Assistant API Docs](https://developers.home-assistant.io/docs/api/rest)
- [Authentication Guide](https://developers.home-assistant.io/docs/auth_api)
- [Long-lived Tokens](https://developers.home-assistant.io/docs/auth_api#long-lived-access-token)
- [WebSocket Connection](https://developers.home-assistant.io/docs/api/websocket)

---

**Branch**: `claude/home-assistant-hub-connect-8aeedl`  
**Setup Date**: 2026-09-04  
**Connection Status**: Ready for configuration
