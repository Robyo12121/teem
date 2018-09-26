import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import datetime
import time
import random
import json
import sys
import configparser

class Teem():
    
    client_id = 'fI5X1eXUX2sHVmuiYtiK2VMmhmbBIEXJblt71vRt'
    client_secret = 'dvWTAJK5GDh8Aw2ZuwFLz6ITQjBQITEPypqo5evMIRhdO24DpcOxxBy8DyKy730rwxzx3WUXP7wbR85wKRwkokbnyuSje0BK073z0URmIcQfMqTamnxVpEd4iVR2cp96'
    base_url = 'https://app.teem.com/api/v4/'
    #auth_url = 'https://app.teem.com/oauth/authorize/'
    token_url= 'https://app.teem.com/oauth/token/'
    #redirect_uri = 'https://www.google.com'
    #OAuth = auth_url + '?' + client_id + '&redirect_uri=' + redirect_uri+ '/callback&response_type=code&scope=users'
    scope = ['users', 'reservations', 'accounts']
    # Legacy resource owner password credentials
    # myexperienceshowcase
    username = 'myexperienceshowcase@gmail.com'
    password = 'myexperienceshowcase'
    config_file = '/data/Teem.ini'
    # Endpoints
    # Rooms
    # Get
    rooms = 'deployment/rooms/'
    users = 'accounts/users/'
    frequently_booked = '/frequently-booked/'
    uri_checkin = '/checkin/'
    # Calendars
    # Get
    reservations = 'calendars/reservations/'
    events = []

    def __init__(self, token=None):
        self.config = configparser.ConfigParser()
        self.creds = self.config.read(self.config_file)
        self.token = token
        if self.token == None:
            print('No token. Obtaining')
            self.obtain_token(self.client_id, self.token_url,
                                           self.username, self.password,
                                           self.client_secret)

        self.default_headers = {
            'Authorization': 'Bearer '+ self.token
            }
            
    def obtain_token(self, client_id, token_url, username, password, client_secret):
        oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id, scope=self.scope))
        token = oauth.fetch_token(token_url=token_url,
                              username=username,
                              password=password,
                              client_id=client_id,
                              client_secret=client_secret)
        print(token)
        self.token = token['access_token']
        print(self.token)
        self.refresh_token = token['refresh_token']
        print(self.refresh_token)
        self.token_valid = True

    def verify_token(self, token):
        url = self.base_url + self.rooms
        headers = {
            'Authorization': 'Bearer '+ token
            }
        r = requests.get(url, headers=headers)        
        if r.status_code in range(200, 206):
            return True
        elif r.status_code in range(400, 430):
            return False
        else:
            return False

##    def read_creds(self, file):
##        self.config.read(file)
##        creds = config['app.teem.com']
##        return dict(creds)
##
##    def write_creds(self, file, some_dict):
##        with open(self.config_file, 'w') as cfg:
##            self.config.write(
        
        
    def refresh(self):
        url = self.token_url
        payload = {'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'grant_type': 'refresh_token',
                   'refresh_token': self.refresh_token
                   }
        r = requests.post(url, params=payload)
        r.raise_for_status()
        response = r.json()
        self.token = response['access_token']
        self.refresh_token = response['refresh_token']
        print("Token refreshed! New token {} expires in {} seconds".format(response['access_token'],response['expires_in']))

    def get_rooms(self, room_id = None):
        '''return a list of all spaces'''
        if room_id is None:
            url = self.base_url + self.rooms

        else:
            url = self.base_url + self.rooms + str(room_id) + '/'
        payload = {'per_page':100}
        r = requests.get(url, params=payload, headers=self.default_headers)
        r.raise_for_status()
        data = r.json()
        rooms = data['rooms']
        return rooms

    def get_users(self, parameters=None):
        '''return a list of all users'''
        url = self.base_url + self.users
        payload = parameters
        r = requests.get(url, params=payload, headers=self.default_headers)
        r.raise_for_status()
        data = r.json()
        users = data['users']
        return users

    def get_reservations(self, reservation_id = None, parameters={}):
        if reservation_id is None:
            url = self.base_url + self.reservations
        else:
            url = self.base_url + self.reservations + str(reservation_id) + '/'
