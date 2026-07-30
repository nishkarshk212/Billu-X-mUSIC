import os
import asyncio
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

async def generate():
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║   Pyrogram Session String Generator              ║")
    print("║   Get API credentials: https://my.telegram.org   ║")
    print("╚══════════════════════════════════════════════════╝")
    print()

    api_id_env = os.getenv("API_ID")
    api_hash_env = os.getenv("API_HASH")

    if api_id_env and api_hash_env:
        api_id = int(api_id_env)
        api_hash = api_hash_env
        print(f"  Auto-loaded credentials from .env:")
        print(f"  API_ID   : {api_id}")
        print(f"  API_HASH : {api_hash}")
    else:
        api_id   = int(input("  API_ID   : ").strip())
        api_hash = input("  API_HASH : ").strip()


    print()
    print("  Starting Telegram client — you will receive an OTP...")
    print()

    # Prevent Pyrogram from auto-loading dead session string from env
    for key in ["SESSION", "SESSION1", "SESSION2", "SESSION3"]:
        if key in os.environ:
            del os.environ[key]

    async with Client(name="session_generator", in_memory=True, api_id=api_id, api_hash=api_hash) as app:
        session = await app.export_session_string()

        print()
        print("╔══════════════════════════════════════════════════╗")
        print("║  ✅  SESSION STRING GENERATED                    ║")
        print("╚══════════════════════════════════════════════════╝")
        print()
        print(session)
        print()
        print("  ↑ Copy the string above and paste it as SESSION= in your .env")
        print()

        # Also save to a file for convenience
        with open("generated_session.txt", "w") as f:
            f.write(f"SESSION={session}\n")
        print("  📄 Also saved to: generated_session.txt")
        print()


asyncio.run(generate())
