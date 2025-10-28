#!/usr/bin/env python3
"""
UE5 Telegram Update Monitor
Monitors Telegram channels for Unreal Engine plugin version updates
"""

import os
import re
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Set
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import Message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UE5UpdateMonitor:
    """Monitor Telegram channels for Unreal Engine plugin updates"""
    
    # Pattern to match Unreal Engine plugin version updates
    # Matches patterns like "UE5.4", "UE 5.3", "Unreal Engine 5.2", "v5.1", etc.
    VERSION_PATTERN = re.compile(
        r'(?:UE|Unreal\s+Engine|Version|v)?\s*'
        r'(\d+\.\d+(?:\.\d+)?)',
        re.IGNORECASE
    )
    
    # Keywords that indicate a plugin update
    UPDATE_KEYWORDS = [
        'update', 'updated', 'new version', 'release', 'released',
        'download', 'available', 'plugin', 'marketplace'
    ]
    
    def __init__(
        self,
        api_id: int,
        api_hash: str,
        phone: str,
        channel: str,
        check_interval: int = 300,
        download_dir: Optional[str] = None
    ):
        """
        Initialize the monitor
        
        Args:
            api_id: Telegram API ID
            api_hash: Telegram API hash
            phone: Phone number for authentication
            channel: Channel username or ID to monitor
            check_interval: Check interval in seconds
            download_dir: Directory for automatic downloads (optional)
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.channel = channel
        self.check_interval = check_interval
        self.download_dir = Path(download_dir) if download_dir else None
        self.client: Optional[TelegramClient] = None
        self.seen_message_ids: Set[int] = set()
        self.last_check_time: Optional[datetime] = None
        
        # Create download directory if specified
        if self.download_dir:
            self.download_dir.mkdir(parents=True, exist_ok=True)
    
    async def start(self):
        """Start the monitoring client"""
        logger.info("Starting UE5 Update Monitor")
        
        # Create Telegram client
        self.client = TelegramClient('ue5_monitor_session', self.api_id, self.api_hash)
        
        # Connect and authenticate
        await self.client.start(phone=self.phone)
        logger.info("Connected to Telegram")
        
        # Register event handler for new messages
        @self.client.on(events.NewMessage(chats=self.channel))
        async def handle_new_message(event):
            await self.process_message(event.message)
        
        logger.info(f"Monitoring channel: {self.channel}")
        logger.info(f"Check interval: {self.check_interval} seconds")
        
        # Start periodic checking for historical messages
        asyncio.create_task(self.periodic_check())
        
        # Keep the client running
        await self.client.run_until_disconnected()
    
    async def periodic_check(self):
        """Periodically check for new messages"""
        while True:
            try:
                await asyncio.sleep(self.check_interval)
                await self.check_recent_messages()
            except Exception as e:
                logger.error(f"Error in periodic check: {e}", exc_info=True)
    
    async def check_recent_messages(self):
        """Check recent messages in the channel"""
        try:
            logger.info("Checking for recent messages...")
            
            # Get recent messages
            async for message in self.client.iter_messages(self.channel, limit=20):
                if message.id not in self.seen_message_ids:
                    await self.process_message(message)
                    self.seen_message_ids.add(message.id)
            
            self.last_check_time = datetime.now()
            logger.info(f"Check completed at {self.last_check_time}")
            
        except Exception as e:
            logger.error(f"Error checking messages: {e}", exc_info=True)
    
    async def process_message(self, message: Message):
        """
        Process a message to check if it matches UE plugin update pattern
        
        Args:
            message: Telegram message to process
        """
        if not message.text:
            return
        
        # Check if message matches update pattern
        if self.is_update_message(message.text):
            logger.info(f"Found matching update message (ID: {message.id})")
            await self.notify_update(message)
            
            # Download if enabled
            if self.download_dir and message.media:
                await self.download_media(message)
    
    def is_update_message(self, text: str) -> bool:
        """
        Check if message text matches UE plugin update pattern
        
        Args:
            text: Message text to check
            
        Returns:
            True if message matches update pattern
        """
        text_lower = text.lower()
        
        # Check for version number
        has_version = bool(self.VERSION_PATTERN.search(text))
        
        # Check for update keywords
        has_keywords = any(keyword in text_lower for keyword in self.UPDATE_KEYWORDS)
        
        # Check for UE/Unreal Engine mention (including UE5.x format)
        has_ue_mention = bool(re.search(r'\b(?:UE\s*\d*|Unreal\s+Engine)\b', text, re.IGNORECASE))
        
        # Match if: (has version AND UE mention) OR (has version AND UE mention AND keywords)
        # This ensures we only match Unreal Engine related updates
        return has_version and has_ue_mention
    
    async def notify_update(self, message: Message):
        """
        Notify user about an update
        
        Args:
            message: Message containing the update
        """
        # Extract version info
        version_match = self.VERSION_PATTERN.search(message.text)
        version = version_match.group(1) if version_match else "Unknown"
        
        notification = f"""
╔════════════════════════════════════════╗
║   UE PLUGIN UPDATE DETECTED!           ║
╚════════════════════════════════════════╝

Version: {version}
Date: {message.date}
Channel: {self.channel}
Message ID: {message.id}

Message Preview:
{message.text[:200]}...

"""
        print(notification)
        logger.info(f"Update notification sent for version {version}")
    
    async def download_media(self, message: Message):
        """
        Download media from a message
        
        Args:
            message: Message containing media to download
        """
        try:
            logger.info(f"Downloading media from message {message.id}")
            
            # Create filename with timestamp and message ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ue_update_{timestamp}_msg{message.id}"
            
            # Download the media
            file_path = await self.client.download_media(
                message,
                file=str(self.download_dir / filename)
            )
            
            if file_path:
                logger.info(f"Downloaded media to: {file_path}")
                print(f"✓ Downloaded: {file_path}")
            else:
                logger.warning(f"No media downloaded for message {message.id}")
                
        except Exception as e:
            logger.error(f"Error downloading media: {e}", exc_info=True)
    
    async def stop(self):
        """Stop the monitor and disconnect"""
        if self.client:
            await self.client.disconnect()
            logger.info("Monitor stopped")


async def main():
    """Main entry point"""
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    channel = os.getenv('TELEGRAM_CHANNEL')
    check_interval = int(os.getenv('CHECK_INTERVAL', '300'))
    download_dir = os.getenv('DOWNLOAD_DIR')
    
    # Validate required configuration
    if not all([api_id, api_hash, phone, channel]):
        logger.error("Missing required environment variables!")
        logger.error("Please set: TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_CHANNEL")
        logger.error("See .env.example for reference")
        return
    
    try:
        # Create and start monitor
        monitor = UE5UpdateMonitor(
            api_id=int(api_id),
            api_hash=api_hash,
            phone=phone,
            channel=channel,
            check_interval=check_interval,
            download_dir=download_dir
        )
        
        await monitor.start()
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
