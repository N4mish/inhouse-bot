# isolated file to hold all possible responses
scheduled = False # future - make this database

def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == 'hello':
        return 'hey!'


    if p_message == 'help':
        return 'i helped'
    
    if p_message == 'schedule':
        scheduled = True
        return 'sched successful'

    