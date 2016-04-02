# Sync.py

## Version 0.2

## REQUIRES PYTHON3

If you have a .NIX machine, make sure to install python3:

	$ sudo apt-get install python3 (or equivalent)
	$ python3 --version

Should output:

	Python 3.x.x (or equivalent)

## Description

(Up/Down)loads to remote website.

	EX: python3 Sync.py -d www.yoursite.com
	python3 Sync.py -h

It will look into your local_website folder (currently hard-wired into the script but later on will be in your ~/.sync file.) and begins to look for a local .sync file. EX:

	/var/www/www.yoursite.com/.sync

The file will contain two lines:

	remote_server local_folder
	remote_db local_db_folder

The first line is the remote server address, followed by a [space] and the local folder. So if the first line is:

	user@remote-server:/httpdocs/ httpdocs/

And you want to download your site:

	python3 Sync.py -d www.yoursite.com

Sync.py will use rsync to download the site:

	rsync -[...] --exclue=[exclude_list] -e ssh user@remote-server:/httpdocs/ /var/www/www.yoursite.com/httpdocs/

## Development of Sync.py

Sync.py currenly requires 4 variables to work:

	1) [websites_folder] Where all your local sites will be held. (currently hard-wired into Sync.py but will be moved to your ~/.sync file)
	2) The website's .sync file. EX: [websites_folder]/www.yoursite.com/.sync
	3) The websites's logs folder. EX: [websites_folder]/www.yoursite.com/logs
	4) The websites's db_backups folder. EX: [websites_folder]/www.yoursite.com/db_backups

However in the next version, all we will need are the first two. The folders will be added automatically if none found.

Also, the next version will have the capacity of doing multiple sites:

	python3 Sync.py -d www.site1.com www.site2.com -u www.site3.com www.site4.com

## Help

I am a busy person who is always in need of efficient code to manage my businesses. If you are out there and are willing to help me develop this code who can also envision this project (more details of the project's vision will be created in the wiki soon), feel free to contact me.
