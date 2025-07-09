import asyncio
import aiosqlite

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        print("All users:", rows)
        await cursor.close()

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        print("Users older than 40:", rows)
        await cursor.close()

# Run both concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the main async function
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
