"""
Zip a number of flickr sets to a group pool, resulting in a group pool ordered
by photo capture time, oldest first.

Feature request: http://www.flickr.com/groups/flickrideas/discuss/72157600606083730/
"""

import flickr
import flickrauth
import secret
import sys

###
# To run this, create a secret.py file with these vairables set according to
# your flickr API key (see
# http://www.flickr.com/services/api/misc.api_keys.html).

flickr.API_KEY = secret.API_KEY
flickr.API_SECRET = secret.API_SECRET

###
# Set the IDs of the sets from which photos will be drawn, and the group
# to which they will be added. (Make sure photo timestamps are synchronized!)

setIds = [
	# flickr.com/photos/capybararancher/sets/72157627084315687/
	'72157627084315687',
	# flickr.com/photos/markfickett/sets/72157627035346247/
	'72157627035346247',
]
# http://www.flickr.com/groups/1738107@N21/
# old group: http://www.flickr.com/groups/micahtraceywedding/
groupId = '1738107@N21'

###
###

def cmpPhotosByDateTakenAsc(a, b):
	return cmp(b.datetaken, a.datetaken)

allPhotos = []

for setId in setIds:
	sourceSet = flickr.Photoset(setId, None, None)
	setPhotos = sourceSet.getPhotos()
	if not setPhotos:
		print "No photos for set ID '%s'" % setId
		continue
	flickrauth.EnsureAuthenticatedForUser(setPhotos[0].owner)
	print ("Listed %d photos for set ID '%s'" % (len(setPhotos), setId))
	allPhotos += setPhotos

print ("Loading details for %d photos" % len(allPhotos))
for photo in allPhotos:
	photo._load_properties()
	print '.',
	sys.stdout.flush()
print " done."

print ("Sorting %d photos." % len(allPhotos))
allPhotos.sort(cmp=cmpPhotosByDateTakenAsc)

groupPool = flickr.Group(groupId)
print ("Adding to group ID '%s'..." % groupId)

for photo in allPhotos:
	print ("Adding %s (ID=%s) ..." % (photo.url, photo.id)),
	sys.stdout.flush()
	flickrauth.EnsureAuthenticatedForUser(photo.owner)
	groupPool.add(photo)
	print ("done")

print 'All done!'
