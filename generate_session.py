import asyncio
import os
import glob
import re
from pyrogram import Client

DEFAULT_API_ID = 30201492
DEFAULT_API_HASH = "6bf0844e2bd6dc434fa19c641deeaf84"


def cleanup_stale_files():
    """Remove any old session sqlite files to guarantee a fresh login."""
    for f in glob.glob("*.session*") + [":memory:.session", "generated_session.txt"]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except OSError:
            pass


async def generate():
    cleanup_stale_files()

    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║   Pyrogram Session String Generator              ║")
    print("║   Billu Music Bot Session Generator              ║")
    print("╚══════════════════════════════════════════════════╝")
    print()

    inp_id = input(f"  API_ID   [{DEFAULT_API_ID}]: ").strip()
    api_id = int(inp_id) if inp_id else DEFAULT_API_ID

    inp_hash = input(f"  API_HASH [{DEFAULT_API_HASH}]: ").strip()
    api_hash = inp_hash if inp_hash else DEFAULT_API_HASH

    print()
    print("  Starting Telegram client — enter your phone number with country code...")
    print()

    async with Client(name="billu_session", api_id=api_id, api_hash=api_hash, in_memory=True) as app:
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

        # Update .env file automatically if present
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                env_content = f.read()
            if re.search(r"^SESSION=.*$", env_content, flags=re.MULTILINE):
                env_content = re.sub(r"^SESSION=.*$", f"SESSION={session}", env_content, flags=re.MULTILINE)
            else:
                env_content += f"\nSESSION={session}\n"
            with open(".env", "w") as f:
                f.write(env_content)
            print("  ✅ Automatically saved SESSION into .env")

        with open("generated_session.txt", "w") as f:
            f.write(f"SESSION={session}\n")
        print("  📄 Also saved to: generated_session.txt")
        print()

    cleanup_stale_files()
    # Re-save generated_session.txt
    with open("generated_session.txt", "w") as f:
        f.write(f"SESSION={session}\n")


if __name__ == "__main__":
    asyncio.run(generate())
