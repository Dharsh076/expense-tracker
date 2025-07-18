import os

class Config:
    SECRET_KEY = 'super-secret-key-change-this'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
