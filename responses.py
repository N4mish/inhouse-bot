# isolated file to hold all possible responses
def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == 'hello':
        return 'hey!'
    elif p_message == 'help':
        return 'i helped'
    
    elif p_message == 'schedule':
        return 'sched successful'

    else:
        return None
