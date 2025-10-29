# Greek SuperLeague: Probing the Honeymoon Statistics

With the present algorithm, we are interested in probing the so-called honeymoon statistics (Kuper, Simon, Soccernomics, New York, Nation Books, 2009), the change in the performance of a team after a manager's departure. The effect has been documented across various teams ([UK Sports Yahoo](https://uk.sports.yahoo.com/news/soccernomics-does-sacking-manager-actually-182544870.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAHLklveZlGvXzToFAAhbWTGTBQ4l7ft7VOZp-KrpaL3miSt5GIrn2QNJDit6AkNqkzsSKC4C7mmKiBsw84rWYbKGXCsxaXtyRC10_5q7iSUfPqE-13jdzfpoH3IuLyMWsPuG_pLuiZWs8TxO3x_K02Qz1j63ak4sbvMGBrMzHzRG)).
We create a utility to query [TranferMarkt](https://www.transfermarkt.com), a database of football data. Our playground is the Greek SuperLeague and in particular, the teams that participated in it over the past decade. We are interested in the past decade, in order to gather sufficient statistics about managers' departures and the change in the score of a team. The output of this algorithm is a database containing the points a team gathers as a function of date and the dates of its managers' departures. This data can then be post-processed to obtain the cross-correlation between a team's performance and the time elapsed after a manager's departure. Below is a sample product using the output of this code for PAOK Thessaloniki. The black lines indicate the date at which a maneger left the team.

<img width="886" alt="image" src="https://github.com/user-attachments/assets/bbb2d0f4-bcc4-469e-91dd-b120717377e6">

## Modules

* SL_tools.py: SuperLeague-related tools, to get a team's managers, retrieve the teams that played in a season and the game statistics
* TM_tools.py: Tranfermarkt-related tools, to move from one page to another
* visualise_manager_data.py: Create a timeline of the managers changes in each team.
* main.py: Iterate over the seasons and compute each team's final score in each season.

## Dependencies:

Ensure you have the necessary dependencies installed:
- numpy
- pandas
- matplotlib
- beautifulsoup4
- requests

## Disclaimer:

This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

## Prohibited Use:

This software shall not be used for any malicious purposes, including but not limited to hacking, unauthorized access, cyber attacks, or any activity that harms others or violates any laws or regulations.
