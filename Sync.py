#!/usr/bin/python
# Arty // Web Design and Programming
# Sync.py
# Get new updates of this script at:
#    https://github.com/blackbeltscripting/sync
# Or visit us at:
#    http://www.arty-web-design.com

# Decided to use the easy form to add the log directory using the code from:
# http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary

# Imports all classes that are being used in program
import sys, glob, os, datetime, getopt, subprocess, argparse, configparser

script_name='sync'
version = '0.5.1'

# Import config file from home folder
config_filename = ".sync_config"
sync_config = os.environ['HOME'] + "/" + config_filename

# Script Arguments {{{
parser = argparse.ArgumentParser(
        prog=script_name,
        description='''\
               (Up/Down)loads to remote website.
               EX: ''' + script_name + ''' -d www.yoursite.com''',
        epilog='''
           Sync uses rsync to move the website by using the ".''' +
           script_name +
           '''" file located in your websites_folder. All logs will be
           written in your logs_folder. To change these locations,
           edit your "''' + config_filename + '''" file located at '''
           + sync_config)

parser.add_argument('-u', '--upload', metavar='WEBSITE', nargs='*',
                    help='Uploads site to remove (live) server.')
parser.add_argument('-d', '--download', metavar='WEBSITE', nargs='*',
                    help='Downloads site to your local (dev) server.')
parser.add_argument('--upload_all', action="store_true", default=False,
                    help='Uploads all websites from your local (dev) server. If this command is called, program will ignore all other "-u" or "-d" commands.')
parser.add_argument('--download_all', action="store_true", default=False,
                    help='Downloads all websites from your local (dev) server. If this command is called, program will ignore all other "-u" or "-d" commands.')
parser.add_argument('--wpscan', action="store_true", default=False,
                    help='Runs wpscan on site. REQUIRES wpscan!')
parser.add_argument('-q', '--quiet',
                    action="store_false", dest="verbose",
                    help='Display only errors.')
parser.add_argument('-v', '--verbose',
                    action="store_true", dest="verbose",
                    default=True,
                    help='Verbose will show you important information.')
parser.add_argument('--debug',
                    action="store_true", dest="debug",
                    help='VERY verbose. For debugging purposes.')
parser.add_argument('--version', action='version', version='%(prog)s ' + version)

args = parser.parse_args()
# }}}

# Create default config file if none found {{{
if not os.path.isfile(sync_config):
    # No configuration file found.
    if args.verbose:
        print( "[!] No " + config_filename + " file found. Creating file." )
    with open(sync_config, "wt") as out_file:
        # Write default config file
        output = '''[DEFAULT]
logs_folder = logs/

[SYNC]
websites_folder = /var/www/'''
        out_file.write(output)
# }}}

# Read file and parse it. {{{
with open(sync_config, 'r') as f:
    config_string = f.read()
config = configparser.ConfigParser()
config.read_string(config_string)

wpscan_command = config.get('SYNC', 'wpscan_command')
# }}}

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
    if args.upload:
        websites = args.upload
    if args.download:
        websites = args.download
    if args.upload_all or args.download_all:
        os.chdir(config.get('SYNC', 'websites_folder', fallback="/var/www"))
        websites = glob.glob('*')
        if args.upload_all:
            args.upload = True
        if args.download_all:
            args.download = True
    for website in websites:
        # define variables
        local_website = config.get('SYNC', 'websites_folder', fallback="/var/www/") + website + "/"

        if os.path.exists(local_website):
            if args.verbose == True:
                print( '--------' )
                print( 'Website: ' + website )
                print( '--------' )
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
                if is_remote:
                    # Remote server MUST have username/hostname
                    remote_username = sync.get('REMOTE', 'username', fallback=False)
                    remote_hostname = sync.get('REMOTE', 'hostname', fallback=False)
                    remote_alias = sync.get('REMOTE', 'alias', fallback=False)
                    remote_db_folder = sync.get('REMOTE', 'db_folder', fallback=False)

                    if remote_folder:
                        remote_folder = ":" + remote_folder

                    # If alias is setup, continue.
                    if remote_alias:
                        remote_server = "ssh " + remote_alias
                    else:
                        # Alias is not setup. Do we have at least user@host?
                        if remote_username and remote_hostname:
                            if args.verbose:
                                remote_server = sync.get('REMOTE', 'alias', fallback=remote_username + '@' + remote_hostname)
                            else:
                                sys.exit( "[ERROR] Cannot run quietly because this site has no alias. Setup your ssh to login automatically." )
                        else:
                            sys.exit( "[ERROR] " + sync_filename + " does not contain remote server address. Exiting." )
                else:
                    # Running rsync locally. Check if remote folder is set.
                    if not remote_folder:
                        sys.exit( "[ERROR] No remote folder found. Check your " + sync_filename + " file. Exiting" )

                if args.upload:
                    from_location = local_website + sync.get('LOCAL', 'folder', fallback="")
                    to_location = "-e " + remote_server + remote_folder

                local_db_folder = sync.get('LOCAL', 'db_folder', fallback="db_backups/")
                if args.download:
                    # If remote_db_folder is set, rsync db
                    if remote_db_folder:
                        to_location = local_website + local_db_folder
                        from_location = "-e " + remote_server + ":" + remote_db_folder
                        if args.verbose:
                            print( "[rsync] Downloading DB." )
                            print( "[rsync] " + from_location + " -> " + to_location )
                        # Run rsync & log
                        rsync_command = "rsync -vrizc --del --exclude=.git --exclude=.gitignore --exclude=.ssh --exclude=" + sync_filename + " --exclude=" + log_folder + " " + from_location + " " + to_location
                        commandtolog(rsync_command, 'rsync', local_website + log_folder, args)

                    to_location = local_website + sync.get('LOCAL', 'folder', fallback="")
                    from_location = "-e " + remote_server + remote_folder

                if args.verbose:
                    print( "[rsync] Downloading files." )
                    print( "[rsync] " + from_location + " -> " + to_location )

                # Run rsync & log
                rsync_command = "rsync -vrizc --del --exclude=.git --exclude=.gitignore --exclude=.ssh --exclude=" + sync_filename + " --exclude=" + local_db_folder + " --exclude=" + log_folder + " " + from_location + " " + to_location
                commandtolog(rsync_command, 'rsync', local_website + log_folder, args)

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

                # CD to local website to run next command.
                os.chdir(local_website)

                # Run git status & log
                commandtolog(["git", "log", "--since='1 week ago'"], 'git', local_website + log_folder, args)
            else:
                sys.exit( "[ERROR] No or empty .sync file found. Skipping website." )

            if args.wpscan:
                wpscan_file_lookout = local_website + sync.get('LOCAL', 'folder', fallback="") + 'wp-config.php'

                # If it's a WordPress site
                if os.path.isfile(wpscan_file_lookout):
                    if args.verbose:
                        print( "[wpscan] WordPress Found. Initializing wpscan." )
                    wpscan_command = wpscan_command + " " + website
                    commandtolog(wpscan_command.split(), 'wpscan', local_website + log_folder, args)
            if args.verbose:
                print( "[sync] Finished: " + website )
        else:
            print( "[ERROR] No local website folder found. Skipping website: " + website )
else:
    sys.exit( "[ERROR] No site(s) specified. Exiting." )
