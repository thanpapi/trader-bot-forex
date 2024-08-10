from telegram import Bot
import asyncio

async def get_chat_id(bot_token):
    bot = Bot(token=bot_token)
    try:
        # Obtén las actualizaciones
        updates = await bot.get_updates()
        if updates:
            # Extrae el chat_id del primer mensaje en las actualizaciones
            chat_id = updates[-1].message.chat.id
            print(f"-1002165469196: {chat_id}")
            return chat_id
        else:
            print("No hay actualizaciones disponibles.")
            return None
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bot_token = "7430415385:AAGXJRFEJtbqdGdTEsayKB5tmN16wXOLeYU"  # Reemplaza con el token de tu bot

    asyncio.run(get_chat_id(bot_token))
