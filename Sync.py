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
version = '0.6.0'

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

if args.download or args.upload or args.upload_all or args.download_all:
    # Catch the websites.
    livesites_folder = config.get('SYNC', 'websites_folder', \
            fallback="/var/www")
    if args.upload:
        websites = args.upload
    if args.download:
        websites = args.download
    if args.upload_all or args.download_all:
        # Go to websites folder and get all folder names.
        os.chdir(livesites_folder)
        websites = next(os.walk(os.path.join(livesites_folder,'.')))[1]
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
            if website in config['WEBSITES']:
                ssh = "-e ssh " + website + ":/" + config['WEBSITES'][website]
                if args.upload:
                    from_location = local_website
                    to_location = ssh

                if args.download:
                    from_location = ssh
                    to_location = local_website

                if args.verbose:
                    print( "[rsync] " + from_location + " -> " + to_location )

                # Run rsync & log
                rsync_command = "rsync -vrizc --del " + \
                    "--exclude=.git --exclude=.gitignore --exclude=.ssh " + \
                    from_location + " " + to_location
                print(subprocess.getoutput(rsync_command))

            else:
                parser.error("Website folder not configured in: "+ sync_config)

            if args.verbose:
                print( "[sync] Finished: " + website )
        else:
            print( "[ERROR] No local website folder found: " + local_website )
else:
    parser.error( "No site(s) specified. Exiting." )
