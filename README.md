# Fairlay Public API Documentation v0

This is a free service to scrape all markets on Fairlay. For all POST requests (creating/changing markets and orders) use the paid API.
* The data is updated every 5 seconds;
* You have to accept GZIP, DEFLATE in your HEADER;
* Use the __*SoftChangedAfter*__ parameter for incremental calls. Retrieve the server time and only query markets that have changed after your last request;
* 12 incremental calls are allowed per minute (the __*SoftChangedAfter*__ parameter must be set to not more than 30 seconds in the past);
* 1 call without a proper __*SoftChangedAfter*__ parameter is allowed per IP per minute;
* When using the markets request make sure that your URI is not too long;
* All times are UTC;
* Strings are not case sensitive.

For more examples how this API should be used together with our paid API, please take a look at our sample clients in [C#](https://github.com/Fairlay/CSharpSampleClient/blob/master/GetAPI.cs) and [Python](https://github.com/Fairlay/PythonSampleClient/blob/master/client.py#L291).


Please feel free to comment and make suggestions.

## Servers

> `http://31.172.83.181:8080` <br/>
> `http://31.172.83.53:8080` *(is an alternate server with the same functionality)*


## View markets on Fairlay

You can use the market ids to access any market on fairlay directly

> `https://www.fairlay.com/market/MARKETID`

<br/>

---

## Methods

### Server Time
Returns the server time in ticks.

> `http://31.172.83.181:8080/free/time`

<br/>

### Markets
Returns JSON encoded list of markets that apply to the given filter.

> `http://31.172.83.181:8080/free/markets/JSON-ENCODED-MARKETFILTER`

<br/>
MARKETFILTER object looks like this:

```json
{
        "Cat":0,
        "RunnerAND":["Arsenal","Chelsea"],
        "TitleAND":null,
        "TitleNOT":["Corners","Throwin"],
        "Comp":"Premier League",
        "TypeOR":null,
        "PeriodOR":[1],
        "SettleOR":null,
        "Descr":null,
        "ChangedAfter":"2016-01-01T22:01:01",
        "SoftChangedAfter":"0001-01-01T00:00:00",
        "OnlyActive":false,
        "NoZombie":false,
        "FromClosT":"2016-05-01T00:00:00",
        "ToClosT":"0001-01-01T00:00:00",
        "FromID":0,
        "ToID":10000
}
```

*Cat:* Category, see A2) for more information. 0 queries all Categories.

*TitleAND*: List of strings which all must appear in the title of the market.

*RunnerAND*: List of strings which all must be contained in at least one name of one runner of the market.

*TitleNOT: List of strings which none may appear in the title of the market.

*Comp*: Competition name. __null__ to get all competitions.

*TypeOr*: Market Types, see A2) for more information. Only the Market Types given will be returned. If set to null, all market types will be returned.

*PeriodOr*: Market Period, see A2) for more information.

*SettleOr*: Settlement Type, see A2) for more information.

*NoZombie*: If `True`, no empty markets will be returned (without any open order).

*Descr*: The given string must appear in the market description.

*ChangedAfter*: Return markets where the meta data was changed after the given date. Usually the Closing and Settlement
Dates of a market is the only data that changes.

*SoftChangedAfter*: Return all markets, where either the the meta data or the orderbook has changed since the given date.

*FromClosT*: Return markets where the closing time is greater than the given one.

*FromID* and *ToID*: Use for paging requests. __ToID__ has a default value of 300 if not set.


#### Examples:

Returns the first 100 non-empty soccer markets, where one of the runners is Portugal, the Title does not contain the words "Corners" or "Throwin" and the period of the match is full-time.

> `http://31.172.83.181:8080/free/markets/{"Cat":1,"NoZombie":true,"RunnerAND":["Portugal"], "TitleNOT":["Corners","Throwin"], "PeriodOR":[1],"FromID":0,"ToID":100}`

<br/>

Returns all active tennis matches of the type Over/Under or Outright where the odds or market data have changed after June 1st 12:01:30pm.

>`http://31.172.83.181:8080/free/markets/{"Cat":2,"TypeOr":[1,2],"SoftChangedAfter":"2016-06-01T12:01:30","OnlyActive":true,"ToID":10000}`

<br/>

Returns all active non-empty markets.

>`http://31.172.83.181:8080/free/markets/{"OnlyActive":true,"NoZombie":true,"ToID":100000}`

<br/>

### Competitions

Returns all competitions in the selected category.

> `http://31.172.83.181:8080/free/comps/CATEGORYID`

<br/>

Example for all soccer competitions:
> `http://31.172.83.181:8080/free/comps/1`

<br/>


## A2) DATA Fields


```CSharp
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

Category:
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
        POLITICS = 15;
        FINANCIAL = 16;
        GREYHOUND = 17;
        VOLLEYBALL = 18;
        HANDBALL = 19;
        DARTS = 20;
        BANDY = 21;
        WINTERSPORTS = 22;
        BOWLS = 24;
        POOL = 25;
        SNOOKER = 26;
        TABLETENNIS = 27;
        CHESS = 28;
        HOCKEY = 30;
        FUN = 31;
        ESPORTS = 32;
        RESERVED4 = 34;
        MIXEDMARTIALARTS = 35;
        RESERVED6 = 36;
        RESERVED = 37;
        CYCLING = 38;
        RESERVED9 = 39;
```