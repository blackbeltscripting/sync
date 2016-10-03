# Sync.py

## Version 0.6.x

## REQUIREMENTS

* python3
* ssh
* rsync

If you have a \*NIX machine, make sure to install the required commands:

	$ sudo apt-get install python3 rsync ssh
	$ python3 --version

The second line should output a version of python3.

## Usage

(Up/Down)loads to remote website. For more information:

	$ python3 Sync.py -h

## How it works

The script will look for your `~/.sync` file. Here is an example of a default `.sync` file:

	[SYNC]
	websites_folder = /var/www/
	
	[WEBSITES]
	www.mysite.com = httpdocs/
	mysite2.com = public_html/
	

There it will look for the `websites_folder` path for your site (default is `/var/www/`):

	$ python3 Sync.py -d www.mysite.com

Your default folder will then be:

	/var/www/www.mysite.com/

Once it finds your selected site, it will the `.sync` file for the remote folder. In this case the remote folder is:

	www.mysite.com/httpdocs/

### Using SSH

This script requires SSH access and connects using only the `alias` found in your `~/.ssh/config` file:

	Host `alias`
		HostName mysite.com
		User username
		IdentityFile ~/.ssh/id_rsa

Rsync will then run like so:

	rsync /var/www/www.yoursite.com/ -e ssh `alias`

## Upload/Download Multiple sites at once:

Sync.py can upload or download multiple websites at once with the simple code:

	$ python3 Sync.py -[u/d] www.site1.com www.site2.com ...

### Upload/Download all sites at once:

Sync.py can process all your sites with the following command:

	$ python3 Sync.py --[up/down]all

**NOTE:** This command will ignore all -u and -d commands. Downloads takes precedence over uploads.

### Download takes precedence over upload

Suppose you write the following:

	$ python3 Sync.py -d www.site1.com -u www.site2.com

Sync.py **will ignore the upload arguments and will only download**!

## Development of Sync.py

The next version will have the options of not logging/or auto-git

	python3 Sync.py -d www.yoursite.com --nolog --nogit

## Help

I am a busy person who is always in need of efficient code to manage my businesses. If you are out there and are willing to help me develop this code who can also envision this (or any other) project, feel free to contact me.
