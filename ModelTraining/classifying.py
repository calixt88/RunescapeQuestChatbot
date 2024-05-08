import pandas as pd

csv_file_path = '../quests_data.csv'

try:
    df = pd.read_csv(csv_file_path)
    print("File successfully loaded.")
except FileNotFoundError:
    print(f"Failed to load the file at: {csv_file_path}")

df.fillna('None', inplace=True)
df = df.applymap(lambda s: s.lower() if type(s) == str else s)

templates = {
    "query_enemies": [
        "Who are the enemies in {quest_name}?",
        "What foes must I defeat in {quest_name}?",
        "List all enemies encountered during {quest_name}.",
        "Who will I fight in {quest_name}?",
        "What enemies do i need to defeat for {quest_name}",
    ],
    "query_items": [
        "What items do I need for {quest_name}?",
        "List necessary equipment for {quest_name}.",
        "What must I bring to complete {quest_name}?",
        "What are the required items for {quest_name}?",
        "What do i need to bring with me for {quest_name}",
    ],
    "query_steps": [
        "How do I complete {quest_name}?",
        "What are the steps to finish {quest_name}?",
        "Guide me through {quest_name}.",
        "What is the process to solve {quest_name}?"
    ],
    "query_rewards": [
        "What are the rewards for completing {quest_name}?",
        "What do I earn from finishing {quest_name}?",
        "List the rewards for {quest_name}.",
        "What can I gain by completing {quest_name}?"
    ],
    "query_requirements": [
        "What are the requirements to start {quest_name}?",
        "What do I need to begin {quest_name}?",
        "What prerequisites are there for {quest_name}?",
        "What must be done before starting {quest_name}?"
    ],
    "query_start_point": [
        "Where does {quest_name} start?",
        "What is the starting point for {quest_name}?",
        "Where do I begin {quest_name}?",
        "How do I start {quest_name}?"
    ],
    "query_released": [
        "When was {quest_name} released?",
        "What is the release date of {quest_name}?",
        "When did {quest_name} first become available?",
        "What year was {quest_name} launched?",
        "When did {quest_name} release?",
        "When did {quest_name} come out?",
    ],
    "query_members": [
        "Is {quest_name} a members quest?",
        "Do you need a membership for the quest {quest_name}?",
        "Members needed for {quest_name}?",
        "Is Membership a must for {quest_name}?"
    ]
}

questions = []
for index, row in df.iterrows():
    quest_name = row['quest_name']
    for intent, template_list in templates.items():  # template_list is the list of templates for each intent
        for template in template_list:  # Iterate over each template in the list
            if quest_name != 'none':  # Ensure there is a valid quest name
                question = template.format(quest_name=quest_name)
                questions.append((question, intent))

generated_df = pd.DataFrame(questions, columns=['question', 'intent'])

final_df = generated_df

final_df.to_csv('intent_training_data.csv', index=False)
print("Training data has been successfully saved.")
