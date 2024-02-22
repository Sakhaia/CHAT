import asyncio
import websockets
import json
from db import Database

class ChatServer:
    def __init__(self):
        self.clients = set()
        self.db = Database()

    async def register(self, websocket):
        self.clients.add(websocket)

    async def unregister(self, websocket):
        self.clients.remove(websocket)

    async def send_to_clients(self, message):
        if self.clients:
            # Логирование сообщения
            data = json.loads(message)
            if data.get("action") == "message":
                print(f"Message from {data.get('user', 'Unknown')}: {data.get('message', '')}")

            await asyncio.wait([asyncio.create_task(client.send(message)) for client in self.clients])

    async def handle_message(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "message":
                    await self.send_to_clients(message)
                elif data["action"] == "register":
                    if self.db.user_exists(data["user"]["username"]):
                        await websocket.send(json.dumps({"action": "register", "success": False, "error": "Username already exists"}))
                        print(f"Registration failed: Username {data['user']['username']} already exists")
                    else:
                        self.db.register_user(data["user"])
                        await websocket.send(json.dumps({"action": "register", "success": True}))
                        print(f"User registered: {data['user']['username']}")
                elif data["action"] == "login":
                    success = self.db.login_user(data["user"]["username"], data["user"]["password"])
                    await websocket.send(json.dumps({"action": "login", "success": success}))
                    if success:
                        print(f"User logged in: {data['user']['username']}")
                    else:
                        print(f"Login failed for user: {data['user']['username']}")
        finally:
            await self.unregister(websocket)

async def main():
    chat_server = ChatServer()
    start_server = await websockets.serve(chat_server.handle_message, "0.0.0.0", 8080)

    async with start_server:
        print("Server started. Listening for incoming connections...")
        await asyncio.gather(start_server.wait_closed())

if __name__ == "__main__":
    asyncio.run(main())