# UE5 Telegram Update Monitor - Usage Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run the monitor:**
   ```bash
   python ue5_monitor.py
   ```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_PHONE=+1234567890
TELEGRAM_CHANNEL=unrealengine
CHECK_INTERVAL=300
DOWNLOAD_DIR=./downloads
```

### Configuration Details

- **TELEGRAM_API_ID**: Numeric API ID from https://my.telegram.org/apps
- **TELEGRAM_API_HASH**: String API hash from https://my.telegram.org/apps
- **TELEGRAM_PHONE**: Your phone number with country code (e.g., +1234567890)
- **TELEGRAM_CHANNEL**: Channel username (without @) or numeric channel ID
- **CHECK_INTERVAL**: How often to check for new messages (in seconds)
- **DOWNLOAD_DIR**: Where to save downloaded files (optional)

## How It Works

### Pattern Matching

The monitor detects Unreal Engine plugin updates by looking for messages that contain:

1. **Version numbers**: Patterns like:
   - `UE 5.4`
   - `UE5.3`
   - `Unreal Engine 5.2`
   - `Version 5.1`
   - `v5.0`

2. **UE/Unreal Engine mentions**: The text must reference:
   - `UE` or `UE5`, `UE4`, etc.
   - `Unreal Engine`

### Example Matching Messages

✅ **Will Match:**
- "New UE 5.4 plugin update available!"
- "Updated to Unreal Engine 5.3"
- "Plugin released for UE5.2"
- "Download UE5.4 now!"
- "Unreal Engine 4.27 update"

❌ **Will NOT Match:**
- "Version 1.0 now available" (no UE mention)
- "UE marketplace" (no version number)
- "Random text about updates" (no UE or version)

## Features

### Real-time Monitoring

The monitor runs continuously and:
- Listens for new messages in real-time
- Checks recent messages periodically
- Notifies you when updates are found

### Automatic Downloads

If `DOWNLOAD_DIR` is set, the monitor will automatically download:
- Files attached to update messages
- Media content from matching posts
- Files are named with timestamp and message ID

### Notifications

When an update is detected, you'll see:
```
╔════════════════════════════════════════╗
║   UE PLUGIN UPDATE DETECTED!           ║
╚════════════════════════════════════════╝

Version: 5.4
Date: 2025-10-28 12:34:56
Channel: unrealengine
Message ID: 12345

Message Preview:
New UE 5.4 plugin update available...
```

## Advanced Usage

### Programmatic Usage

```python
import asyncio
from ue5_monitor import UE5UpdateMonitor

async def main():
    monitor = UE5UpdateMonitor(
        api_id=12345,
        api_hash="your_hash",
        phone="+1234567890",
        channel="unrealengine",
        check_interval=300,
        download_dir="./downloads"
    )
    
    await monitor.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Pattern Matching

To modify what messages are detected, edit the `is_update_message` method in `ue5_monitor.py`.

Current logic:
- Message must contain a version number
- Message must mention UE/Unreal Engine

## Troubleshooting

### Authentication Issues

**Problem**: Can't connect to Telegram

**Solutions**:
- Ensure API credentials are correct
- Check phone number includes country code
- Verify internet connection
- Try removing session file: `rm ue5_monitor_session.session`

### No Messages Detected

**Problem**: Monitor runs but doesn't detect updates

**Solutions**:
- Verify you're a member of the channel
- Check channel username is correct (no @ symbol)
- Test pattern matching with: `python test_patterns.py`
- Review logs for error messages

### Download Failures

**Problem**: Files aren't downloading

**Solutions**:
- Check `DOWNLOAD_DIR` exists and is writable
- Verify messages have media attachments
- Review logs for download errors

### Rate Limiting

**Problem**: Telegram API rate limits

**Solutions**:
- Increase `CHECK_INTERVAL` (default: 300 seconds)
- Reduce number of messages checked (modify `limit=20` in code)
- Wait before retrying

## Best Practices

1. **Start with testing**: Use `test_patterns.py` to verify pattern matching
2. **Monitor low-volume channels first**: Start with channels that post infrequently
3. **Use appropriate intervals**: Don't check too frequently (300 seconds is reasonable)
4. **Keep credentials secure**: Never commit `.env` file to version control
5. **Monitor logs**: Check console output for errors and matches

## Security

- Store API credentials in `.env` file (never in code)
- The `.env` file is in `.gitignore` and won't be committed
- Session files contain authentication tokens - keep them secure
- Don't share your API credentials or session files

## Examples

### Monitor Multiple Channels

Run multiple instances with different configurations:

```bash
# Terminal 1
TELEGRAM_CHANNEL=channel1 python ue5_monitor.py

# Terminal 2
TELEGRAM_CHANNEL=channel2 python ue5_monitor.py
```

### Test Pattern Matching

Before running the monitor, test your patterns:

```bash
python test_patterns.py
```

### Check Without Downloads

To monitor without downloading files, remove `DOWNLOAD_DIR` from `.env`:

```bash
# .env
TELEGRAM_API_ID=12345
TELEGRAM_API_HASH=abcdef
TELEGRAM_PHONE=+1234567890
TELEGRAM_CHANNEL=unrealengine
CHECK_INTERVAL=300
# DOWNLOAD_DIR not set - no downloads
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs for error messages
3. Test with `test_patterns.py`
4. Check Telethon documentation: https://docs.telethon.dev/
