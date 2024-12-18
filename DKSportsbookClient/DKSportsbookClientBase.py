import requests
import re
import json
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class Extraction:
    pattern: re.Pattern
    extracted: bool = False

class DKSportsbookClientBase:
    _initialized = False
    _http_client = requests.Session()

    site_experience = None
    sports_content_base_url = None
    sports = None

    EXTRACTS = {
        'initial_state': Extraction(r'(?<=window.__INITIAL_STATE__ = )(.*)(?=;[\r\n])'),
        'product_config': Extraction(r'(?<=window.__productConfig = )(.*)(?=;[\r\n])')
    }

    @staticmethod
    def _initialize() -> None:
        """ Initialize base class members to be shared amongst all child classes """

        # Set up requests session object for re-usability throughout the entire dependency chain
        DKSportsbookClientBase._http_client.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Referer": "https://sportsbook.draftkings.com/",
            "Origin": "https://sportsbook.draftkings.com",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Priority": "u=1, i",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Site": "same-site"
        }

        # Use HTTP client to load DraftKings Sportsbook homepage HTML and parse out the interesting bits for use later
        soup = BeautifulSoup(DKSportsbookClientBase._http_client.get('https://sportsbook.draftkings.com').text, 'lxml')
        for element in soup.find_all('script'):
            for key in [key for key in DKSportsbookClientBase.EXTRACTS.keys() if not DKSportsbookClientBase.EXTRACTS[key].extracted]:
                pattern = DKSportsbookClientBase.EXTRACTS[key].pattern
                if match := re.search(pattern, element.get_text()):
                    match = json.loads(match.group(0))
                    if key == 'initial_state':
                        DKSportsbookClientBase.site_experience = match['user']['siteExperience']
                        DKSportsbookClientBase.sports = match['sports']['data']
                        pass
                    elif key == 'product_config':
                        DKSportsbookClientBase.sports_content_base_url = match['sportsContentBff']
                    
                    DKSportsbookClientBase.EXTRACTS[key].extracted = True

            # Stop looking through <script> nodes in the homepage HTML if we've hit all our extraction logic already
            if len([_ for _ in DKSportsbookClientBase.EXTRACTS.values() if not _.extracted]) == 0:
                break

        DKSportsbookClientBase._initialized = True