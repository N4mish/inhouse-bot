def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == 'hello':
        return 'hey!'


    if p_message == 'help':
        return 'i helped'