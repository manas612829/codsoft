# Simple Chatbot in Python

def chatbot():
    print("Chatbot: Hi! I'm a simple chatbot. Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ").lower()
        
        if user_input == "hi" or user_input == "hello":
            print("Chatbot: Hello! How are you?")
        
        elif "how are you" in user_input:
            print("Chatbot: I'm just a bot, but I'm doing fine. Thanks for asking!")
        
        elif "your name" in user_input:
            print("Chatbot: I'm a simple chatbot written in Python.")
        
        elif "bye" in user_input:
            print("Chatbot: Goodbye! Have a great day.")
            break
        
        else:
            print("Chatbot: Sorry, I didn't understand that.")

# Run the chatbot
chatbot()
