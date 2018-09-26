#! python3.7
import argparse
from Teem_API import Teem, create_time, get_input, make_meeting
""" Usage:

    ARGPARSE FORMAT: 'python3 script.py POSITIONAL_ARG --OPTIONAL_ARG...--OPTIONAL_ARG
    
    reserve - creates a reservation in platform
        REQUIRED - room, start_time, duration
        OPTIONAL - meeting title, participants

    delete - delete a created reservation
        REQUIRED - meeting id

    change - create a change to a reservation

    checkin - check in to a reservation

    reservations - display reservations
        REQUIRED: None
        OPTIONAL: --loop = keeps printing every 20 seconds
                  --room = only show reservations for particular room
                  --before = reservations before a particular time
                  --after = reservations after a particular time

    rooms - list all the rooms available in the platform

    users - list all users in platform
"""
parser = argparse.ArgumentParser(description="""Create, change and delete Teem reservations,
list reservations, users and rooms.""")
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
group1.add_argument("-q","--quiet", help="decrease output verbosity", action="store_true")

parser.add_argument("action", help="action can be: -reserve, -delete, -change, -checkin, -reservations, -rooms, -users",
                    choices=['reserve', 'delete', 'change', 'checkin', 'reservations', 'rooms', 'users'],
                    type=str,
                    action='store'
                    )
                    
def main():
    args = parser.parse_args()
    print(args.action)
    if args.action == 'delete':
        print("Delete Action Detected")
    if args.verbose:
        print("verbosity turned on")

if __name__ == '__main__':
    main()


    