##            parameters = {
##                'room_id': room_id
##                }
        r = requests.get(url, params=parameters,headers = self.default_headers)
        r.raise_for_status()
        data = r.json()
        response = {}
        try:
            response['reservations'] = data['reservations']
            response['meta'] = data['meta']
        except KeyError:
            try:
                response['reservations'] = data['reservation']
                return response
            except Exception as e:
                raise e
        
        else:
            return response

    def list_rooms(self, rooms):
        for room in rooms:
            print(room['name'], room['id'])

    #def make_reservation(self, room_id, title='Robin-testing', participants=[], dur_mins = 30):
    def make_reservation(self, room_id, payload={}):
        param_payload = {"room_id": room_id}
        print(param_payload)
        body_payload = payload
        print(body_payload)
        url = self.base_url + self.reservations
        print(url)
        r = requests.post(url, params=param_payload, json=body_payload, headers=self.default_headers)
        r.raise_for_status()
        print(r.status_code)
        resp = r.json()
##        event_id = resp['reservation']['id']
##        self.events.append({'title':resp['reservation']['title'],
##                                 'event_id': event_id}) 
        return resp

       

    def delete_reservation(self, event_id):
        url = self.base_url + self.reservations + str(event_id) + '/'
        print(url)
        payload = {'id': event_id}
        body = {"reservations": {}}
        
        r = requests.delete(url, headers=self.default_headers)
        r.raise_for_status()
        print(r.status_code)
        return r.status_code

    def checkin(self, event_id):
        url = self.base_url + self.reservations + str(event_id) + self.uri_checkin
        print(url)
        r = requests.post(url, headers=self.default_headers)
        r.raise_for_status()
        return r.status_code

    def create_change(self, event_id, change_type, reason="null"):
        url = self.base_url + self.reservations + str(event_id) + '/changes/'
        print(url)
        payload = {'type': change_type,
                   'reason': reason}
        r = requests.post(url, params=payload,headers=self.default_headers)
        r.raise_for_status()
        print(r.status_code)
        return r.status_code

    def patch_res(self, event_id, details={}):
        if event_id is None:
            raise Exception("No reservation id given, Nonetype, exiting...")
        elif details is None or details == {}:
            raise Exception("No change details given, exiting...")
        
        url = self.base_url + self.reservations + str(event_id) + '/'
        print(url)
        r = requests.patch(url, json=details, headers=self.default_headers)
        r.raise_for_status()
        
        return r.status_code
    
def convert_time(time_stamp):
    return datetime.datetime.fromtimestamp(int(time_stamp)).strftime('%Y-%m-%d %H:%M:%S')

def print_users(users):
    for user in users:
        print(user['id'], user['first_name'], user['last_name'])

def print_reservations(reservations, info=[]):
    #interesting = ['room_id', 'title', 'creator','id']
    for event in reservations:
        print()
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
            

        print("Starts: {0}, Ends: {1}".format(convert_time(event['starts_at']),
                                              convert_time(event['ends_at'])))

def reverse_list(some_list):
    """A dumb list reverse function.
    Doesn't check any times. Assumes reservations are stored
    earliest first"""
    return some_list[::-1]

def get_closest(reservation_list):
    """
    Returns the closest reservation to the current time from a
    list of reservations
    """
    now = time.time()
    closest = None
    min_diff = 999999999999
    for event in reservation_list:
        diff = event['starts_at'] - now
        if diff > 0 and diff < min_diff:
            closest = event
            min_diff = diff
        else:
            pass
    return closest     
    

#Showcase Room ID: 130700
#PISTACHIO Room ID: 218764
#RoomBookingBot User ID: 1884037

Data = {
        'Rooms': {
            'Showcase': 130700,
            'Pistachio': 218764,
            'Almond': 218763,
            '22-91': 219151,
            '22-92': 219152,
            '22-93': 219153,
            'Toronto': 135254,
            },
        'Users': 
            {
                'RoomBookingBot': 1884037
                }
        }
