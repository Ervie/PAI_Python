import threading
import urllib2

class MetadataWorker(object):
    """Class for sending HttpRequest to streams asking for metadata"""

    def __init__(self):
        """Initialize"""

    def startWorking(self):
       return threading.Timer(5.0, sendRequest("")).start()


    def sendRequest(self, requestUrl):

        request = urllib2.Request(requestUrl)

        try:
            request.add_header('Icy-MetaData', 1)
            response = urllib2.urlopen(request)
            icy_metaint_header = response.headers.get('icy-metaint')

            if icy_metaint_header is not None:
                metaint = int(icy_metaint_header)
                read_buffer = metaint+255
                content = response.read(read_buffer)
                title = content[metaint:].split("'")[1]
                return title
        except:
            return ""


