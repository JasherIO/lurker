# Lurker

Web crawls esports, primarily *Rocket League*, tournament sites for entrants and results. 

**Supported Sites**

* [Beyond Esports](http://teambeyond.net)
* [Rocket League Tracker Network](https://rocketleague.tracker.network)

## Installation

```bash
pip install scrapy
pip install validators
```

## Usage

```bash
scrapy crawl beyond -o teams.csv -a tournament="http://teambeyond.net/forum/tournaments/standings/160-astronauts-2000-rocket-league-3v3-1126-700pm-est/"
```

## Resources

* [League of Legends Scraper](https://medium.com/datadriveninvestor/how-i-created-a-league-of-legends-high-elo-database-using-scrapy-3becdee8f385)  
* [Yield Different Items](https://stackoverflow.com/questions/39227277/can-scrapy-yield-different-kinds-of-items)  
* [Clean Different Items in Pipeline](https://stackoverflow.com/questions/32743469/scrapy-python-multiple-item-classes-in-one-pipeline)  

## License

[MIT](https://choosealicense.com/licenses/mit/)
