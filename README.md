# DKSportsbookClient
A Python client for making better sense of DraftKings Sportsbook's API.

## Getting started
1. Install `DKSportsbookClient` from this repository using `pip`:
 
       python3 -m pip install git+https://github.com/esqew/DKSportsbookClient.git

2. Import & instantiate the client in your script:

       import DKSportsbookClient
       client = DKSportsbookClient()

3. Start using it to pull information from DraftKings' API:

       client.league("NBA").get_events()
       # ...

## Key concepts
### Player location
For a number of reasons, DraftKings likes to try to geo-locate you while you're interacting with their service. (This is separate from the geo-location they do for registered users placing wagers via things like the Player Location Check software.) Things like the leagues, markets, and bet types that DraftKings serves to you (among others) seems to be highly dependent on the result of this upfront location check.

On first instantiation, `DKSportsbookClient` parses makes a request to `https://sportsbook.draftkings.com` and parses the response HTML for certain key elements to dynamically determine which of their markets DraftKings has detected you accessing it from.

In future releases, I would like to give developers the ability to override whatever endpoints DraftKings tells you to use in this upfront call, but this idea still needs to be analyzed a bit for feasibility.

### Data model
DraftKings Sportsbook uses a specific heirarchy in their data model, which I've tried to emulate as much as possible where it makes sense:

    --> Sport
        --> League (a.k.a. "event group")
            --> Event
                --> Category
                    --> Market (bet type, i.e. moneyline, spread, over/under)
                        --> Selection