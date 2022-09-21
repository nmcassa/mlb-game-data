# mlb-game-data
 A storage for a scraper that can write txt files containing season results

 Currently there is only information held from the 2019 and 2021 seasons. More seasons can be accessed by changing the url in the python script and also the id for the regular season games in the find python script. 

```python
 page = get_parsed_page("https://www.baseball-reference.com/leagues/majors/2019-schedule.shtml")

 data = page.find("div", {'id': "all_9125626744"})
```

All of the information in the .txt files are formatted in this way:

```python
f.write("%s(%s)@%s(%s)^%s#%s\n" % (bs.home, bs.homeRecord, bs.away, bs.awayRecord, bs.homeScore, bs.awayScore))
```

Therefore, even though it is written:

```
Baltimore Orioles(17-25)@Tampa Bay Rays(25-19)^1#10
```

The Orioles are the Home Team. Sorry, that's confusing. Was just using the @^# symbols to make parsing later on easier.

## Read

```python
outcomes = read("2019")

print(outcomes[100].jsonify())
```

returns:

```json
{
    "info": "Pittsburgh Pirates(1-3)@Cincinnati Reds(1-4)^2#0",
    "home": {
        "Team": "Pittsburgh Pirates",
        "Record": "1-3",
        "Score": "2"
    },
    "away": {
        "Team": "Cincinnati Reds",
        "Record": "1-4",
        "Score": "0"
    }
}
```

### std

```python
Total Runs
 Average: 9.661177439275422
 Std: 4.75899828210121
Home Team Runs
 Average: 4.824619184849732
 Std: 3.218493786398544
Away Team Runs
 Average: 4.8365582544256895
 Std: 3.4225004177520515
```