# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

# Owner-only command to toggle play/error logging to the LOGGER_ID group.


from pyrogram import filters, types

from ishu import app, db, lang


@app.on_message(filters.command(["logger", "loggroup"]) & filters.user(app.owner))
@lang.language()
async def _logger_toggle(_, m: types.Message):
    args = m.command[1:] if len(m.command) > 1 else []
    arg = args[0].lower() if args else None

    if arg in ("on", "enable", "true", "1"):
        await db.set_logger(True)
        return await m.reply_text(
            f"✅ Play & error logging is now <b>ENABLED</b> → <code>{app.logger}</code>"
        )

    if arg in ("off", "disable", "false", "0"):
        await db.set_logger(False)
        return await m.reply_text(
            f"🔕 Play & error logging is now <b>DISABLED</b>."
        )

    status = "ENABLED ✅" if await db.is_logger() else "DISABLED 🔕"
    await m.reply_text(
        f"📝 Logging is currently <b>{status}</b>.\n"
        f"Log group: <code>{app.logger}</code>\n\n"
        f"Usage: <code>/logger on</code> or <code>/logger off</code>"
    )
