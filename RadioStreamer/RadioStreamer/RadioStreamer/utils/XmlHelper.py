import xml.etree.ElementTree as ET
import xml.dom.minidom as xmlDom
import os.path

from  RadioStreamer.database.services.dbServices import dbServices
import urllib2


class XmlHelper(object):
    """Class for handling additional xml file with user designed stations"""

    def __init__(self, userName = ""):
        """Initialize"""

        # Prepare file, if it does not exists
        self.__filePath = "./RadioStreamer/user_data/privateChannels_" + userName + ".xml"

        if os.path.isfile(self.__filePath) == False:
            file = open(self.__filePath, 'a')
            file.write("<PrivateChannels>\n</PrivateChannels>")
            file.close()

        # Create XML objects
        parser = ET.XMLParser(encoding = "utf-8")
        self.__xml = ET.parse(self.__filePath, parser = parser)
        self.__root = self.__xml.getroot()

    def readAllChannels(self):
        """Return collection of all stations names"""

        channelNames = []
        for child in self.__root:
            channelNames.append( child.attrib['name'] )

        return channelNames

    def getStreamUrl(self, channelName = ""):
        """Return stream Url for given channel"""

        for child in self.__root:
            if child.attrib['name'] == channelName:
                return child.attrib['streamUrl']

        return ""

    def appendNewChannel(self, channelName = "", siteUrl = "", streamUrl = ""):
        """Append new channel to file,  validation here. Return True if append is successful."""
        
        # Check if channel exists locally in file
        for child in self.__root:
            if (child.attrib['name'] == channelName or child.attrib['siteUrl'] == siteUrl or child.attrib['streamUrl'] == streamUrl):
                return False

        # Check if channel exists in database
        db = dbServices();
        if (db.check_channel_exists(channelName, siteUrl, streamUrl) == True):
            return False

        # Check URLs
        try:
            hostAddress = self.__processUrl(siteUrl)
            status = urllib2.urlopen(hostAddress)
                        
            hostAddress = self.__processUrl(streamUrl)
            status = urllib2.urlopen(hostAddress)
        except Exception as e:
            print "Page not found"
            return False

		# Add channel to file
        newElem = ET.Element("Channel")
        newElem.set("name", channelName)
        newElem.set("siteUrl", siteUrl)
        newElem.set("streamUrl", streamUrl)

        self.__root.append(newElem)
        #self.__xml.write('./RadioStreamer/user_data/privateChannels.xml')

        prettyXml = self.__prettifyXml(self.__root)
        file = open(self.__filePath, "wb")
        file.write(prettyXml)
        file.close()

        return True

	# Processes URL to optionally add "http://" prefix
    def __processUrl(self, url):        
        if url.startswith('http://') == False:
            url = "http://" + url

        return url

    # Return a pretty-printed XML string for the Element.
    def __prettifyXml(self, root):
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = xmlDom.parseString(rough_string)

        uglyXml = reparsed.toprettyxml(indent="\t")

        # pretty xml has a ton of unnecessary newline characters (which is not pretty)
        lines = uglyXml.split('\n')
        lines = [l for l in lines if (l != '\t' and l != '')]

        prettyXml = ""
        for line in lines:
            prettyXml += line + '\n'

        return prettyXml