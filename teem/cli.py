#! python3.7
import argparse
from inspect import getmembers, isclass

""" Usage:

    ARGPARSE FORMAT: 'python3 script.py POSITIONAL_ARG --OPTIONAL_ARG...--OPTIONAL_ARG
    
    reserve - creates a reservation in platform
        REQUIRED - room, start_time, duration
        OPTIONAL - meeting title, participants
        Usage:
        1) 'py cli.py reserve showcase 2 5' - reserves the showcase room for five minutes
            with a start time two minutes from now.
        2) 'py cli.py reserve showcase 10 30 --title 'Very Important Meeting' --participants Robin'
            - reserves the showcase room for thirty minutes with a start time in ten minutes, a title of:
            'Very Important Meeting' and with participants of myself and Robin.
            

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
parser = argparse.ArgumentParser(description="""Create, change and delete Teem reservations.
                                                List reservations, users and rooms.""")
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
group1.add_argument("-q","--quiet", help="decrease output verbosity", action="store_true")
subparsers = parser.add_subparsers(title='commands', dest='command',help="Subparser help")

# RESERVE
reserve_parser = subparsers.add_parser('reserve', help="reserve command help")
##reserve_parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
##reserve_parser.add_argument("-q","--quiet", help="decrease output verbosity", action="store_true")
reserve_parser.add_argument("room", type=str, action='store')
reserve_parser.add_argument("starts_in", type=int, action='store')
reserve_parser.add_argument("duration", type=int, action='store')
reserve_parser.add_argument("--title", type=str, action='store')
reserve_parser.add_argument("--participants", type=str, action='store', nargs='*')

# DELETE
delete_parser = subparsers.add_parser('delete', help="delete command help")
delete_parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
delete_parser.add_argument("-q","--quiet", help="decrease output verbosity", action="store_true")
delete_parser.add_argument("meeting_id", type=int, action='store')

##change_parser = subparsers.add_parser('change', "change command help")
##change_parser.add_argument('')

##checkin_parser = subparsers.add_parser('checkin', "checkin command help")
##checkin_parser.add_argument('')

# RESERVATIONS
reservations_parser = subparsers.add_parser('reservations', help="reservations command help")
reservations_parser.add_argument('-r','--room', type=str, action='store', help='specify the room name to filter reservations just for that room')
reservations_parser.add_argument('-l','--loop', action='store_true', help='continuously update reservations list')
reservations_parser.add_argument('-b','--before', action='store', type=str, help='filter results before specified time')
reservations_parser.add_argument('-a','--after', action='store', type=str, help='continuously update reservations list')

# ROOMS
rooms_parser = subparsers.add_parser('rooms', help="rooms command help")
##rooms_parser.add_argument('')

# USERS
users_parser = subparsers.add_parser('users', help="users command help")
users_parser.add_argument('-n', '--name', type=str, action='store', help='get info about a particular user')

                    
def main():
    """ 1) parse arguments
        2) match arg.command to a class in 'commands' module
        3) pass the other arguments in args into the 'run()' function
            of the class and run it."""
    import commands
##    args = parser.parse_args('reservations --loop'.split())
    args = parser.parse_args()
    if hasattr(commands, str(args.command)):
        module = getattr(commands, str(args.command))
        module.run(module, vars(args))

if __name__ == '__main__':
##    args = main()
    main()
##    command = main()


    