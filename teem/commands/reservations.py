from .base import Base
from utilities import authenticate
import requests


class reservations(Base):
    """Make 'get reservations' function calls to Teem
        with parameters passed via CLI"""

    def get_reservations(access_token, reservation_id=None, parameters={}):
        """
        Returns a dictionary of all reservations, a sigle reservation or the
        reservations of a single room depending on the input parameters
        @ Parameter - 'access_token' - Teem access token
        @ Parameter - 'reseration_id' - Id of an individual reservation
        @ Parameter - 'parameters' - dictionary of values to modify results
            of get_reservations api call. Visible in Teem API documentation.
        """
        reservations = 'calendars/reservations/'
        base_url = 'https://app.teem.com/api/v4/'
        nulls = ['null', 'None', None]
        if reservation_id in nulls:
            url = base_url + reservations
            parameters = parameters
        else:
            url = base_url + reservations + str(reservation_id) + '/'
            
        headers = {'Authorization': 'Bearer ' + access_token}
        
        try:
            r = requests.get(url, params=parameters, headers=headers)
        except Exception as e:
            raise e
        print(r.status_code)
        r.raise_for_status()
        data = r.json()
        response = {}
        try:
            response['reservations'] = data['reservations']
            response['meta'] = data['meta']
        except KeyError as e:
            print("No Meta")
            try:
                response['reservations'] = []
                response['reservations'].append(data['reservation'])
            except KeyError as e:
                raise e
        
        return response
    
    def run(self, some_dict):
        print("Received the following options from command line", some_dict)


if __name__ == '__main__':
    res = reservations(room='Showcase', loop=True, before='10:30')
    res.run()
    res.args
    
              
