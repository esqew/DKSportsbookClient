import requests
from typing import Union

class DKSportsbookClient:
    BASE_URL = r'https://sportsbook-nash-usma.draftkings.com/sites/{}/api/{}/{}/{}/{}'
    LEAGUES = {
        'NFL': 88808,
        'NBA': 42648,
        'NCAAM': 92483,
        'NCAAW': 36647,
        'NHL': 42133,
    }
    def __init__(self, **kwargs) -> None:
        if not 'location_code' in kwargs or not kwargs['location_code']:
            self.location_code = DKSportsbookClient.get_locations()['location'] + '-SB'
        else:
            self.location_code = kwargs['location_code']
        return

    @staticmethod
    def get_locations() -> dict:
        return DKSportsbookClient.__get_json(r'https://api.draftkings.com/geolocations/v1/locations.json')
    
    @staticmethod
    def __get(*args, **kwargs) -> Union[dict, list, str]:
        url = args[0]
        if 'raw' in kwargs and kwargs['raw']:
            return DKSportsbookClient.__get_raw(url)
        else:
            return DKSportsbookClient.__get_json(url)
    
    @staticmethod
    def __get_raw(url) -> str:
        return requests.get(url).raw
    
    @staticmethod
    def __get_json(url) -> Union[dict, list]:
        response = requests.get(url)
        try:
            return response.json()
        except Exception as e:
            raise Exception(f'Could not parse response as JSON (response was: {response.status_code}: {response.text})')

    @staticmethod
    def __format_url(location_code: str, api_version: str = 'v5', service: str = 'eventgroups', id: int = 42648, relative_url: str = '') -> str:
        return DKSportsbookClient.BASE_URL.format(location_code, api_version, service, id, relative_url)

    def get_event_group(self, event_group_id, **kwargs) -> dict:
        url = DKSportsbookClient.__format_url(self.location_code, api_version='v5', service='eventgroups', id=event_group_id)
        return DKSportsbookClient.__get(url, **kwargs)
    
    def get_category_for_event_group(self, event_group_id, category_id, **kwargs) -> list:
        url = DKSportsbookClient.__format_url(self.location_code, api_version='v5', service='eventgroups', id=event_group_id, relative_url=f'/categories/{category_id}')
        response = DKSportsbookClient.__get(url, **kwargs)
        return next((category for category in response['eventGroup']['offerCategories'] if category['offerCategoryId'] == category_id), None)
    
    def get_subcategory_for_event_group(self, event_group_id: int, category_id: int, subcategory_id: int):
        url = DKSportsbookClient.__format_url(self.location_code, api_version='v5', service='eventgroups', id=event_group_id, relative_url=f'/categories/{category_id}/subcategories/{subcategory_id}')
        response = DKSportsbookClient.__get(url)['eventGroup']['offerCategories']
        category = next((category for category in response if category['offerCategoryId'] == category_id), None)
        subcategory = next((subcategory for subcategory in category['offerSubcategoryDescriptors'] if subcategory['subcategoryId'] == subcategory_id), None)
        return subcategory['offerSubcategory']