"""
Zip a number of flickr sets to a group pool, resulting in a group pool ordered
by photo capture time, oldest first.
"""

import flickr
import flickrauth
import secret
import sys


###
# Set the IDs of the sets from which photos will be drawn, and the group
# to which they will be added. (Make sure photo timestamps are synchronized!)

# A list of set IDs. If your set is at
#	flickr.com/photos/markfickett/sets/72157627035346247/
# then the ID is 72157627035346247 .
# For example:
# setIds = [
#	'12357627035346247',
#	'45657627035346247',
# ]
setIds = [
]

# The ID of the group to which the photos should be added. If your group is at
#	http://www.flickr.com/groups/1738107@N21/
# then the ID is 1738107@N21 .
# For example:
# groupId = '5678107@N21'
groupId = ''

# Create secret.py with your API key information. For example, the contents
# might look like:
# API_KEY = '5958788e232dc888244f97e4543f974d'
# API_SECRET = 'bcd9e28f8ba3d8bf'

# No need to edit below here for default usage.
###

flickr.API_KEY = secret.API_KEY
flickr.API_SECRET = secret.API_SECRET

def cmpPhotosByDateTakenAsc(a, b):
	"""
	Sort older photos first, according to the datetaken field.
	To reverse the order, switch a.datetaken and b.datetaken below.
	(datetaken is different from the 'date time original' EXIF data field,
	and can be edited in flickr. In batch mode ('organize and create'),
	there is an option to batch adjust for time zone offsets.)
	"""
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
