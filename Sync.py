#!/usr/bin/python

# Imports all classes that are being used in program
import sys, glob, os, datetime, getopt, subprocess, argparse

# Import this file
# ~/.sync_config
# [...]
script_name='sync'

# Define variables
websites_folder = os.environ['HOME'] + "/Public/" + "live_sites/"
log_name = 'logs'

# docommand( [list] command ) {{{
# Do command and return output regardless if throws errors
def docommand(command):
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        output = e.output
    return output
# }}}

# commandtolog( [list] command, [string] command_name, [string] log_path ) {{{
# Look for log file folder, and create
# Name the file as command-date-ISOformat.log
# Get command output suting docommand() and write() into file
# Print and exit
def commandtolog(command, command_name, log_path, args):
    filename = command_name + '-' + datetime.datetime.now().isoformat() + '.log'
    full_filename = log_path + filename

    # If log/ folder exist, continue
    if not os.path.exists(log_path):
        if args.verbose:
            print( "[-] " + log_path + " Folder not found. Please create folder. Quitting without sync." )
        sys.exit(0)
    else:
        if args.verbose:
            print ( "[>] Log folder found! Creating log file: " + filename )

    if args.debug:
        print()
        print ( command )
        print()
    if isinstance(command, list) == False:
        command = command.split()
    output = docommand(command)
    if args.debug:
        print()
        print("Log File contents:")
        print(output.decode("utf-8"))
        print("EOF")
        print()
    with open(full_filename, "wt") as out_file:
        out_file.write(output.decode("utf-8"))
    if args.verbose:
        print ( '[+] ' + full_filename )
# }}}

# Parser {{{
parser = argparse.ArgumentParser(
        prog=script_name,
        description='''\
               (Up/Down)loads to remote website.
               EX: ''' + script_name + ''' -d www.yoursite.com''',
        epilog='''
           Sync uses rsync to move the website by using the ".''' +
           script_name +
           '''" file located in your
           "/live_sites/"
           folder. It will also write into the
           /logs/
           folder.
        ''')

parser.add_argument('-u', '--upload',
                    help='Uploads site to remove (live) server.')
parser.add_argument('-d', '--download',
                    help='Downloads site to your local (dev) server.')
parser.add_argument('-q', '--quiet',
                    action="store_false", dest="verbose",
                    help='Does not display any outputs')
parser.add_argument('-v', '--verbose',
                    action="store_true", dest="verbose",
                    default=True,
                    help='Verbose will show you important information.')
parser.add_argument('--debug',
                    action="store_true", dest="debug",
                    help='VERY verbose. For debugging purposes.')
parser.add_argument('--version', action='version', version='%(prog)s 0.2')

args = parser.parse_args()
# }}}

if args.debug:
    print ( args )

if args.download:
    website = args.download

if args.upload:
    website = args.upload

# define variables
local_website = websites_folder + website + "/"

if args.verbose == True:
    print ( '--------' )
    print ('Website: ' + website)
    print ( '--------' )


# CD to local website and get .sync file
os.chdir(local_website)

# Get remote site
for dotfile in glob.glob(".*"):
    if dotfile == ".sync" and os.stat(dotfile).st_size != 0:
        f = open(dotfile, 'r')
        sync_file = []
        for line in f:
            sync_file.append(line[:-1])
        f.close()

if args.debug:
    print ( '.' + script_name + ' file:' )
    print ( sync_file )
    print ()

# If we have a sync_file, continue
if sync_file:
    # Must define here
    log_path = local_website + log_name + '/'

    remote_server = sync_file[0].split()
    if args.upload:
        local_subdirectory = ""
        if len(remote_server) > 1:
            local_subdirectory = remote_server[1]
        from_location = local_website + local_subdirectory
        to_location = remote_server[0]
    if args.download:
        remote_db = sync_file[1].split()
        from_location = remote_db[0]
        local_subdirectory = ""
        if len(remote_db) > 1:
            local_subdirectory = remote_db[1]
        to_location = local_website + local_subdirectory
        if args.verbose:
            print ("[rsync] Downloading DB.")
            print ( "[rsync] " + from_location + " -> " + to_location )
        rsync_command = "rsync -vrizc --del --exclude=.sync --exclude=.ssh --exclude=" + log_name + " --exclude=.git --exclude=.gitignore -e ssh " + from_location + " " + to_location
        commandtolog(rsync_command, 'rsync', log_path, args)

        local_subdirectory = ""
        if len(remote_server) > 1:
            local_subdirectory = remote_server[1]
        to_location = local_website + local_subdirectory
        from_location = remote_server[0]

    # define variables
    if args.verbose:
        print ("[rsync] Downloading files.")
        print ( "[rsync] " + from_location + " -> " + to_location )
    rsync_command = "rsync -vrizc --del --exclude=.sync --exclude=.ssh --exclude=db_backups --exclude=.git --exclude=.gitignore --exclude=" + log_name + " -e ssh " + from_location + " " + to_location

    # Run rsync & log
    commandtolog(rsync_command, 'rsync', log_path, args)

    # CD to website
    os.chdir(local_website)

    # Look for git
    ignore = local_website + ".gitignore"
    if not os.path.isfile(ignore):
        if args.verbose:
            print ( "[!] No .gitignore file found. Creating file." )
        with open(ignore, "wt") as out_file:
            out_file.write(log_name + '/')
    if not os.path.exists(local_website + ".git"):
        if args.verbose:
            print ( "[!] No .git folder found. Initializing git." )
        docommand(["git", "init"])
        docommand(["git", "add", "."])
        docommand(["git", "commit", "-am", "'Auto Commit'"])

    # Run git status & log
    commandtolog(["git", "log", "--since='1 week ago'"], 'git', log_path, args)
else:
    print ( "[rsync] No or empty .sync file found. Skipping website." )

if args.verbose:
    print ( "[rsync] Finished: " + website )

sys.exit(0)
