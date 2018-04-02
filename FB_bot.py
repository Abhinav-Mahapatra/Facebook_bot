from fbchat import  Client, log
from fbchat.models import *
import apiai, codecs, json

Facebook_email_id = "<Your Facebook Email Id>"
Facebook_Password = "<Your Facebook Password>"

class Jarvis(Client):

    # Connect to dialogflow
    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "52d7a3d5d864415382df5a72cfb97ae9"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'de' #Default : English
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"


    def onMessage(self, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        # Mark message as read
        self.markAsRead(author_id)

        # Print info on console
        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))

        # Establish conn
        self.apiaiCon()

        # Message Text
        msgText = message_object.text

        # Request query/reply for the msg received
        self.request.query = msgText

        # Get the response which is a json object
        response = self.request.getresponse()

        # Convert json obect to a list
        obj = json.load(response)

        # Get reply from the list
        reply = obj['result']['fulfillment']['speech']

        # Send message
        if author_id!=self.uid:
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

        # Mark message as delivered
        self.markAsDelivered(author_id, thread_id)


# Create an object of our class, enter your email and password for facebook.
client = Jarvis(Facebook_email_id, Facebook_Password)

# Listen for new message
client.listen()
