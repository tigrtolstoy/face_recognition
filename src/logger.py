import logging


file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')


# Логгер для клиента
client_logger = logging.getLogger('client_logger')
client_logger.setLevel(logging.INFO)

cl_file_handler = logging.FileHandler('client.log')
cl_stream_handler = logging.StreamHandler()

cl_file_handler.setFormatter(file_format)
cl_stream_handler.setFormatter(stream_format)

client_logger.addHandler(cl_file_handler)
client_logger.addHandler(cl_stream_handler)


# Логгер для сервера
server_logger = logging.getLogger('server_logger')
server_logger.setLevel(logging.INFO)

serv_file_handler = logging.FileHandler('server.log')
serv_stream_handler = logging.StreamHandler()

serv_file_handler.setFormatter(file_format)
serv_stream_handler.setFormatter(stream_format)

server_logger.addHandler(serv_file_handler)
server_logger.addHandler(serv_stream_handler)
