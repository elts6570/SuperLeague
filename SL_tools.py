import numpy as np

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def _convert_european(day):
    date_object = datetime.strptime(day, '%m/%d/%y')
    european_date = date_object.strftime('%d/%m/%y')
    return european_date


def _reverse_date(date):
    try:
        date_object = datetime.strptime(date, '%b %d, %Y')
        reversed_date = date_object.strftime('%d/%m/%y')
        return reversed_date
    except:
        return None


def _remove_parentheses(text):
    return re.sub(r'\([^)]*\)', '', text).strip()


def get_team_managers(team_url):
    """
    Queries a team's URL on Transfermarkt and returns a dataframe with its managers' names, start and end date of their contract.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    response = requests.get(team_url, headers = headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {team_url}")

    soup = BeautifulSoup(response.content, 'html.parser')

    manager_table = soup.find('div', {'id': 'yw1'}) 
    if not manager_table:
        raise Exception("Could not find manager history table")

    rows = manager_table.find_all('tr')[1:]

    managers = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 5:
            continue 

        manager_name = cols[2].get_text(strip=False)
        start_date = cols[5].get_text(strip=True)
        end_date = cols[6].get_text(strip=True)

        managers.append({
            'Manager': manager_name,
            'Start Date': _reverse_date(start_date),
            'End Date': _reverse_date(end_date),
        })
        df = pd.DataFrame(managers)
    return df


def _get_teams_for_season(season):
    url = f'https://www.transfermarkt.com/super-league/startseite/wettbewerb/GR1/plus/?saison_id={season}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load page for season {season}")

    soup = BeautifulSoup(response.content, 'html.parser')

    manager_table = soup.find('table', {'class': 'items'})
    if not manager_table:
        raise Exception(f"Could not find teams table for season {season}")

    teams = []
    for row in manager_table.find_all('tr')[1:]: 
        cells = row.find_all('td')
        if len(cells) < 2:
            continue

        team_cell = row.find('td', {'class': 'hauptlink'})
        if not team_cell:
            print(f"Warning: Could not find team cell in row: {row}")
            continue

        team_name = team_cell.get_text(strip=True)
        teams.append(team_name)

    return teams


def scrape_super_league_teams(start_year, end_year):
    """
    Queries Transfermarket for all SL teams that played in a season bounded by start_year and end_year.
    """
    all_teams = []

    teams = _get_teams_for_season(start_year)
    for team in teams:
        all_teams.append({
            'Season': f"{start_year}/{end_year}",
            'Teams': team
                })

    return pd.DataFrame(all_teams)


def _cleanup_dates(df, season):
    # If missing day + month + year, inherit the most recently encountered date.
    dates = np.array(df['Date'])
    
    days = []
    for i in range(len(dates)):
        alpha = dates[i][0].isalpha()

        if alpha:
            day = dates[i][:10]
            try:
                if int(day[-3:]) > 99:
                    day = dates[i][:9]
            except:
                day = dates[i][:10]
            day = day[3:]


        inherit = day
        if not alpha:
            if inherit[0].isalpha():
                inherit = inherit[3:]
            day = inherit 
        
        if day[-2:].isdigit():
            year = day[-2:]
        if not day[-2:].isdigit():
            day = day + year[-1]
        days.append(_convert_european(day))
    return days


def get_season_games(season):
    """
    Queries Transfermarkt and returns all games in a given season, along with their dates and full time score.
    """
    url = f'https://www.transfermarkt.com/protathlima-stoiximan-super-league/gesamtspielplan/wettbewerb/GR1/saison_id/{season}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load page for season {season}")

    soup = BeautifulSoup(response.content, 'html.parser')
    
    games = []

    
    matchdays = soup.find_all('div', class_ = 'content-box-headline')
    for matchday in matchdays:
        table = matchday.find_next('table')
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
        
        match_date = None
        for row in rows:
            date_cell = row.find('td', class_ = 'show-for-small')
            if date_cell:
                match_date = date_cell.get_text(strip = True)
                continue  
            
            cells = row.find_all('td')
            if len(cells) < 7:
                continue 
            
            home_team = cells[2].get_text(strip = True)
            result = cells[4].get_text(strip = True)
            away_team = cells[6].get_text(strip = True)

            games.append({
                'Date': match_date,
                'Home Team': _remove_parentheses(home_team),
                'Away Team': _remove_parentheses(away_team),
                'Result': result
            })

    df = pd.DataFrame(games)
    days = _cleanup_dates(df, season)
    df['Date'] = days
    return df


