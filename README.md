# Sync.py

## Version 0.3

## REQUIREMENTS

* python3
* ssh
* rsync
* git
* `.sync_config` [File located in your home folder.]
* `.sync` [File located in your local website's home folder.]
* `wpscan` [GET IT HERE: http://wpscan.org/]

If you have a \*NIX machine, make sure to install the required commands:

	$ sudo apt-get install python3 rsync git ssh
	$ python3 --version

The second line should output a version of python3.

## Usage

(Up/Down)loads to remote website. For more information:

	$ python3 Sync.py -h

## How it works

The script will look for your `~/.sync_config` file. Here is an example of a default `.sync_config` file:

	[DEFAULT]
	logs_folder = logs/
	
	[SYNC]
	websites_folder = /var/www/

There it will parse the `websites_folder` variable (default is `/var/www/`) and will look for that site:

	$ python3 Sync.py -d www.yoursite.com

Your default folder will then be:

	/var/www/www.yoursite.com/

Once it finds your selected site, it will parse its `.sync` file for the remote address and local folders to (up/down)load. Your default `.sync` file will be:

	/var/www/www.yoursite.com/.sync

Here is a sample of a full `.sync` file:

	[REMOTE]
	is_remote = [true/false]
	alias = yoursite
	username = user
	hostname = yoursite.com
	folder = /public_html/
	db_folder = /db_backups/
	
	[LOCAL]
	folder = httpdocs/
	db_folder = db_backups/

## Local-to-Local sync

If we ran the command `python3 Sync.py -d www.yoursite.com`, and we had the `.sync` below:

	[REMOTE]
	is_remote = false
	folder = /home/user/Public/www.yoursite.com/public_html
	
	[LOCAL]
	folder = public_html/

Then rsync will run like so:

	rsync /home/user/Public/www.yoursite.com/public_html /var/www/www.yoursite.com/public_html/

## Local-to-Remote sync

**NOTE:** Remember to set `is_remote` to `true`.

### Using username@hostname

If we ran the command `python3 Sync.py -d www.yoursite.com`, and we had the `.sync` below:

	[REMOTE]
	is_remote = true
	username = user
	hostname = yoursite.com
	folder = /public_html/

Then rsync will run like so:

	rsync -e ssh user@yoursite.com:/public_html/ /var/www/www.yoursite.com/

### Using alias

If you want to `cron` this script, you can choose to use the `alias` variable. Simply type your `Host` name from your `~/.ssh/config` into the `.sync` file:

If we ran the command `python3 Sync.py -u www.yoursite.com`, and we had the `~/.ssh/config` file below:

	Host mysite
		HostName yoursite.com
		User user
		IdentityFile ~/.ssh/id_rsa

And we had the `.sync` file below:

	[REMOTE]
	is_remote = true
	alias = mysite

Then rsync will run like so:

	rsync /var/www/www.yoursite.com/ -e ssh mysite

### Download mysqldump file output

If your remote server `cron`s a `mysqldump` file into a `tmp` folder. Simply type the following in your `.sync` file:

	[REMOTE]
	is_remote = true
	alias = mysite
	db_folder = /tmp/
	
	[LOCAL]
	db_folder = db_backup/

And Sync.py will automatically download all files in folder `/tmp/`.

**NOTE:** The script will create a `db_folder` if not found.

## Logs & Git

Sync.py will by default log all commands into your logs folder (default `www.yoursite.com/logs`). If it doesn't find a `.git` folder in your site, it will init and do a first commit automatically.

**NOTE:** The script will automaticall create a `logs/` folder if not found.

**NOTE:** rsync will ignore your `.git/` folder, your `.gitignore` file, your `.ssh/` folder, your `logs/`, and your `.sync` files automatically. So there is no breach of security.

## wpscan

In order to automatically do a `wpscan`, you must have `ruby v 2.3.0+` and `wpscan`. Then add the `ruby` path in your `.sync_config` file:

	wpscan_command = /home/usr/.rvm/wrappers/ruby-2.3.0@wpscan/ruby /path/to/wpscan/wpscan.rb --update --url

And Sync.py will do the rest!

### Changing log folder location

To change the logs location to `loggings/` as an example, type the following in your `~/.sync_config`:

	[DEFAULT]
	logs_folder = loggins/

**NOTE:** The script will automatically create a `loggins/` folder if not found.

## Development of Sync.py

The next version will have the capacity of doing multiple sites:

	python3 Sync.py -d www.site1.com www.site2.com -u www.site3.com www.site4.com

It will also have the options of not logging/or auto-git

	python3 Sync.py -d www.yoursite.com --nolog --nogit

## Help

I am a busy person who is always in need of efficient code to manage my businesses. If you are out there and are willing to help me develop this code who can also envision this (or any other) project, feel free to contact me.
