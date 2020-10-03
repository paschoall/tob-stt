from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient()
    db = client.rasa
    collection = db.conversations

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
            print('User: ' + e['text'])
        if e['event'] == 'bot':
            print('Bot: ' + e['text'])
