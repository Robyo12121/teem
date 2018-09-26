#! python3.7
import argparse
from Teem_API import Teem, create_time, get_input, make_meeting
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


##parser.add_argument("action", help="cli.py help",
##                    choices=['reserve', 'delete', 'change', 'checkin', 'reservations', 'rooms', 'users'],
##                    type=str,
##                    action='store'
##                    )
subparsers = parser.add_subparsers(help="Subparser help")

reserve_parser = subparsers.add_parser('reserve', help="reserve command help")
##reserve_parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
##reserve_parser.add_argument("-q","--quiet", help="decrease output verbosity", action="store_true")
reserve_parser.add_argument("room", type=str, action='store')
reserve_parser.add_argument("start_in", type=int, action='store')
reserve_parser.add_argument("duration", type=int, action='store')
reserve_parser.add_argument("--title", type=str, action='store')
reserve_parser.add_argument("--participants", type=str, action='store', nargs='*')

##delete_parser = subparsers.add_parser('delete', "delete command help")
##delete_parser.add_argument('')
##
##change_parser = subparsers.add_parser('change', "change command help")
##change_parser.add_argument('')
##
##checkin_parser = subparsers.add_parser('checkin', "checkin command help")
##checkin_parser.add_argument('')
##
##reservations_parser = subparsers.add_parser('reservations', "reservations command help")
##reservations_parser.add_argument('')
##
##rooms_parser = subparsers.add_parser('rooms', "rooms command help")
##rooms_parser.add_argument('')
##
##users_parser = subparsers.add_parser('users', "users command help")
##users_parser.add_argument('')

#parser.add_argument
                    
def main():
    import commands
    args = parser.parse_args()
    print(vars(args))
##    if args.action == 'reserve':
##        if args.verbose:
##            print("AAAGGGGHHHH!!!!")
##        if args.quiet:
##            print("shhhh!")
##        print(f"{args.action} the {args.room} room for {args.duration} minutes with a start time in {args.start} minutes")
##    else:
##        print(f"{args.action}")

if __name__ == '__main__':
    main()


    
