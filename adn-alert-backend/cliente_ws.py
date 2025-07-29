import asyncio
import websockets

async def conectar(n):
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print(f"🟢 Cliente {n} conectado")
        await asyncio.sleep(10)  # Mantenerlo conectado un rato

async def main():
    await asyncio.gather(*(conectar(i) for i in range(1, 6)))

asyncio.run(main())
