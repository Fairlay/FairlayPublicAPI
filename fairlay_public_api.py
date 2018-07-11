import json
import socket
import time
import datetime
import requests

def convert_ticks_to_datetime(s):
    return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=int(s)/10)

class FairlayPythonPublic(object):

    MARKET_CATEGORY = {
        1: 'Soccer',
        2: 'Tenis',
        3: 'Golf',
        4: 'Cricket',
        5: 'RugbyUnion',
        6: 'Boxing',
        7: 'Horse Racing',
        8: 'Motorsport',
        10: 'Special',
        11: 'Rugby League',
        12: 'Bascketball',
        13: 'American Football',
        14: 'Baseball',
        15: 'Politics',
        16: 'Financial',
        17: 'Greyhound',
        18: 'Volleyball',
        19: 'Handball',
        20: 'Darts',
        21: 'Bandy',
        22: 'Winter Sports',
        24: 'Bowls',
        25: 'Pool',
        26: 'Snooker',
        27: 'Table tennis',
        28: 'Chess',
        30: 'Hockey',
        31: 'Fun',
        32: 'eSports',
        33: 'Inplay',
        34: 'reserved4',
        35: 'Mixed Martial Arts',
        36: 'reserved6',
        37: 'reserved',
        38: 'Cycling',
        39: 'reserved9',
        40: 'Bitcoin',
        42: 'Badminton'
    }

    MARKET_TYPE = {
        0: 'MONEYLINE',
        1: 'OVER_UNDER',
        2: 'OUTRIGHT',
        3: 'GAMESPREAD',
        4: 'SETSPREAD',
        5: 'CORRECT_SCORE',
        6: 'FUTURE',
        7: 'BASICPREDICTION',
        8: 'RESERVED2',
        9: 'RESERVED3',
        10: 'RESERVED4',
        11: 'RESERVED5',
        12: 'RESERVED6'
    }

    MARKET_PERIOD = {
        0: 'UNDEFINED',
        1: 'FT',
        2: 'FIRST_SET',
        3: 'SECOND_SET',
        4: 'THIRD_SET',
        5: 'FOURTH_SET',
        6: 'FIFTH_SET',
        7: 'FIRST_HALF',
        8: 'SECOND_HALF',
        9: 'FIRST_QUARTER',
        10: 'SECOND_QUARTER',
        11: 'THIRD_QUARTER',
        12: 'FOURTH_QUARTER',
        13: 'FIRST_PERIOD',
        14: 'SECOND_PERIOD',
        15: 'THIRD_PERIOD',
    }

    MARKET_SETTLEMENT = {
        0: 'BINARY',
        1: 'DECIMAL',
        2: 'CFD',
        3: 'EXCHANGE'
    }

    MATCHED_ORDER_STATE = {
        0: 'MATCHED',
        1: 'RUNNER_WON',
        2: 'RUNNER_HALFWON',
        3: 'RUNNER_LOST',
        4: 'RUNNER_HALFLOST',
        5: 'MAKERVOIDED',
        6: 'VOIDED',
        7: 'PENDING',
        8: 'DECIMAL_RESULT'
    }

    UNMATCHED_ORDER_STATE = {
        0: 'ACTIVE',
        1: 'CANCELLED',
        2: 'MATCHED',
        3: 'MATCHEDANDCANCELLED'
    }

    ORDER_TYPE = {
        0: 'MAKERTAKER',
        1: 'MAKER',
        2: 'TAKER'
    }

    def __init__(self):
        super(FairlayPythonPublic, self).__init__()
        self.__last_time_check = None
        self.__offset = None

    def __parse_market(self, market):
        print(market['Title'])
        market['MarketCategory'] = self.MARKET_CATEGORY[market['CatID']]
        market['MarketType'] = self.MARKET_TYPE[market['_Type']]
        market['MarketPeriod'] = self.MARKET_PERIOD[market['_Period']]
        market['SettlementType'] = self.MARKET_SETTLEMENT[market['SettlT']]
        if market['OrdBStr']:
            market['OrdBJSON'] = [json.loads(ob) for ob in market['OrdBStr'].split('~') if ob]

    def __public_request(self, endpoint, json=True, tries=0):

        try:
            response = requests.get('http://31.172.83.181:8080/free/' + endpoint)
            
            if response == 'XError: Service unavailable':
                raise requests.exceptions.ConnectionError

            if 'XError' in response.text:
                return

            if json:
                return response.json()
            else:
                return response

        except requests.exceptions.ConnectionError:
            time.sleep(6)
            if tries >= 3:
                raise requests.exceptions.ConnectionError
            return self.__public_request(endpoint, json, tries + 1)

    def get_server_time(self):
        try:
            response = self.__public_request('time')
            if not response:
                raise ValueError
            return response
        except Exception:
            return []

    def get_markets_and_odds(self, market_filter={}, changed_after=datetime.datetime(2015, 1, 1)):
        '''
            Free Public API for retrieving markets and odds. 
            More details at: https://github.com/Fairlay/FairlayPublicAPI

            market_filter: dictionary
            change_after: datetime

        Response: dictionary
            E.g. {'Ru': [{'RedA': 0.0, 'VisDelay': 3000, 'Name': 'Yes', 'VolMatched': 0.0},
                        {'RedA': 0.0, 'VisDelay': 3000, 'Name': 'No', 'VolMatched': 0.0}],
                'LastSoftCh': '2015-11-30T00:50:09.2443208Z', 'Descr': 'This market resolves to ...',
                'Title': 'Will OKCoin lose customer funds in 2016?', 'OrdBStr': '~', 'MarketCategory': 'Bitcoin',
                'Status': 0, '_Type': 2, 'CatID': 40, 'LastCh': '2015-10-30T06:05:00.7541435Z',
                'Comp': 'Bad News', 'MarketType': 'MONEYLINE', 'OrdBJSON': [], 'Comm': 0.02,
                'ClosD': '2016-10-01T00:00:00', 'Margin': 10000.0, 'ID': 57650700754, 'MaxVal': 0.0,
                'SettlT': 0, 'MinVal': 0.0, 'CreatorName': 'FairMM', 'Pop': 0.0, 'MarketPeriod': 'FIRST_SET',
                'SettlD': '2017-01-01T00:00:00', '_Period': 1, 'SettlementType': 'BINARY'}
        '''

        if not self.__last_time_check or self.__last_time_check + datetime.timedelta(minutes=10) < datetime.datetime.now():
            try:
                response = self.__public_request('time')
                if not response:
                    raise ValueError
            except Exception:
                return []

            self.__offset = datetime.datetime.now() - convert_ticks_to_datetime(response)
            self.__last_time_check = datetime.datetime.now()

        changed = changed_after - datetime.timedelta(seconds=10) - self.__offset
        filters = {'SoftChangedAfter': changed.isoformat()}
        filters.update(market_filter)
        try:
            response = self.__public_request('markets/{}'.format(json.dumps(filters)))
        except ValueError:
            return []

        for market in response:
            self.__parse_market(market)
        return response

    def get_competitions(self, categoryID):
        try:
            response = self.__public_request('comps/{}'.format(categoryID))
        except ValueError:
            return []

        return response