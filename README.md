This is a free service to scrape all markets on Fairlay. For all POST requests (creating/changing markets and orders) use the paid [Private API](../Private-API).
* The data on the free servers is updated every 5 seconds 
* For Professional Users there exist private servers with an update frequency of half a second. Please contact   fairlay+api@protonmail.com to get access.
* You have to accept GZIP, DEFLATE in your HEADER
* Use the __*SoftChangedAfter*__ parameter for incremental calls. Retrieve the server time and only query markets that have changed after your last request
* 12 incremental calls are allowed per minute (the __*SoftChangedAfter*__ parameter must be set to not more than 30 seconds in the past)
* 1 call without a proper __*SoftChangedAfter*__ parameter is allowed per IP per minute
* When using the markets request make sure that your URI is not too long
* All times are UTC (like DateTime.UtcNow, to account for any time difference with your developer machine grab [Server Time](#server-time), in the C# API all calls other than time will do this automatically for you)
* Strings are not case sensitive

For more examples how this API should be used together with our paid API, please take a look at our sample clients in [C#](https://github.com/Fairlay/FairlayDotNetClient/blob/master/PublicApi/PublicApiRequest.cs) and [Python](https://github.com/Fairlay/PythonSampleClient/blob/master/client.py#L291).

Please feel free to comment and make suggestions.


## Free Servers

> `http://31.172.83.181:8080` *(used by default for all Public API calls)*<br/>
> `http://31.172.83.53:8080` *(is an alternate server with the same functionality, also used for all [Private API](../private-api) calls)*


## View markets on Fairlay

You can use the market ids to access any market on fairlay directly

> `https://fairlay.com/market/MARKETID`

Example:
> `https://fairlay.com/market/will-donald-trump-be-president-at-year-end-2018/`

<br />

## Methods

For examples on how to use each of the API calls presented here, see the [C# Unit Tests](https://github.com/Fairlay/FairlayDotNetClient/tree/master/src/Tests/Public/PublicApiTests.cs).

In all of the examples below you can call /free/(method) calls with /free0/ up to /free9/ to increase the given limits above, a simple way is to either rotate from 1 to 9 or just randomize the free call from 1 to 9.

### Server Time
Returns the server time in ticks.

> `http://31.172.83.181:8080/free/time`

Note: You can do the same in the [Private API via getservertime](../Private-API#getservertime-2)

### Markets
Returns JSON encoded list of markets that apply to the given filter.

> `http://31.172.83.181:8080/free/markets/JSON-ENCODED-MARKETFILTER`


MARKETFILTER object looks like this:

```json
{
        "Cat":0,
        "RunnerAND":["Arsenal","Chelsea"],
        "TitleAND":null,
        "TitleNOT":["Corners","Throwin"],
        "Comp":"Premier League",
        "TypeOR":[0],
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


# API Examples & Source Code

## A0) Access information 

You need to register your IP to access the server. You will receive the IP and port you can connect to.
This is a testserver for general use:  31.172.83.53:18012

This is the public key from the server. All responses must be signed.

```
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC52cTT4XaVIUsmzfDJBP/ZbneO
6qHWFb01oTBYx95+RXwUdQlOAlAg0Gu+Nr8iLqLVbam0GE2OKfrcrSy0mYUCt2Lv
hNMvQqhOUGlnfHSvhJBkZf5mivI7k0VrhQHs1ti8onFkeeOcUmI22d/Tys6aB20N
u6QedpWbubTrtX53KQIDAQAB
-----END PUBLIC KEY-----
```

## A1) Orders

```csharp
    class ReturnMOrder
    {
        UserOrder _UserOrder;
        MatchedOrder _MatchedOrder;
        long _UserUMOrderID;   //the corresponding unmatched order id
    }

    class UserOrder
    {
        int BidOrAsk;
        long MarketID;
        int RunnerID;
        long OrderID;
        string MatchedSubUser;
    }

    class MatchedOrder
    {
        int R;  //internal status
        long ID;  
        MOState State;  //See A2)
        decimal Price;
        decimal Amount;
        int MakerCancelTime;  //Pending Period
    }
```

## A2)  DATA Fields

```csharp
        enum MarketPeriod
        {
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
            THIRD_PERIOD   
        }

        enum StatusType
        {
            ACTIVE,
            INPLAY,
            SUSPENDED,
            CLOSED,
            SETTLED,
            CANCELLED
        }

        enum MarketType
        {
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
        }

        enum SettleType
        {
            BINARY,
            DECIMAL
        }
```

### for matched orders:

```csharp
        enum MOState
        {
            MATCHED,
            RUNNERWON,
            RUNNERHALFWON,
            RUNNERLOST,
            RUNNERHALFLOST,
            MAKERVOIDED,
            VOIDED,
            PENDING,
            DECIMALRESULT
        }
```

### unmatched orders

```csharp
        enum Type
        {
            MAKERTAKER,   
            MAKER,  //will not match with an existing order on the orderbook
            TAKER  //will only match with an existing order on the orderbook, after placement the order is immediately cancelled
        }
```

## Categories

```csharp
        const int SOCCER = 1;
        const int TENNIS = 2;
        const int GOLF = 3;
        const int CRICKET = 4;
        const int RUGBYUNION = 5;
        const int BOXING = 6;
        const int HORSERACING = 7;
        const int MOTORSPORT = 8;
        const int SPECIAL = 10;
        const int RUGBYLEAGUE = 11;
        const int BASKETBALL = 12;
        const int AMERICANFOOTBALL = 13;
        const int BASEBALL = 14;
        const int HOCKEY = 30;
        const int POLITICS = 15;
        const int FINANCIAL = 16;
        const int GREYHOUND = 17;
        const int VOLLEYBALL = 18;
        const int HANDBALL = 19;
        const int DARTS = 20;
        const int BANDY = 21;
        const int WINTERSPORTS = 22;
        const int BOWLS =24;
        const int POOL = 25;
        const int SNOOKER = 26;
        const int TABLETENNIS = 27;
        const int CHESS = 28;
        const int FUN = 31;
        const int ESPORTS = 32;
        const int INPLAY = 33;
        const int RESERVED4 = 34;
        const int MIXEDMARTIALARTS = 35;
        const int RESERVED6 = 36;
        const int RESERVED = 37;
        const int CYCLING = 38;
        const int RESERVED9 = 39;
        const int BITCOIN = 40;
```

## A3) Sample Python code

```python
# -*- coding: utf-8 -*-
# Standard library imports
import socket
import json
import gzip
from StringIO import StringIO
from base64 import b64encode, b64decode
from os.path import join
import time
from decimal import Decimal
from logging import getLogger

# Third party imports
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512

logger = getLogger(__name__)

QUERY_TYPE_MAPPING = {
    "GETPUBLICKEY": "GETPUBLICKEY",
    "GETORDERBOOK": 1,   # market id
    "GETORDERBOOKS": 4,  # Serialized list of long market ids    returns Serialized  Dictionary<long,string>
    "GETSERVERTIME": 2,
    "GETCOMPETITIONS": 3,  # sport category
    "GETMARKET": 6,  # market id
    "GETMARKETS": 7,  # serialized market filter
    "CREATEMARKET": 11,  # serialized market
    "CREATEORDER": 12,  # see example
    "CREATEORDERWITHCANCELTIME": 13,  # See example
    "CREATELAYORDERWITHLIABILITY": 51,  # place lay bet
    "CREATELAYORDERWITHLIABILITYANDCANCELTIME": 51,
    "CANCELORDER": 15,     # MarketID|RunnerID|Unmatched-OrderID
    "CANCELORDERWITHMATCHES": 75,     # MarketID|RunnerID|Unmatched-OrderID
    "CANCELMATCHEDORDER": 9,  # MarketID|RunnerID|Matched-OrderID
    "CONFIRMMATCHEDORDER": 8,  # MarketID|RunnerID|Matched-OrderID
    "CANCELORDERSONMARKET": 10,  # market id
    "CANCELALLORDERS": 16,
    "CHANGEORDER": 17,  # long MarketID|int  RunnerID|long OrderID| decimal Price| decimal amount
    "CHANGEORDERCANCELTIME": 18,  # long MarketID|int  RunnerID|long OrderID| DateTime time
    "REDUCEORDERSTAKE": 19,
    "REGISTER": 20,  # string public key  |  long FundServerID
    "GETME": 21,   # -
    "GETMYBALANCE": 22,
    "GETNEW": 24,  # long time    returns  new UMO, new MO
    "GETNEWSILENT": 30,  # long time    returns  new UMO, new MO
    "GETUNMATCHEDORDERS": 25,  # time     or   time|fromID|toID   for large requests
    "GETMATCHEDORDERS": 27,  # time     or   time|fromID|toID   for large requests
    "SETABSENCECANCELPOLICY": 43,  # ms
    "SETFORCENONCE": 44,  # true or false
    "SETFORCESIGNATURE": 45,  # true or false
    "SETSCREENNAME": 46,  # true or false
    "GETMARKETSORDERBOOK": 67  # serialized market filter
}

CATEGORIES = {
    "SOCCER": 1,
    "TENNIS": 2,
    "GOLF": 3,
    "CRICKET": 4,
    "RUGBYUNION": 5,
    "BOXING": 6,
    "HORSERACING": 7,
    "MOTORSPORT": 8,
    "SPECIAL": 10,
    "RUGBYLEAGUE": 11,
    "BASKETBALL": 12,
    "AMERICANFOOTBALL": 13,
    "BASEBALL": 14,
    "POLITICS": 15,
    # "FINANCIAL": 16,
    # "GREYHOUND": 17,
    # "VOLLEYBALL": 18,
    # "HANDBALL": 19,
    # "DARTS": 20,
    # "BANDY": 21,
    # "WINTERSPORTS": 22,
    # "BOWLS": 24,
    # "POOL": 25,
    # "SNOOKER": 26,
    # "TABLETENNIS": 27,
    # "CHESS": 28,
    "HOCKEY": 30,
    "FUN": 31,
    "ESPORTS": 32,
    "MixedMartialArts": 35,
    "reserved8": 38,  # cycling
}

ORDER_TYPES = {
    "MAKERTAKER": 0,
    "MAKER": 1,
    "TAKER": 2
}

CLIENT_ID = settings.CLIENT_ID
SPORT_BETS_SERVER_IP = "31.172.83.53"
SPORT_BETS_SERVER_PORT = 18012

def create_json_query(comp=None, min_pop=None, no_zombie=None, only_active=None, cat=None, from_id=None, to_id=None,
                      runner_and=None, title=None, type_or=None, period_or=None, to_settle=None,
                      only_my_created_markets=None, changed_after=None, from_close_t=None, to_close_t=None):
    json_dict = {}
    if comp:
        json_dict["Comp"] = comp
    if min_pop:
        json_dict["MinPop"] = min_pop
    if no_zombie:
        json_dict["NoZombie"] = no_zombie
    if only_active:
        json_dict["OnlyActive"] = only_active
    if cat:
        json_dict["Cat"] = cat
    if from_id:
        json_dict["FromID"] = from_id
    if to_id:
        json_dict["ToID"] = to_id
    if runner_and:
        json_dict["RunnerAND"] = runner_and
    if title:
        json_dict["Title"] = title
    if type_or:
        json_dict["TypeOR"] = type_or
    if period_or:
        json_dict["PeriodOR"] = period_or
    if to_settle:
        json_dict["ToSettle"] = to_settle
    if only_my_created_markets:
        json_dict["OnlyMyCreatedMarkets"] = only_my_created_markets
    if changed_after:
        json_dict["ChangedAfter"] = changed_after
    if from_close_t:
        json_dict["FromClosT"] = from_close_t
    if to_close_t:
        json_dict["ToClosT"] = to_close_t
    return json.dumps(json_dict)

def get_message_signature(message):
    private_key_dir = join(settings.SPORT_BETS_KEY_PATH, "private_key.txt")
    private_key = open(private_key_dir, "r").read()
    rsa_key = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(rsa_key)
    digest = SHA512.new()
    digest.update(message)
    sign = signer.sign(digest)
    return b64encode(sign)

def verify_message(message):
    if message.find('|') == -1:
        return True
    signed_message = message[:message.find('|')]
    original_message = message[message.find('|')+1:]
    public_key_dir = join(settings.SPORT_BETS_KEY_PATH, "public_key.txt")
    public_key = open(public_key_dir, "r").read()
    rsa_key = RSA.importKey(public_key)
    signer = PKCS1_v1_5.new(rsa_key)
    digest = SHA512.new()
    digest.update(original_message)
    if signer.verify(digest, b64decode(signed_message + "=" * ((4 - len(signed_message) % 4) % 4))):
        return True
    return False

def send_request(message, signed=False, tries=0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SPORT_BETS_SERVER_IP, SPORT_BETS_SERVER_PORT))
        message_signature = ''
        if signed:
            message_signature = get_message_signature(message)
        message_to_send = '{}|{}<ENDOFDATA>'.format(message_signature, message)
        s.send(message_to_send)
        data = ""
        while True:
            new_data = s.recv(4096)
            if not new_data:
                break
            data += new_data
        s.close()
        result = gzip.GzipFile(fileobj=StringIO(data)).read()
        if not verify_message(result):
            raise ValueError
        return result
    except (socket.timeout, socket.error) as e:        
        if tries < 3:
            return send_request(message, signed, tries + 1)
        else:
                 pass

def get_public_key():
    request_no = 0
    query_type = QUERY_TYPE_MAPPING["GETPUBLICKEY"]
    message = "{}|{}|{}".format(request_no, CLIENT_ID, query_type)
    result = send_request(message, signed=True)
    return result

def get_balance():
    request_no = 0
    query_type = QUERY_TYPE_MAPPING["GETMYBALANCE"]
    message = "{}|{}|{}".format(request_no, CLIENT_ID, query_type)
    result = send_request(message, signed=True)
    balance = result.split('|')[-1]
    try:
        return json.loads(balance)
    except ValueError:
        logger.info(u'Not able to parse response: {}'.format(balance))

def fetch_single_event_odds(event_id):
    request_no = 0
    query_type = QUERY_TYPE_MAPPING["GETORDERBOOK"]
    message = "{}|{}|{}|{}".format(request_no, CLIENT_ID, query_type, event_id)
    result = send_request(message, signed=True)
    order_books_json = result.split('|')[-1]
    if not ('Bids' in order_books_json or 'Asks' in order_books_json):
        return []
    order_books_json = order_books_json.strip('~') if order_books_json else None
    odds = []
    return

def fetch_sport_events():
    request_no = 0
    query_type = QUERY_TYPE_MAPPING["GETMARKETS"]
    events_list = []
    for category_name, category_id in CATEGORIES.iteritems():
        from_id = 0
        events = []
        while True:
            json_query = create_json_query(no_zombie=True,
                                           only_active=True,
                                           cat=category_id,
                                           from_id=from_id,
                                           to_id=from_id+300,
                                           min_pop=MIN_POP_DICT.get(category_name, None))
            message = "{}|{}|{}|{}".format(request_no, CLIENT_ID, query_type, json_query)
            result = send_request(message)
            try:
                new_events = json.loads(result.split("|")[-1])
            except ValueError:
                break
            events += new_events
            if len(new_events) < 300:
                break
            from_id += 300
    return events_list

def update_matches(latest_matched_bet_id, unresolved_events, sport_event_id=None):
    request_no = 0
    query_type = QUERY_TYPE_MAPPING["GETMATCHEDORDERS"]
    timestamp = 1420070400L
    from_id = 0
    new_matched_bets = []
    new_resolved_events = []
    voided_events = set()
    all_new_matches_checked = False
    while True:
        if sport_event_id:
            message = "{}|{}|{}|{}|{}".format(request_no, CLIENT_ID, query_type, timestamp, sport_event_id)
        else:
            message = "{}|{}|{}|{}|{}|{}".format(request_no, CLIENT_ID, query_type, timestamp, from_id, from_id+300)
        result = send_request(message, signed=True)
        matches = json.loads(result.split("|")[-1])
       
def can_sport_bet_be_placed(sport_event_id, sport_bet_outcome_id, outcome_type, odds, amount, maker=False):
    request_no = int(time.time())
    query_type = QUERY_TYPE_MAPPING["CREATEORDER" if outcome_type == 'back' else "CREATELAYORDERWITHLIABILITY"]
    back_or_lay = 1 if outcome_type == "back" else 0
    user_name = "fairlay"
    order_type = ORDER_TYPES["MAKERTAKER"] if not maker else ORDER_TYPES['MAKER']
    message = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(request_no, CLIENT_ID, query_type,
                                                     sport_event_id, sport_bet_outcome_id, back_or_lay, odds,
                                                     amount * 1000, order_type, user_name)
    try:
        response = send_request(message, signed=True)
    except RequestFailed:
        return False
    logger.debug(u'--- can_sport_bet_be_placed ---')
    logger.debug(u'message -> {}'.format(message))
    logger.debug(u'response -> {}'.format(response))
    result = response.split("|")[-1]

def can_cancel_order(sport_event_id, sport_bet_outcome_id, sport_bet_order_id):
    request_no = 0
    query_type = QUERY_TYPE_MAPPING["CANCELORDERWITHMATCHES"]
    message = "{}|{}|{}|{}|{}|{}".format(request_no, CLIENT_ID, query_type,
                                         sport_event_id, sport_bet_outcome_id, sport_bet_order_id)
    response = send_request(message, signed=True)
    try:
        pass
    except ValueError:
        reason = response.split('|')[-1]
        if reason.startswith(('Order does not exist', 'XError: Market Closed', 'XError: Market does not exist')):
            logger.info(u'Reason: {}'.format(reason))
            can_be_cancelled = True
        else:
            can_be_cancelled = False

def update_odds():
    request_no = 0
    query_type = QUERY_TYPE_MAPPING["GETMARKETSORDERBOOK"]
    from_id = 0
    orders = []
    while True:
        json_filter = create_json_query(from_id=from_id, to_id=from_id+300, only_active=True)
        message = "{}|{}|{}|{}".format(request_no, CLIENT_ID, query_type, json_filter)
        result = send_request(message, signed=True)
       
        if len(new_orders.keys()) < 300:
            break
        from_id += 300
```
