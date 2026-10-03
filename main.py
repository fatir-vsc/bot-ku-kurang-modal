import sqlite3
import discord
from discord.ext import commands
from config import DATABASE
from logic import DB_Manager

if __name__ == "__main__":
    manager = DB_Manager(DATABASE)
    manager.create_tables()