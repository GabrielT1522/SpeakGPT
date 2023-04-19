#   Functions for formatting and storing chat history in list.

def add_question_to_history(message_history_list, question):
    message = {"author": "You", "text": question}
    message_history_list.append(message)   
    pass


def add_answer_to_history(message_history_list, answer):
    #   Goes in get_response() function: then placed in answer param.
    #response = generate_response(previous_messages, question)
    message = {"author": "AI", "text": response}
    message_history_list.append(message)
    pass

