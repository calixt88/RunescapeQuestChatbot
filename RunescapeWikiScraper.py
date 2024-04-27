import requests
from bs4 import BeautifulSoup

def scrape_quest_data(url):
    # Initial Beautiful Soup Setup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scraping the Quest Name (quest_name)
    content_div = soup.find('div', id='content')
    quest_name_span = content_div.find('h1', id='firstHeading').find('span') if content_div else None
    quest_name = quest_name_span.text if quest_name_span else 'No Quest Name Found'

    # Scraping the Quest Description (quest_description)
    content_div = soup.find('div', id='bodyContent')
    mw_content_text_div = content_div.find('div', id='mw-content-text') if content_div else None
    quest_description_paragraph = mw_content_text_div.find('p') if mw_content_text_div else None
    quest_description = ' '.join(quest_description_paragraph.stripped_strings) if quest_description_paragraph else 'No paragraph found.'

    # Scraping the Quest Release Date (quest_release_date)
    infobox = soup.find('table', class_='rsw-infobox no-parenthesis-style infobox-quest')
    release_date = ""
    if infobox:
        # Look for the 'td' with 'data-attr-param' set to 'release'
        release_td = infobox.find('td', {"data-attr-param": "release"})
        if release_td:
            # Get all text within the 'td' element, and take only the first two parts (usually the date and year)
            release_date_parts = list(release_td.stripped_strings)[:2]  # Only take the first two elements
            release_date = ' '.join(release_date_parts)

    # Scraping Membership Requirement (quest_membership_requirement)
    infobox = soup.find('table', class_='rsw-infobox no-parenthesis-style infobox-quest')
    members_info = ""
    if infobox:
        # Find the <th> or <td> element containing the word "Members"
        members_element = infobox.find(lambda tag: tag.name in ['th', 'td'] and 'Members' in tag.text)
        if members_element:
            # Get the next <td> sibling which should contain the text "Yes" or "No"
            members_requirement_td = members_element.find_next_sibling('td')
            if members_requirement_td:
                members_requirement = members_requirement_td.text.strip()

    # Scraping the Start Point of the Quest (quest_start_point)
    start_point = ""
    start_point_table = soup.find('table', class_='questdetails plainlinks')
    if start_point_table:
        # Find the td element that has a 'data-attr-param' of 'start'
        start_point_data = start_point_table.find('td', {'data-attr-param': 'startDisp'})
        if start_point_data:
            # Extract all text from this td element
            text_parts = list(start_point_data.stripped_strings)[:-1]  # Convert to list and remove the last item
            start_point = ' '.join(text_parts).strip()

    # Scraping the Quest Requirements (quest_requirements)

    # Scraping the Required Quest Items (quest_items)
    required_items_td = soup.find('td', {'data-attr-param': 'itemsDisp'})
    quest_items_parts = []
    if required_items_td:
        # Find the div that contains the actual list items
        lighttable_checklist_div = required_items_td.find('div', class_='lighttable checklist')
        if lighttable_checklist_div:
            # Find all list items
            list_items = lighttable_checklist_div.find_all('li')
            # Extract the text from each list item
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

    # Scraping the Quest Rewards (quest_rewards)

    # Scraping the Quest Achievements (quest_achievements)

    return quest_description, quest_name, release_date, members_requirement, start_point, quest_items, enemies_info, quest_enemies



# URL to scrape
# url = 'https://runescape.wiki/w/Observatory_Quest'
url = 'https://runescape.wiki/w/Wanted!'
quest_data = scrape_quest_data(url)
print(quest_data)
