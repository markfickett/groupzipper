============
Introduction
============

Zip a number of flickr sets to a group pool, resulting in a group pool ordered
by photo capture time, oldest first.

Some editing of zipsetstogroup.py (hereafter 'the main file')  will be required
to run the script; see comments in that file. You will also need a flickr API
key, and some patience getting all the photo owners to visit a flickr URL to
allow this script (using your API key) to access their accounts.

Flickr ideas discussion thread:
	http://www.flickr.com/groups/flickrideas/discuss/72157600606083730/

============
Instructions
============

o Get an API key: http://www.flickr.com/services/api/misc.api_keys.html . Create
secret.py in the same directory as the main file with the API key and
secret.

o Edit the main file to add the set IDs and group ID.

o Run the main file. The first time, you will need each flickr account owner to
log in to flickr and allow the script (in concert with your API key) access.
You will see something like:

$ python zipsetstogroup.py 
'token_35112219@N07.txt' not found, authenticating.
Log in to flickr as Ada Smith (ID = 35112919@N07), then visit this URL and allow access: http://flickr.com/services/auth/?api_key=stuffstuff&perms=write&frob=stuffstuffstuff&api_sig=stuffstuff

While it's waiting, log in as the right flickr user, visit the URL, and grant
the requested permissions. Repeate for other users.

o The script should fetch all the photo data and populate the group. Note that
the group is not cleared first.

============
Difficulties
============

Motivating problem: Sorting flickr group pools from the owner perspective is not
possible (as it is with sets). There is not an option to sort a group (or search
results) by date taken (as opposed to added-to-group or added-to-flickr time).

Complication: Only a photo's owner can add a photo to a group. Therefore (a) the
script must be authenticated, and (b) it must match the currently 'installed'
authentication token with the photo being added to the group. (Due to the nature
of the problem, this means switching auth tokens back and forth.)

