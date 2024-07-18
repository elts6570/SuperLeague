import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def visualise(df, squad):
    """
    Receive team's name and managers' dataframe to create a timeline of managers'
    arrivals and departures in a team.
    """
    fig, ax = plt.subplots(dpi=120, figsize=(20,20))
    
    colors = plt.cm.tab20.colors
    
    for i, row in df.iterrows():
        ax.barh(row['Manager'], (row['End Date'] - row['Start Date']).days,
                left=row['Start Date'], color=colors[i % len(colors)], align='center')
    
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    plt.xlabel('Date')
    plt.ylabel('Manager')
    plt.title(squad + ': Manager Tenures Over Time')
    
    plt.xticks(rotation=45)
    
    plt.grid(True)
    plt.show()
    return None