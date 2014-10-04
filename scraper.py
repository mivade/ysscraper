"""Yahoo Sports CFB data scraper"""

from __future__ import print_function
import os.path
import json
import urllib2
import re
from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup
import tabledef

_db_file = 'data.sqlite'

class YahooScraper(object):
    """Scrapes data from Yahoo Sports."""
    _datefmt = '%Y-%m-%d'
    _team_names_file = 'data/teams.csv'
    
    def __init__(self):
        with open('urls.json') as json_file:
            self.urls = json.load(json_file)
        self.conn = sqlite3.connect(_db_file)

    def get_team_names(self):
        """Obtain all team names and save them to the database.

        Notes
        -----
        The URLs use the division names "I-A" and "I-AA" to signify
        FBS and FCS, respecitvely.

        """
        # Check if we should proceed
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams';")
        if len(cur.fetchall()) is not 0:
            print("teams table already populated.")
            return
        self.conn.execute(tabledef.teams)
        self.conn.commit()

        # Load HTML for scraping
        print("Fetching team names...")
        try:
            url = self.urls['names'].format(division="I-A")
            fbs_html = urllib2.urlopen(url)
            url = self.urls['names'].format(division="I-AA")
            fcs_html = urllib2.urlopen(url)
        except urllib2.URLError:
            print("Failed to fetch names. Are the URLs incorrect?")
            
        # Scrape FBS
        #conferences = fbs_html.find_all('span', class_='yspdetailttl')
        soup = BeautifulSoup(fbs_html)
        teams = soup.find_all('a', href=re.compile('^/ncaaf/teams/'))
        for team in teams:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO teams(name,division) VALUES (?,?)",
                    (team.text, 'FBS')
                )

        # Scrape FCS
        soup = BeautifulSoup(fcs_html)
        teams = soup.find_all('a', href=re.compile('^/ncaaf/teams/'))
        for team in teams:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO teams(name,division) VALUES (?,?)",
                    (team.text, 'FCS')
                )

    def get_scores(self, week, with_stats=False):
        """Get all scores from one week.

        Notes
        -----
        The URLs for all games use "conference" names 'fbs_all' and
        'fcs_all' for all games in FBS and FCS,
        respectively. Unfortunately, the link for all FBS and FCS does
        not appear to work for all weeks, so they would have to be
        scraped separately.

        """
        # Fetch scores
        assert isinstance(week, int)
        print("Fetching scores for week {}...".format(week))
        url = self.urls['scores'].format(conf='fbs_all', week=week)
        try:
            html = urllib2.urlopen(url)
        except urllib2.URLError:
            print("Failed to fetch scores.")
        soup = BeautifulSoup(html)

        # Filter for game rows
        def game_row(tag):
            try:
                if tag['class'] == ['game', 'link']:
                    return True
                else:
                    return False
            except:
                return False

        # Empty dictionary for storing score data
        data = {
            'date': [],
            'home.team': [],
            'home.score': [],
            'away.team': [],
            'away.score': [],
            'uid': [],
            'url': []
        }

        # Get score data
        # TODO: make self.scores a list or dictionary to store more
        # than one week at a time in memory
        games = soup.find_all(game_row)
        for game in games:
            date_str = game['data-gid'].split('.')[2][:8]
            date = datetime.strptime(date_str, '%Y%m%d')
            home = game.find('td', class_='home').find('em').text
            away = game.find('td', class_='away').find('em').text
            score = game.find('td', class_='score')
            home_score = int(score.find(True, class_='home').text)
            away_score = int(score.find(True, class_='away').text)
            url = 'http://sports.yahoo.com' + game['data-url']
            data['date'].append(date)
            data['home.team'].append(home)
            data['home.score'].append(home_score)
            data['away.team'].append(away)
            data['away.score'].append(away_score)
            data['uid'].append(game['data-gid'])
            data['url'].append(url)
            if with_stats:
                stats = self.get_team_stats(url)
                for key in stats:
                    new_key = key.lower().split()
                    akey = 'away.' + '_'.join(new_key)
                    hkey = 'home.' + '_'.join(new_key)
                    if akey not in data:
                        data[akey] = [stats[key][0]]
                        data[hkey] = [stats[key][1]]
                    else:
                        data[akey].append(stats[key][0])
                        data[hkey].append(stats[key][1])
        self.scores = pd.DataFrame(data)

    def get_team_stats(self, url):
        """Get the team stats from the game page at url."""
        # Get relevant section of the HTML file
        print("Attempting to connect to", url)
        try:
            html = urllib2.urlopen(url)
        except:
            raise RuntimeError("Failed fetching URL " + url)
        soup = BeautifulSoup(html)
        title = soup.title.text.split('|')
        title = '{} ({})'.format(title[0].strip(), title[1].strip())
        print("Parsing data for {}...".format(title))
        stats = soup.find('h3', text=u'Team Stats').parent.parent
        rows = stats.find('table').find_all('tr')

        # Empty dictionary for data
        data = {}

        # Crawl the table
        for row in rows:
            if row.find().text == '':
                continue
            stat_name = row.find('th', class_='stat-name').text
            stats = row.find_all('td')
            away = stats[0].text
            home = stats[1].text
            data[stat_name] = [away, home]
        return data
            
    def export(self, location, kind='scores', fmt='csv'):
        """Export data.

        Parameters
        ----------
        location : str
            Path to save the data to.
        kind : str
            Which data to export. Default: 'scores'
        fmt : str
            Data format to use. Default: 'csv'

        """
        kinds = ['scores']
        formats = ['csv']
        if kind not in kinds:
            raise RuntimeError("Invalid data kind. Must be one of " + str(kinds))
        if fmt not in formats:
            raise RuntimeError("Invalid format. Must be one of " + str(formats))

        # Select the data to write
        if kind is 'scores':
            data = self.scores

        # Write data
        if fmt is 'csv':
            data.to_csv(location, index=False, date_format=self._datefmt)

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.mkdir('data')
    scraper = YahooScraper()
    t_start = datetime.now()
    print("Starting at {}...".format(datetime.ctime(t_start)))
    scraper.get_team_names()
    #for i in range(1, 2):
    #    scraper.get_scores(i, with_stats=True)
    #    scraper.export('data/scores_2014_week_{:02d}.csv'.format(i), fmt='csv')
    t_end = datetime.now()
    print("Finished at {}.".format(datetime.ctime(t_end)))
    print("Total time:", str(t_end - t_start))
    
