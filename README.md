#API DOCUMENTATION v0 - Fairlay Node


This is a free service to scrape all markets on Fairlay. For all post requests (creating / changing markets and orders) use the paid API.

- the data is updated every 5 seconds
- use the "SoftChangedAfter" parameter for incremental calls. Retrieve the server time and only query markets that have changed after your last request.

- 12 incremental calls are allowed per minute (the SoftChangedAfter parameter must be set to not more than 30 seconds in the past)
- 1 call without a proper SoftChangedAfter parameter  is allowed per IP and per minute
- you have to accept gzip,deflate in your header
- when using the markets request make sure that your uri is not too long
- all times are UTC
- strings are not case sensitiv

For more examples how this API should be used together with our paid API, please take a look at our sample clients
- https://github.com/Fairlay/CSharpSampleClient/blob/master/GetAPI.cs
- https://github.com/Fairlay/PythonSampleClient/blob/master/client.py#L291




Please feel free to comment and make suggestions. 
http://31.172.83.53  is an alternate server with the same functionality.


##server time

http://31.172.83.181:8080/free/time

returns the server time in ticks.

#markets

Usage:

http://31.172.83.181:8080/free/markets/[json encoded marketfilter object]

marketfilter object looks like this:

{"Cat":0,"RunnerAND":["Arsenal","Chelsea"],"TitleAND":null,"TitleNOT":["Corners","Throwin"],"Comp":"Premier League","TypeOR":null,"PeriodOR":[1],"SettleOR":null,"Descr":null,"ChangedAfter":"2016-01-01T22:01:01","SoftChangedAfter":"0001-01-01T00:00:00","OnlyActive":false,"NoZombie":false,"FromClosT":"2016-05-01T00:00:00","ToClosT":"0001-01-01T00:00:00","FromID":0,"ToID":10000}

Cat: is the Category, see A2) for more information. 0 queries all Categories.
RunnerAND: All strings provided must be contained in at least one name of one runners of the market.
TitleNOT: = None of the strings may appear in the title of the market
Comp:   if not null, must equal the competition's name.
TypeOr:   Only the Market Types given will be returned. If set to null, all market types will be returned. See A2) for Market Types
PeriodOr: Similiar to TypeOr See A2) for Market Periods
SettleOr: See A2)  for Settlement Types
NoZombie: if set to true, no empty markets will be returned (without any open order)
Descr:   The given string must appear in the market description.
ChangedAfter:   Only returns markets, where the meta data was changed after the given date. Usually the Closing and Settlement Dates of a market is the only data that changes.
SoftChangedAfter:  returns all markets, where either the the meta data or the orderbook has changed since the given date.


FromClosT:  only return markets where the closing time is greater than the given one.

FromID:  for paging requests. 
ToID (default 300 if not set):   should be set.

Returns:  json encoded list of markets that apply to the given filter. 


####Examples: 

 http://31.172.83.181:8080/free/markets/{"Cat":1,"NoZombie":true,"RunnerAND":["Portugal"], "TitleNOT":["Corners","Throwin"], "PeriodOR":[1],"FromID":0,"ToID":100}


returns the first  100 non-empty soccer markets, where one of the runners is Portugal, the Title does not contain the words "Corners" or "Throwin" and the period of the match is full-time.

http://31.172.83.181:8080/free/markets/{"Cat":2,"TypeOr":[1,2],"SoftChangedAfter":"2016-06-01T12:01:30","OnlyActive":true,"ToID":10000}  

Returns all active tennis matches of the type Over/Under or Outright where the odds or market data have changed after  June 1st  12:01:30pm 



http://31.172.83.181:8080/free/markets/{"OnlyActive":true,"NoZombie":true,"ToID":100000}

Returns all active non-empty markets.

##competitons

http://31.172.83.181:8080/free/comps/[sportid]

find the sport ID below.

Example for all soccer competitions: http://31.172.83.181:8080/free/comps/1

##access markets on fairlay

You can use the market ids to access any market on fairlay directly

https://www.fairlay.com/market/72633292476


## A2) DATA Fields


 enum MarketPeriod
        
            UNDEFINED,
            FT,
            FIRST_SET,
            SECOND_SET,
            THIRD_SET,
            FOURTH_SET,
            FIFTH_SET,
            FIRST_HALF,
            SECOND_HALF,
            FIRST_QUARTER,
            SECOND_QUARTER,
            THIRD_QUARTER,
            FOURTH_QUARTER,
            FIRST_PERIOD,
            SECOND_PERIOD,
            THIRD_PERIOD,
           
        

enum StatusType
        
            ACTIVE,
            INPLAY,
            SUSPENDED,
            CLOSED,
            SETTLED,
            CANCELLED

        

enum MarketType
        
            M_ODDS,
            OVER_UNDER,
            OUTRIGHT,
            GAMESPREAD,
            SETSPREAD,
            CORRECT_SCORE,
            FUTURE,
            BASICPREDICTION,
            RESERVED2,
            RESERVED3,
            RESERVED4,
            RESERVED5,
            RESERVED6

            

        


enum SettleType
        
            BINARY,
            DECIMAL


Categories:


        SOCCER = 1;
        TENNIS = 2;
        GOLF = 3;
        CRICKET = 4;
        RUGBYUNION = 5;
        BOXING = 6;
        HORSERACING = 7;
        MOTORSPORT = 8;
        SPECIAL = 10;
        RUGBYLEAGUE = 11;
        BASKETBALL = 12;
        AMERICANFOOTBALL = 13;
        BASEBALL = 14;
        HOCKEY = 30;
    
       
        POLITICS = 15;
        FINANCIAL = 16;
        GREYHOUND = 17;
        VOLLEYBALL = 18;
        HANDBALL = 19;
        DARTS = 20;
        BANDY = 21;
        WINTERSPORTS = 22;
        BOWLS =24;
        POOL = 25;
        SNOOKER = 26;
        TABLETENNIS = 27;
        CHESS = 28;
        FUN = 31;
        ESPORTS = 32;
        RESERVED4 = 34;
        MIXEDMARTIALARTS = 35;
        RESERVED6 = 36;
        RESERVED = 37;
        CYCLING = 38;
        RESERVED9 = 39;

