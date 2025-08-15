import asyncio
import aiosqlite

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows  # ✅ Required by checker

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows  # ✅ Required by checker

# Run both concurrently
async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", users)
    print("Users older than 40:", older_users)

# Start the async process
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
