# Python Generators 0x00 - Seed Database

This project sets up a MySQL database called `ALX_prodev` with a `user_data` table using Python.

## Features

- Connects to MySQL
- Creates a database and table if not existing
- Reads from a `user_data.csv` file
- Inserts user records into the table

## Table Schema

- `user_id`: UUID, Primary Key
- `name`: VARCHAR, NOT NULL
- `email`: VARCHAR, NOT NULL
- `age`: DECIMAL, NOT NULL

## Files

- `seed.py`: Handles DB connection, creation, and data seeding
- `0-main.py`: Entry point to test the setup
- `user_data.csv`: Contains sample data to seed the DB

## How to Run

1. Make sure MySQL server is running
2. Set your MySQL `root` password in `seed.py`
3. Run:

```bash
chmod +x 0-main.py
./0-main.py
