# Ue5TGUpdate

A Python script that monitors Telegram channels for Unreal Engine plugin version updates using the Telethon library. Automatically detects posts matching specific patterns and notifies users or triggers automatic downloads.

## Features

- 🔍 **Pattern Matching**: Automatically detects Unreal Engine version updates (e.g., UE5.4, UE 5.3, Unreal Engine 5.2)
- 📢 **Real-time Notifications**: Receives instant notifications for new matching posts
- ⏰ **Scheduled Checks**: Periodically checks for updates at configurable intervals
- 💾 **Automatic Downloads**: Optionally downloads media attachments from update posts
- 🔐 **Secure Configuration**: Uses environment variables for API credentials

## Prerequisites

- Python 3.7 or higher
- Telegram account
- Telegram API credentials (API ID and API Hash)

## Setup

### 1. Get Telegram API Credentials

1. Go to https://my.telegram.org/apps
2. Log in with your Telegram account
3. Create a new application
4. Note down your `api_id` and `api_hash`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and set your values:

```env
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_PHONE=your_phone_number_here
TELEGRAM_CHANNEL=target_channel_username
CHECK_INTERVAL=300
DOWNLOAD_DIR=./downloads
```

**Configuration Options:**

- `TELEGRAM_API_ID`: Your Telegram API ID from my.telegram.org
- `TELEGRAM_API_HASH`: Your Telegram API Hash from my.telegram.org
- `TELEGRAM_PHONE`: Your phone number (with country code, e.g., +1234567890)
- `TELEGRAM_CHANNEL`: Username or ID of the channel to monitor
- `CHECK_INTERVAL`: Check interval in seconds (default: 300 = 5 minutes)
- `DOWNLOAD_DIR`: Directory for automatic downloads (optional)

## Usage

Run the monitor:

```bash
python ue5_monitor.py
```

On first run, you'll need to authenticate with Telegram by entering the verification code sent to your phone.

The script will:
1. Connect to Telegram using your credentials
2. Monitor the specified channel for new posts
3. Check for posts matching Unreal Engine update patterns
4. Display notifications when updates are found
5. Optionally download media attachments

### Pattern Detection

The monitor looks for messages containing:

- **Version numbers**: UE5.4, UE 5.3, Unreal Engine 5.2, v5.1, etc.
- **Update keywords**: update, updated, new version, release, released, download, available, plugin, marketplace
- **UE mentions**: References to UE or Unreal Engine

### Example Output

```
╔════════════════════════════════════════╗
║   UE PLUGIN UPDATE DETECTED!           ║
╚════════════════════════════════════════╝

Version: 5.4
Date: 2025-10-28 12:34:56
Channel: unrealengine_updates
Message ID: 12345

Message Preview:
New UE 5.4 plugin update available! Download now from the marketplace...
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API credentials secure
- The `.env` file is already in `.gitignore`

## Troubleshooting

**Authentication Issues:**
- Ensure your phone number includes the country code (e.g., +1234567890)
- Make sure you have a stable internet connection
- Check that your API credentials are correct

**Channel Access:**
- Ensure you're a member of the channel you want to monitor
- Use the channel username (without @) or numeric channel ID
- Some channels may require special permissions

**No Updates Detected:**
- Verify the channel has posts matching the pattern
- Check the CHECK_INTERVAL is appropriate for the channel's posting frequency
- Review the logs for any error messages

## Development

The script uses:
- **Telethon**: Telegram client library
- **python-dotenv**: Environment variable management
- **asyncio**: Asynchronous event handling

## License

See LICENSE file for details.
