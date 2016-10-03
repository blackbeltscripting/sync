#!/usr/bin/python
# Arty // Web Design and Programming
# Sync.py
# Get new updates of this script at:
#    https://github.com/blackbeltscripting/sync
# Or visit us at:
#    http://www.arty-web-design.com

# Decided to use the easy form to add the log directory using the code from:
# http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
# NOTE: Let's get the log file to Pub/logs through sync_config

# Imports all classes that are being used in program
import sys, glob, os, datetime, getopt, subprocess, argparse, configparser

script_name='sync'
<<<<<<< HEAD
version = '0.5.9'
=======
version = '0.6.0'
>>>>>>> adding_db

# Import config file from home folder
config_filename = ".sync"
sync_config = os.environ['HOME'] + "/" + config_filename

# Script Arguments {{{
parser = argparse.ArgumentParser(
        prog=script_name,
        description='''\
               (Up/Down)loads to remote website.
               EX: ''' + script_name + ''' -d www.yoursite.com
               YOU MUST HAVE rsync installed.''',
        epilog='''
           Sync uses rsync to move the website by using the ".''' +
           script_name +
           '''" file located in your home folder: '''
           + sync_config)

parser.add_argument('-u', '--upload', metavar='WEBSITE', nargs='*',
                    help='Uploads site to remove (live) server.')
parser.add_argument('-d', '--download', metavar='WEBSITE', nargs='*',
                    help='Downloads site to your local (dev) server.')
parser.add_argument('--upload_all', action="store_true", default=False,
                    help='Uploads all websites from your local (dev) server. If this command is called, program will ignore all other "-u" or "-d" commands.')
parser.add_argument('--download_all', action="store_true", default=False,
                    help='Downloads all websites from your local (dev) server. If this command is called, program will ignore all other "-u" or "-d" commands.')

parser.add_argument('-v', '--verbose',
                    action="store_true", dest="verbose",
                    default=True,
                    help='Verbose will show you important information.')
parser.add_argument('--version', action='version', version='%(prog)s '+version)

args = parser.parse_args()
# }}}

# Read file and parse it. {{{
with open(sync_config, 'r') as f:
    config_string = f.read()
config = configparser.ConfigParser()
config.read_string(config_string)

wpscan_command = config.get('SYNC', 'wpscan_command')
# }}}

<<<<<<< HEAD
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
# Get command output string docommand() and write() into file
# Print and exit
def commandtolog(command, command_name, log_path, args):
    if not args.nolog:
        filename = command_name + '-' + datetime.datetime.now().isoformat() + '.log'
        full_filename = log_path + filename
        # Create if doesn't exist: logs/
        if not os.path.exists(log_path):
            os.makedirs(log_path)
            if args.verbose:
                print( "[!] Created logs folder: " + log_path)
        else:
            if args.verbose:
                print( "[>] Log folder found! Creating log file: " + filename )

    if args.debug:
        print( "\n" , command , "\n" )

    if isinstance(command, list) == False:
        command = command.split()
        output = docommand(command)

    if not args.nolog:
        if args.debug:
            print("\nLog File contents:\n" + output.decode("utf-8") + "\nEOF")

        with open(full_filename, "wt") as out_file:
            out_file.write(output.decode("utf-8"))
    if args.verbose:
        print( '[+] ' + full_filename )
# }}}

if args.debug:
    print( args )

if args.download or args.upload or args.upload_all or args.download_all:
    # Catch the websites.
=======
if args.download or args.upload or args.upload_all or args.download_all:
    # Catch the websites.
    livesites_folder = config.get('SYNC', 'websites_folder', \
            fallback="/var/www")
>>>>>>> adding_db
    if args.upload:
        websites = args.upload
    if args.download:
        websites = args.download
    if args.upload_all or args.download_all:
        # Go to websites folder and get all folder names.
<<<<<<< HEAD
        os.chdir(config.get('SYNC', 'websites_folder', fallback="/var/www"))
        websites = glob.glob('*')
=======
        os.chdir(livesites_folder)
        websites = next(os.walk(os.path.join(livesites_folder,'.')))[1]
>>>>>>> adding_db
        # Still do up/download commands
        if args.upload_all:
            args.upload = True
        if args.download_all:
            args.download = True
    for website in websites:
        # define variables
        local_website = livesites_folder + website + "/"

        if os.path.exists(local_website):
            if args.verbose == True:
                print( '--------' )
                print( 'Website: ' + website )
                print( '--------' )
