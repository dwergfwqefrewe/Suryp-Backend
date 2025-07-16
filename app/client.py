import websockets
import asyncio
import json

BASE_URL = "ws://127.200.0.1:8000/ws"

async def main():
    url = input("Введите номер комнаты: ")
    token = input("Введите JWT токен: ")

    print(f"{BASE_URL}/{url}?token={token}")
    async with websockets.connect(f"{BASE_URL}/{url}?token={token}") as ws:
        print("Подключено! Для отправки сообщений введите текст.")
        async def receive():
            async for msg in ws:
                print(f"\n[Сервер]: {msg}")

        asyncio.create_task(receive())

        while True:
            try:
                text = input("Текст: ")
                await ws.send(json.dumps({"text": text}))
            except KeyboardInterrupt:
                break

asyncio.run(main())
