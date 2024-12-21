import socket
import json

from agent.model import ChatGPTAPI
from agent.rag import retrieve_related_chunks


def start_server():
    host = '127.0.0.1'
    port = 65434

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Сервер запущен на {host}:{port} и ожидает подключения...")
    conn, address = server_socket.accept()
    print(f"Клиент подключился с адреса: {address}")

    model = ChatGPTAPI()

    while True:
        data = ""
        while True:
            data += conn.recv(1024).decode('utf-8')
            try:
                map_info = json.loads(data)
                break
            except json.JSONDecodeError:
                pass

        print(f"Получен JSON от клиента: {map_info}")

        map_desc_help = retrieve_related_chunks(map_info['map']['description'])
        char_desc_help = []
        for character in map_info['characters']:
            char_desc_help.append(retrieve_related_chunks(character['description']))
        print(map_desc_help)

        help = ''
        for res in map_desc_help['chunks']:
            help += res['description']
        for char in char_desc_help:
            for res in char['chunks']:
                help += res['description']

        print('Дополнительная информация:\n', help)

        query = str(map_info) + "\n\n" + "Дополнительная информация:" + help
        res = model.call_api(query)

        print('Ответ модели:\n', res)

        # Ответ клиенту
        response = {"message": str(res), "status": 200}
        conn.send(json.dumps(response).encode('utf-8'))
        break

    conn.close()

if __name__ == "__main__":
    start_server()