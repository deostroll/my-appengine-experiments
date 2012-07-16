#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import oauth
import logging
from google.appengine.api import urlfetch

je = jinja2.Environment(
				loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

consumer_key = 'Osq1xe7gL1PE0mg2kUeuxw'
consumer_secret = '305fZthlfLeTxheS4x7lL9D0jV63fCXMkGnc302Y'
callback_url = ''

class MainHandler(webapp2.RequestHandler):
    def get(self):
		tl = je.get_template('login.htm')
		self.response.out.write(tl.render({}))

class twitter_redirect(webapp2.RequestHandler):
	def get(self):
		url = self.request.url
		cb = url[:url.rfind('/')] + '/oauthHandler'
		self.response.out.write(cb)
		global callback_url 
		callback_url = cb
		client = oauth.TwitterClient(consumer_key, consumer_secret, cb)
		self.redirect(client.get_authorization_url())
		
class oauthHandler(webapp2.RequestHandler):
	def get(self):
		client = oauth.TwitterClient(consumer_key, consumer_secret, callback_url)
		token = self.request.get('oauth_token')
		verifier = self.request.get('oauth_verifier')
		user_info = client.get_user_info(token, auth_verifier=verifier)
		logging.debug('THE user_info object dump: %s' % str(user_info))
		twparams = {
			'status' : 'This is hello from The Web Sink',
		
			}
		result = client.make_request(
				'http://twitter.com/statuses/update.json',
				token = user_info['token'],
				secret = user_info['secret'],
				additional_params = twparams,
				method = urlfetch.POST)		
		self.response.out.write("Posted something...")
		
app = webapp2.WSGIApplication([('/', MainHandler),
							('/redirect', twitter_redirect),
							('/oauthHandler' , oauthHandler)],
                              debug=True)
