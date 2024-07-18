import requests
from bs4 import BeautifulSoup


def get_team_url(team_name):
    """
    Queries Transfermarkt with a team's name to retrieve the URL corresponding to its historical record. 
    """
    search_url = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={team_name.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load search results for {team_name}")

    soup = BeautifulSoup(response.content, 'html.parser')
    link = soup.find('td', class_='zentriert').find_next('a', title='Squad ' + team_name)

    if link:
        url = link['href']
        full_url = 'https://www.transfermarkt.com' + url
        history_url = full_url.replace('kader', 'mitarbeiterhistorie')
    else:
        print("Link not found.")
    return history_url


