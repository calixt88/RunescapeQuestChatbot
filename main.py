import pandas as pd
import pickle

# Load the trained model and vectorizer
with open('ModelTraining/model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('ModelTraining/vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

df = pd.read_csv("ModelTraining/cleaned_quests_data.csv")

quest_names = df['quest_name'].dropna().unique().tolist()

def extract_quest_name(user_input):
    user_input_lower = user_input.lower()
    for quest in quest_names:
        if quest.lower() in user_input_lower:
            return quest
    return None

def fetch_quest_data(df, quest_name):
    quest_info = df[df['quest_name'].str.contains(quest_name, case=False, na=False)]
    return quest_info

def predict_intent(user_input):
    user_input_transformed = vectorizer.transform([user_input])
    intent = model.predict(user_input_transformed)[0]
    return intent

def generate_response(intent, user_input):
    quest_name = extract_quest_name(user_input)
    if quest_name:
        quest_data = fetch_quest_data(df, quest_name)
        if not quest_data.empty:
            intent_responses = {
                'query_enemies': "The enemies you will need to defeat for " + quest_data['quest_name'].iloc[0] + ": " + quest_data['quest_enemies'].iloc[0],
                'query_items': "The items that you will need for " + quest_data['quest_name'].iloc[0] + ": "  + quest_data['quest_items'].iloc[0],
                'query_requirements': "The requirements for " + quest_data['quest_requirements'].iloc[0],
                'query_rewards': "The rewards for the quest" + quest_data['quest_name'].iloc[0] + ": " + quest_data['quest_rewards'].iloc[0],
                'query_released': "The quest " + quest_data['quest_name'].iloc[0] + " release date: " + quest_data['release_date'].iloc[0],
                'query_members': "Does the quest " + quest_data['quest_name'].iloc[0] + " need a membership: " + quest_data['members_requirement'].iloc[0],
                'query_steps': quest_data['quest_steps'].iloc[0],
            }
            return intent_responses.get(intent, "I found the quest but couldn't retrieve details for that specific query.")
    return "I couldn't find that quest. Please try a different query or check the quest name."

def main():
    greeting = "Hello! Feel free to ask about quest information in runescape."
    print("Welcome to the RQC Chatbot!")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'hello':
            print("RQC:", greeting)
        else:
            intent = predict_intent(user_input)
            response = generate_response(intent, user_input)
            print("RQC:", response)

if __name__ == "__main__":
    main()
