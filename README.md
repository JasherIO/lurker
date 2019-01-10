# Lurker

Web crawls esports, primarily *Rocket League*, tournament sites for entrants and results. 

**Supported Sites**

* [Beyond Esports](https://teambeyond.net/forum/tournaments/home/)
  * Specifically *Rocket League* Astronauts tournaments
* [Rocket League Tracker Network](https://rocketleague.tracker.network)
* [Tespa](https://compete.tespa.org/tournament)
  * Specifically *Rocket League* CRL tournaments

## Installation

```bash
pip install scrapy
pip install validators
```

## Usage

```bash
scrapy crawl beyond -o teams.csv -a tournament="https://teambeyond.net/forum/tournaments/164-astronauts-2000-rocket-league-3v3-1217-700pm-est/standings/"
```

## Resources

* [Clean Different Items in Pipeline](https://stackoverflow.com/questions/32743469/scrapy-python-multiple-item-classes-in-one-pipeline)  
* [League of Legends Scraper](https://medium.com/datadriveninvestor/how-i-created-a-league-of-legends-high-elo-database-using-scrapy-3becdee8f385)  
* [Yield Different Items](https://stackoverflow.com/questions/39227277/can-scrapy-yield-different-kinds-of-items)  

## License

[MIT](https://choosealicense.com/licenses/mit/)
