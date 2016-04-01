#!/usr/bin/python

# import classes
import sys, glob, os, datetime, getopt, subprocess

# Define variables
websites_folder = os.environ['HOME'] + "/Public/" + "live_sites/"
log_name = 'logs'

# write( [string] filename, [string] output )
# Writes [string] output into file [string] filename
def write(filename, output):
    saveout = sys.stdout
    fsock = open(filename, 'w')
    sys.stdout = fsock
    print output
    sys.stdout = saveout
    fsock.close()

# docommand( [list] command )
# Do command and return output regardless if throws errors
def docommand(command):
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        output = e.output
    return output

# commandtolog( [list] command, [string] command_name, [string] log_path )
# Look for log file folder, and create
# Name the file as command-date-ISOformat.log
# Get command output suting docommand() and write() into file
# Print and exit
def commandtolog(command, command_name, log_path):
    filename = command_name + '-' + datetime.datetime.now().isoformat() + '.log'
    full_filename = log_path + filename

    # If log/ folder exist, continue
    if not os.path.exists(log_path):
        sys.exit("[-] " + log_path + " Folder not found. Please create folder. Quitting without sync.")
    else:
        print "[>] Log folder found! Creating log file: " + filename
    output = docommand(command)
    write(full_filename, output)
    print '[+] ' + full_filename


def getremotesite():
    for dotfile in glob.glob(".*"):
        if dotfile == ".sync" and os.stat(dotfile).st_size != 0:
            f = open(dotfile, 'r')
            remote_website = []
            for line in f:
                remote_website.append(line[:-1])
            f.close()
            return remote_website

def Sync(argv):
    # define variables
    help_command = """sync(1)

    NAME
            sync - will upload/download to client's site.
    SYNOPSIS
            Upload to live site:
                sync -u [www.WEBSITE.com]
                sync --upload=[www.WEBSITE.com]
            Download from live site:
                sync -d [www.WEBSITE.com]
                sync --download=[www.WEBSITE.com]

            Where WEBSITE is the client's name.
    DESCRIPTION
            Sync uses rsync to move sall client's website into the
            """ + websites_folder + """ folder.

            It will also look for the remote server in the first line of the
            """ + websites_folder + """[www.WEBSITE.com]/.sync file.


            """ + websites_folder + """[www.WEBSITE.com]/""" + log_name + """/ log files.
        """

    if not argv:
        print help_command
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv, "hu:d:", ["upload=","download="])
    except getopt.GetoptError:
        print help_command
        sys.exit(2)
    for opt, website in opts:
        # define variables
        local_website = websites_folder + website + "/"

        print '--------'
        print 'Website: ' + website
        print '--------'

        os.chdir(local_website)
        remote_website = getremotesite()
        if remote_website:
            # Must define here
            log_path = local_website + log_name + '/'

            if opt == '-h':
                print help_command
            elif opt in ("-u", "--upload"):
                from_location = local_website
                to_location = remote_website[0]
            elif opt in ("-d", "--download"):
                from_location = remote_website[1]
                to_location = local_website
                print "[rsync] " + from_location + " -> " + to_location
                rsync_command = "rsync -vrizc --del --exclude=.sync --exclude=tmp --exclude=.ssh --exclude=" + log_name + " --exclude=.git --exclude=.gitignore " + from_location + " " + to_location
                commandtolog(rsync_command.split(), 'rsync', log_path)

                from_location = remote_website[0]

            # define variables
            print "[rsync] " + from_location + " -> " + to_location
            rsync_command = "rsync -vrizc --del --exclude=.sync --exclude=db_backup --exclude=tmp --exclude=.ssh --exclude=" + log_name + " --exclude=.git --exclude=.gitignore " + from_location + " " + to_location

            # CD to website
            os.chdir(local_website)

            # Run rsync & log
            commandtolog(rsync_command.split(), 'rsync', log_path)

            # Look for git
            ignore = local_website + ".gitignore"
            if not os.path.isfile(ignore):
                print "[!] No .gitignore file found. Creating file."
                write(ignore, log_name + '/')
            if not os.path.exists(local_website + ".git"):
                print "[!] No .git folder found. Initializing git."
                docommand(["git", "init"])
                docommand(["git", "add", "."])
                docommand(["git", "commit", "-am", "'Auto Commit'"])

            # Run git status & log
            commandtolog(["git", "log", "--since='1 week ago'"], 'git', log_path)
        else:
            print "[rsync] No or empty .sync file found. Skipping website."
    print "[rsync] Finished: " + website
if __name__ == "__main__":
    Sync(sys.argv[1:])
