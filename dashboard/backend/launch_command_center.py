import asyncio
from telegram_command_center import BrotherhoodCommandCenter

async def main():
    command_center = BrotherhoodCommandCenter()
    await command_center.run_bot()

if __name__ == "__main__":
    asyncio.run(main())
