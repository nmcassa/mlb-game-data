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