<<<<<<< HEAD
            # Get local .sync file
            sync_filename = '.sync'
            if os.path.isfile(local_website + sync_filename):
                # Read file and parse it.
                with open(local_website + sync_filename, 'r') as f:
                    config_string = f.read()
                sync = configparser.ConfigParser()
                sync.read_string(config_string)

                # Get log folder
                # Local takes precedence, then default, then script default.
                default_log_folder = config.get('DEFAULT', 'logs_folder', fallback="logs/")
                log_folder = sync.get('LOCAL', 'logs_folder', fallback=default_log_folder)

                # Check to see if remote server is really remote.
                # (In case we want to rsync locally.)
                remote_server = ""
                remote_folder = sync.get('REMOTE', 'folder', fallback="")
                is_remote = sync.get('REMOTE', 'is_remote', fallback=False)
                remote_folder = sync.get('REMOTE', 'folder', fallback="")
                remote_db_folder = sync.get('REMOTE', 'db_folder', fallback=False)
                if is_remote == "true":
                    # Remote server MUST have username/hostname
                    remote_username = sync.get('REMOTE', 'username', fallback=False)
                    remote_hostname = sync.get('REMOTE', 'hostname', fallback=False)
                    remote_alias = sync.get('REMOTE', 'alias', fallback=False)

                    if remote_folder:
                        remote_folder = ":" + remote_folder + "/"

                    # If alias is setup, continue.
                    if remote_alias:
                        remote_server = "ssh " + remote_alias
                    else:
                        # Alias is not setup. Do we have at least user@host?
                        if remote_username and remote_hostname:
                            if args.verbose:
                                remote_server = "ssh " + sync.get('REMOTE', 'alias', fallback=remote_username + '@' + remote_hostname)
                            else:
                                parser.error( "Cannot run quietly because this site has no alias. Setup your ssh to login automatically. Exiting." )
                        else:
                            parser.error( sync_filename + " does not contain remote server address. Exiting." )
                else:
                    # Running rsync locally. Check if remote folder is set.
                    if not remote_folder:
                        parser.error( "No remote folder found. Check your " + sync_filename + " file. Exiting." )
                    else:
                        remote_server = remote_folder

                if args.upload:
                    local_folder = sync.get('LOCAL', 'folder', fallback="")
                    if local_folder:
                        from_location = local_website + local_folder + "/"
                    else:
                        from_location = local_website
                    to_location = "-e " + remote_server + remote_folder
=======
            if website in config['WEBSITES']:
                ssh = "-e ssh " + website + ":/" + config['WEBSITES'][website]
                if args.upload:
                    from_location = local_website
                    to_location = ssh
>>>>>>> adding_db

                if args.download:
<<<<<<< HEAD
                    # If remote_db_folder is set, rsync db
                    if remote_db_folder:
                        to_location = local_website + local_db_folder
                        if is_remote == "true":
                            from_location = "-e " + remote_server + ":" + remote_db_folder + "/"
                        else:
                            from_location = remote_server + remote_db_folder
                        if args.verbose:
                            print( "[rsync] Downloading DB." )
                            print( "[rsync] " + from_location + " -> " + to_location )
                        # Run rsync & log
                        rsync_command = "rsync -vrizc --del --exclude=.git --exclude=.gitignore --exclude=.ssh --exclude=" + sync_filename + " --exclude=" + log_folder + " " + from_location + " " + to_location
                        commandtolog(rsync_command, 'rsync', local_website + log_folder, args)

                    local_folder = sync.get('LOCAL', 'folder', fallback="")
                    if local_folder:
                        to_location = local_website + local_folder + "/"
                    else:
                        to_location = local_website

                    if is_remote == "true":
                        from_location = "-e " + remote_server + remote_folder
                    else:
                        from_location = remote_server
=======
                    from_location = ssh
                    to_location = local_website
>>>>>>> adding_db

                if args.verbose:
                    print( "[rsync] " + from_location + " -> " + to_location )

                # Run rsync & log
                rsync_command = "rsync -vrizc --del " + \
                    "--exclude=.git --exclude=.gitignore --exclude=.ssh " + \
                    from_location + " " + to_location
                print(subprocess.getoutput(rsync_command))

<<<<<<< HEAD
                if not args.nogit:
                    # Look for git
                    ignore = local_website + ".gitignore"
                    if not os.path.isfile(ignore):
                        if args.verbose:
                            print( "[!] No .gitignore file found. Creating file." )
                        with open(ignore, "wt") as out_file:
                            # ignores only the 'logs/' folder.
                            out_file.write(log_folder)
                    if not os.path.exists(local_website + ".git"):
                        if args.verbose:
                            print( "[!] No .git folder found. Initializing git." )
                        docommand(["git", "init"])
                        docommand(["git", "add", "."])
                        docommand(["git", "commit", "-am", "'Auto Commit'"])

                    # Run git status & log
                    commandtolog("git log --since='1 week ago'", 'git', local_website + log_folder, args)
            else:
                parser.error( "No or empty .sync file found. Skipping website." )

            if args.wpscan:
                # Looks for WordPress config file. Won't work if wp-config.php is in sub-folders
                if os.path.isfile(local_website + sync.get('LOCAL', 'folder', fallback="") + 'wp-config.php'):
                    if args.verbose:
                        print( "[wpscan] WordPress Found. Initializing wpscan." )
                    wpscan_command = wpscan_command + " " + website
                    commandtolog(wpscan_command.split(), 'wpscan', local_website + log_folder, args)
=======
            else:
                parser.error("Website folder not configured in: "+ sync_config)

>>>>>>> adding_db
            if args.verbose:
                print( "[sync] Finished: " + website )
        else:
            print( "[ERROR] No local website folder found: " + local_website )
else:
    parser.error( "No site(s) specified. Exiting." )
