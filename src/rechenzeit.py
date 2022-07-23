from uqo.client.connection import Connection
from uqo.client.config import Config

config = Config(configpath=r"C:\Users\SofieLouise\PycharmProjects\quantum\config.json")
connection = config.create_connection()

print(connection.show_quota())