def create_time(mins, direction):
    mins = int(mins) 
    now = time.time()
    now_dt = datetime.datetime.fromtimestamp(now)
    mins = datetime.timedelta(minutes=mins)
    if direction == '-':
        mins_ago = now_dt - mins
        unix_mins_ago = time.mktime(mins_ago.timetuple())
        return unix_mins_ago, now    
    elif direction == '+':
        mins_ahead = now_dt + mins
        unix_mins_ahead = time.mktime(mins_ahead.timetuple())
        return unix_mins_ahead, now
    else:
        print("Bad. Direction")

def get_input():
    start = int(input("Start in ? minutes: "))
    duration = int(input("Meeting duration: "))
    title = str(input("Meeting name: "))
    space = str(input("Meeting room name format(XX-XX): "))
    space = space.lower()
    space = space[0].capitalize() + space[1:]
    print(space)
    return start, duration, title, space

def make_meeting(start, duration, title, space):
    dur_mins = datetime.timedelta(minutes=duration)
    start_in = datetime.timedelta(minutes=start) #+ offset
    now = datetime.datetime.now()
    start = now + start_in
    end = start + dur_mins
    start_u = time.mktime(start.timetuple())
    end_u = time.mktime(end.timetuple())
        
    payload = {"reservation":{
            "id": random.randint(0,2000),
            "title": title,
            "ends_at": int(end_u),
            "starts_at": int(start_u),
            "room_id": Data['Rooms'][space],
            "participant_ids": Data['Users']['RoomBookingBot']
            }}
    return payload, space


##def main():
##    teem = Teem('RvFMJHDpOMVa8hgdt531h6eYeLBbwe')
            
if __name__ == '__main__':
    teem = Teem('mKk12ZzQiaZTXG91ol7LXciGeBuSWn')

    # GET
##    now = time.time()
    #params = {'range_start_at': now}
    
##    params = {'room_id': 218764}   
##    response = teem.get_reservations(parameters=params)
##    print_reservations(response['reservations'], ['room_id','title', 'creator','id',
##                                                  'participant_ids',
##                                                  'checked_in'])
    # ROOMS
##    rooms = teem.get_rooms()
##    teem.list_rooms(rooms)
    #teem.refresh()
    # USERS
    #parameters = {'search': 'RoomBookingBot'}
    #users = teem.get_users(parameters)
##    users = teem.get_users()
##    print_users(users)
    
    # POST
    # RESERVATION
##    details = {
##        'reservation': {
##            'id': 1148,
##            'title': 'robin extend test 2',
##            'ends_at': 1535954735,
##            'starts_at': 1535954435,
##            'room_id': 218764,
##            'participant_ids': 1884037
##            }
##        }

##    start, duration, title, space = get_input()
##    payload, space = make_meeting(start, duration, title, space)
##    myevent = teem.make_reservation(Data['Rooms'][space], payload=payload)

##    mychange = teem.patch_res(1884037, details=payload)

    while True:
        print("----------------------------------")
        checkFrom, now = create_time(2, '-')
        checkUntil, now2 = create_time(30, '+')
        params = {"range_start_at": int(checkFrom),
                  "range_end_at": int(checkUntil)
                  #"room_id": Data['Rooms']['22-91']
                  }
        response = teem.get_reservations(parameters=params)
        if len(response) < 1:
            print("Nothing to print")
        else:
            print_reservations(response['reservations'], ['room_id','title', 'creator','id',
                                                      'participant_ids',
                                                      'checked_in'])

        print()
        print("Now: {}".format(datetime.datetime.now()))
        time.sleep(20)


    #print_reservations(reservations)    
##    result = teem.delete_reservation(218999436)
##    print(result)
##    #print(teem.checkin(213418237))

##    resp = teem.create_change(213618221, 'cancellation-no-checkin', 'cos')

    # POST PROCCESSING
    #closest = get_closest(response['reservations'])
