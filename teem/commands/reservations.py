from .base import Base
from utilities import authenticate
import requests
import datetime

class reservations(Base):
    """Make 'get reservations' function calls to Teem
        with parameters passed via CLI"""
    Rooms = {
        'showcase': 130700,
        'pistachio': 218764,
        'almond': 218763,
        '22-91': 219151,
        '22-92': 219152,
        '22-93': 219153,
        'toronto': 135254,
        'test room': 167492,
        'techbar': 177863,
        'tower a lobby': 77522        
        }

    def get_reservations(access_token, reservation_id=None, parameters={}):
        """
        Returns a dictionary of all reservations, a sigle reservation or the
        reservations of a single room depending on the input parameters
        @ Parameter - 'access_token' - Teem access token
        @ Parameter - 'reseration_id' - Id of an individual reservation
        @ Parameter - 'parameters' - dictionary of values to modify results
            of get_reservations api call. Visible in Teem API documentation.
        """
        print(parameters)
        reservations = 'calendars/reservations/'
        base_url = 'https://app.teem.com/api/v4/'
        nulls = ['null', 'None', None]
        if reservation_id in nulls:
            url = base_url + reservations
            
        else:
            url = base_url + reservations + str(reservation_id) + '/'
            
        headers = {'Authorization': 'Bearer ' + access_token}
        
        try:
            r = requests.get(url, params=parameters, headers=headers)
        except Exception as e:
            raise e
        #print(r.status_code)
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

    def prompt(parameters):
        print("Received the following options from command line", parameters)
        if parameters['loop']:
            verb = 'Looping through'
        else:
            verb = 'Getting'
        if parameters['room']:
            room = parameters['room']
        else:
            room = 'all rooms'
        if parameters['before']:
            before = f"from {parameters['before']}"
        else:
            before = 'the beginning of time'
        if parameters['after']:
            after = f"until {parameters['after']}"
        else:
            after = 'until the end of time'
        print(f"{verb} reservations for {room} {before} {after}")

    def map_rooms(self, room_name):
        return self.Rooms[room_name.lower()]
        
    def run(self, parameters):
        if parameters['verbose']:
            self.prompt(parameters)
        if parameters['room'] is not None:
            parameters['room_id'] = self.map_rooms(self, parameters.pop('room'))
##        if parameters['before'] or parameters['after'] is not None:
            
        try:
            creds = authenticate.load_credentials()
            tokens = authenticate.obtain_token(creds['teem_access_key_id'],
                                               creds['teem_secret_access_key'],
                                               creds['teem_username'],
                                               creds['teem_password'],
                                               'https://app.teem.com/oauth/token/',
                                               ['users', 'reservations', 'accounts'])
        except Exception as e:
            raise e
        
        if parameters['loop']:
            while True:
                try:        
                    response = self.get_reservations(tokens['access_token'],
                                                parameters['reservation'],
                                                parameters)
                except Exception as e:
                    raise e
                else:
                    if response['meta']['filtered_total'] >= 1:
                        self.print_reservations(response['reservations'])
                    else:
                        break
                        print("No reservations to show with the current filters")
        else:
            try:        
                response = self.get_reservations(tokens['access_token'],
                                            parameters['reservation'],
                                            parameters)
            except Exception as e:
                raise e
            else:
                if response['meta']['filtered_total'] >= 1:
                    self.print_reservations(response['reservations'])
                else:
                    print("No reservations to show with the current filters")
            
        
    def print_reservations(reservations, info=[]):
        interesting = ['room_id','title',
                       'creator','id',
                       'participant_ids','checked_in']
        if not info:
            info = interesting
        for event in reservations:
            for item in info:
                if item == 'creator':
                    try:
                        print(event[item]['first_name'])
                    except TypeError:
                        pass
                elif item == 'checked_in':
                    try:
                        print(item, convert_time(event[item]))
                    except TypeError:
                        print(item)
                else:
                    print(item, event[item])
            print("Starts: {}, Ends: {}".format(convert_time(event['starts_at']),
                                                  convert_time(event['ends_at'])))  

def convert_time(time_stamp):
    return datetime.datetime.fromtimestamp(int(time_stamp)).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    res = reservations(room='Showcase', loop=True, before='10:30')
    res.run()
    res.args
    
              
