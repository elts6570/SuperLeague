import numpy as np

import SL_tools as slt
import TM_tools as tmt


def flatten(xss):
    return [x for xs in xss for x in xs]


teams, games = {}, {}
for start_year in np.arange(2014, 2024):
	"""
	Iterate through all seasons since 2014 and gather the names of all teams that played in
	SuperLeague Greece.
	"""
	df = slt.scrape_super_league_teams(start_year, start_year + 1)
	teams[str(start_year) + "-" + str(start_year + 1)] = df['Teams']
	gm = slt.get_season_games(start_year)
	games[str(start_year) + "-" + str(start_year + 1)] = gm


# Alternative team names will be automatically retrieved in a future release.
team_name = 'PAOK Thessaloniki'
team_name_2 = 'PAOK Salonika'

# Retrieve when managers departed.
team_url = tmt.get_team_url(team_name)
managers = slt.get_team_managers(team_url)
end_dates_team = managers['End Date']

date_list, pts_list = [], []

for start_year in np.arange(2014, 2024):
	gm = games[str(start_year) + "-" + str(start_year + 1)]
	home_team = gm['Home Team']
	away_team = gm['Away Team']
	date_game = gm['Date']
	results = gm['Result']

	home = np.where(home_team==team_name_2)[0]
	away = np.where(away_team==team_name_2)[0]

	date_home = date_game[home]
	date_away = date_game[away]

	# Assuming no one scored > 9 goals, retrieve score from a:b format.
	res_home = results[home]
	home_1 = res_home.str.split(':').str[0].astype(int).tolist()
	home_2 = res_home.str.split(':').str[1].astype(int).tolist()

	# Compute statistics when home.
	draws_home = np.array([a == b for a, b in zip(home_1, home_2)]).astype(int)
	wins_home = np.array([a > b for a, b in zip(home_1, home_2)]).astype(int)
	lose_home = np.array([a < b for a, b in zip(home_1, home_2)]).astype(int)

	res_away = results[away]
	away_1 = res_away.str.split(':').str[0].astype(int).tolist()
	away_2 = res_away.str.split(':').str[1].astype(int).tolist()

	# Compute statistics when away.
	draws_away = np.array([a == b for a, b in zip(away_1, away_2)]).astype(int)
	wins_away = np.array([a < b for a, b in zip(away_1, away_2)]).astype(int)
	lose_away= np.array([a > b for a, b in zip(away_1, away_2)]).astype(int)

	# Flatten because we don't care whether the team was home or away
	dates = np.concatenate((date_home, date_away))
	draws = np.concatenate((draws_home, draws_away))
	wins = np.concatenate((wins_home, wins_away))
	lose = np.concatenate((lose_home, lose_away))

	# This is the final score.
	pts = 1 * draws + 3 * wins + 0 * lose

	date_list.append(dates)
	pts_list.append(pts)

date_list = flatten(date_list)
pts_list = flatten(pts_list)



