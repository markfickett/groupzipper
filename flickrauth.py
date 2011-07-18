"""
Authenticate for write access.
Manage authentication for multiple users, interleaved.
Based on: http://code.google.com/p/flickrpy/wiki/UserAuthentication
"""

import os
import flickr
import secret

permission = "write"

def EnsureAuthenticatedForUser(user):
	"""
	Ensure that the flickr module is authenticated the given user.
	This looks for token_<user NSID>.txt and, if it's not found,
	generates a URL to visit to auth. If the token file exists, set flickr
	variables to use it.
	"""
	tokenFileName = __GetTokenFileName(user)
	if not os.path.isfile(tokenFileName):
		print "'%s' not found, authenticating." % tokenFileName
		token = __AuthenticateForUser(user)
		with open(tokenFileName, "w") as tokenFile:
			tokenFile.write(token)
	flickr.tokenFile = tokenFileName

def __GetTokenFileName(user):
	return 'token_%s.txt' % user.id

def __AuthenticateForUser(user):
	auth = flickr.Auth()
	frob = auth.getFrob()
	link = auth.loginLink(permission, frob)

	raw_input(("Log in to flickr as %s (ID = %s), "
		+ "then visit this URL and allow access: %s")
		% (user.username, user.id, link))

	return auth.getToken(frob)

