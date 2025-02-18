from model import ChatGPTAPI
from rag import retrieve_related_chunks


def process_map(map_info):
    model = ChatGPTAPI()
    map_desc_help = retrieve_related_chunks(map_info['map']['desc']['desc'])
    char_desc_help = []
    for character in map_info['chars']:
        char_desc_help.append(retrieve_related_chunks(character['desc']))

    help = ''
    for res in map_desc_help['chunks']:
        help += res['description']
    for char in char_desc_help:
        for res in char['chunks']:
            help += res['description']

    # map_info['map'].pop('tiles')
    # print('Дополнительная информация:\n', help)

    query = str(map_info).replace('\n', '') + "\n\n" + "Дополнительная информация:" + help

    print(query)
    action = model.generate_action(query)
    print(action)
    new_map_info = model.update_map(map_info, action)
    print(new_map_info)
    return {"message": action, "data": new_map_info}
