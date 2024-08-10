from telegram import Bot
import asyncio

async def test_bot_token(bot_token):
    bot = Bot(token=bot_token)
    try:
        # Intenta obtener información del bot
        me = await bot.get_me()
        print(f"Bot info: {me}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bot_token = "7430415385:AAGXJRFEJtbqdGdTEsayKB5tmN16wXOLeYU"  # Reemplaza con el nuevo token

    asyncio.run(test_bot_token(bot_token))
