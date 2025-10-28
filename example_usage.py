#!/usr/bin/env python3
"""
Example usage of UE5 Update Monitor

This script demonstrates how to use the UE5UpdateMonitor class
with custom configuration.
"""

import asyncio
from ue5_monitor import UE5UpdateMonitor


async def main():
    """Example usage"""
    
    # Example configuration
    # In production, use environment variables instead
    monitor = UE5UpdateMonitor(
        api_id=12345,  # Replace with your API ID
        api_hash="your_api_hash_here",  # Replace with your API hash
        phone="+1234567890",  # Replace with your phone number
        channel="unrealengine",  # Replace with channel to monitor
        check_interval=300,  # Check every 5 minutes
        download_dir="./downloads"  # Optional: directory for downloads
    )
    
    try:
        print("Starting UE5 Update Monitor...")
        print("Press Ctrl+C to stop")
        await monitor.start()
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        await monitor.stop()


if __name__ == "__main__":
    asyncio.run(main())
