class XmlHelper(object):
	"""Class for handling additional xml file with user designed stations"""

	def __init__(self):
		"""Initialize"""

	def readAllChannels(self):
		"""Return collection of all stations names"""

		return None;

	def getChannelUrl(self, channelName):
		"""Return stream Url for given channel"""

		return None;

	def appendNewChannel(self, channelName, siteUrl, streamUrl):
		"""Append new channel to file,  validation here. Return True if append is successful."""
		
		# To check: if name already exist (file/database), if url is valid (send HttpRequest)

		return False;