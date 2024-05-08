import requests
import csv
import time
from quest_links import quest_links
from bs4 import BeautifulSoup

def scrape_quest_data(wiki_link):
    # Initial Beautiful Soup Setup
    response = requests.get(wiki_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    quest_name = 'No Quest Name Found'
    quest_description = 'No paragraph found.'
    release_date = ""
    members_requirement = ""
    start_point = ""
    quest_requirements = ""
    quest_items = ""  # Initialize quest_items
    quest_enemies = ""
    quest_rewards = ""
    quest_steps = ""

    # Scraping the Quest Name (quest_name)
    content_div = soup.find('div', id='content')
    quest_name_span = content_div.find('h1', id='firstHeading').find('span') if content_div else None
    quest_name = quest_name_span.text if quest_name_span else 'No Quest Name Found'

    # Scraping the Quest Description (quest_description)
    content_div = soup.find('div', id='bodyContent')
    mw_content_text_div = content_div.find('div', id='mw-content-text') if content_div else None
    quest_description_paragraph = mw_content_text_div.find('p') if mw_content_text_div else None
    quest_description = ' '.join(
        quest_description_paragraph.stripped_strings) if quest_description_paragraph else 'No paragraph found.'

    # Scraping the Quest Release Date (quest_release_date)
    infobox = soup.find('table', class_='rsw-infobox no-parenthesis-style infobox-quest')
    if infobox:
        release_td = infobox.find('td', {"data-attr-param": "release"})
        if release_td:
            release_date_parts = list(release_td.stripped_strings)[:2]  # Only take the first two elements
            release_date = ' '.join(release_date_parts)

    # Scraping Membership Requirement (quest_membership_requirement)
    infobox = soup.find('table', class_='rsw-infobox no-parenthesis-style infobox-quest')
    members_info = ""
    if infobox:
        members_element = infobox.find(lambda tag: tag.name in ['th', 'td'] and 'Members' in tag.text)
        if members_element:
            members_requirement_td = members_element.find_next_sibling('td')
            if members_requirement_td:
                members_requirement = members_requirement_td.text.strip()

    # Scraping the Start Point of the Quest (quest_start_point)
    start_point = ""
    start_point_table = soup.find('table', class_='questdetails plainlinks')
    if start_point_table:
        start_point_data = start_point_table.find('td', {'data-attr-param': 'startDisp'})
        if start_point_data:
            text_parts = list(start_point_data.stripped_strings)[:-1]  # Convert to list and remove the last item
            start_point = ' '.join(text_parts).strip()

    # Scraping the Quest Requirements (quest_requirements)
    required_quests_info = []
    quest_ul = soup.find('td', style="padding-left:25px").find('ul')
    if quest_ul:
        li_tags = quest_ul.find_all('li', recursive=False)
        for li in li_tags:
            if li.find('a'):
                quest_text = ' '.join(li.stripped_strings).strip()
                required_quests_info.append(quest_text)
    quest_requirements = ', '.join(required_quests_info)

    # Scraping the Required Quest Items (quest_items)
    required_items_td = soup.find('td', {'data-attr-param': 'itemsDisp'})
    quest_items_parts = []
    quest_items = ""
    if required_items_td:
        lighttable_checklist_div = required_items_td.find('div', class_='lighttable checklist')
        if lighttable_checklist_div:
            list_items = lighttable_checklist_div.find_all('li')
            quest_items_parts = [li.get_text(separator=" ").strip() for li in list_items]
            quest_items = ','.join(quest_items_parts)

    # Scraping the Enemies needed to be defeated (quest_enemies)
    enemies_info = []
    enemies_td = soup.find('td', {'data-attr-param': 'kills'})
    if enemies_td:
        li_tags = enemies_td.find_all('li')
        for li in li_tags:
            text = ' '.join(li.stripped_strings)
            enemies_info.append(text)
    quest_enemies = ', '.join(enemies_info)

    # Scraping Steps Description (quest_steps)
    body_content = soup.find('div', id='bodyContent')
    paragraphs = []
    if body_content:
        p_tags = body_content.find_all('p', recursive=True)
        for p in p_tags:
            paragraphs.append(p.get_text(strip=True))
    quest_steps = ' '.join(paragraphs)

    # Scraping the Quest Rewards (quest_rewards)
    rewards_header = soup.find(lambda tag: tag.name == 'h2' and 'Rewards' in tag.text)
    if rewards_header:
        next_ul = rewards_header.find_next('ul')
        if next_ul:
            quest_rewards = ', '.join([li.get_text(strip=True) for li in next_ul.find_all('li')])
        else:
            quest_rewards = 'Rewards list not found.'
    else:
        quest_rewards = 'Rewards section not found.'

    return quest_description, quest_name, release_date, members_requirement, start_point, quest_items, quest_enemies, quest_requirements, quest_rewards, quest_steps


# This will be a list of dictionaries with the scraped data
all_quest_data = []

# Iterate over the list of URLs
for url in quest_links:
    quest_data = scrape_quest_data(url)
    all_quest_data.append(quest_data)
    time.sleep(1)

# Write to CSV
csv_file = 'quests_data.csv'
csv_headers = ['quest_description', 'quest_name', 'release_date', 'members_requirement',
               'start_point', 'quest_items', 'quest_enemies', 'quest_requirements',
               'quest_rewards', 'quest_steps']

# Convert all your tuples to dictionaries
all_quest_data_dicts = []
for quest_tuple in all_quest_data:
    quest_dict = dict(zip(csv_headers, quest_tuple))
    all_quest_data_dicts.append(quest_dict)

# Now write the list of dictionaries to a CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()
    for quest_data in all_quest_data_dicts:
        writer.writerow(quest_data)

print(f'Data written to {csv_file}')
