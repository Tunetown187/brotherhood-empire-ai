from conversation_logger import ConversationLogger

# Create a logger instance
logger = ConversationLogger()

# Example of logging messages
logger.save_message("user", "Hello, this is a test message")
logger.save_message("assistant", "Hi! I've received your message and logged it")

# Retrieve and print the conversation history
history = logger.get_session_history()
for message in history:
    print(f"{message['timestamp']} - {message['role']}: {message['content']}")
