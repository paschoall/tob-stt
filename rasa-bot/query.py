import time
from pymongo import MongoClient

#                          (ano,mes,dia,hora,min,s,dia da semana, dia do ano, horario de verao)
START_TIME = time.mktime((2020, 10, 5, 17, 30, 0, 0, 279, 0))
END_TIME = time.mktime((2020, 10, 5, 18, 40, 0, 0, 279, 0))

FILE_NAME = 'experiment_log.txt'


def get_experiment_questions():
    write_list = []

    cursor = collection.find({}, {'sender_id': 1, '_id': 0})
    uids = [sid['sender_id'] for sid in cursor]

    for user in uids:
        write_list.append(f'\n----------User: {user}-----------\n')
        user_dict = collection.find_one({"sender_id": user})
        events = user_dict['events']
        for e in events:
            if START_TIME <= e['timestamp'] < END_TIME:
                if e['event'] == 'user':
                    write_list.append('---------------------------------\n')
                    tempo = time.localtime(e['timestamp'])
                    write_list.append(f"[timestamp] "
                                      f"{tempo.tm_hour}:"
                                      f"{str(tempo.tm_min).zfill(2)}:"
                                      f"{str(tempo.tm_sec).zfill(2)}\n")
                    write_list.append('[User] ' + e['text'] + '\n')
                if e['event'] == 'bot':
                    write_list.append('[Bot] ' + e['text'] + '\n')

    with open(FILE_NAME, 'w') as fp:
        for line in write_list:
            fp.write(line)


def get_single_chat():
    users_cursor = collection.find({}, {'sender_id': 1, '_id': 0})
    print('Users ids:')
    for i in users_cursor:
        print('\t' + i['sender_id'])

    user = input('Please select an user: ').strip('\n')
    user_dict = collection.find_one({"sender_id": user})
    events = user_dict['events']
    for e in events:
        if e['event'] == 'user':
            print('------------------')
            print(f"Time: {time.localtime(e['timestamp'])}")
            print('User: ' + e['text'])
        if e['event'] == 'bot':
            print('Bot: ' + e['text'])


if __name__ == '__main__':
    client = MongoClient()
    db = client.rasa
    collection = db.conversations
    get_single_chat()

