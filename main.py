# 1. Agent starts with a greeting that includes the user's name(s).
# 2. User queries agent about a particular issue contained in the data.
# 3. Agent responds to the query, citing references from the data.

user_name = "John Doe"

def chat_agent(name):
    print(f"Hello {name}, what do you need help with today?")

    user_prompt = input()

    if bool(user_prompt) is False:
        return "Kindly input your query..."
    else:
        return {
            "query": user_prompt,
            "response": "The statute in question states that..."
        }

response = chat_agent(user_name)

print(response)
