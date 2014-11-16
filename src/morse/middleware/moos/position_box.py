import logging; logger = logging.getLogger("morse." + __name__)
import pymoos.MOOSCommClient
from morse.middleware.moos import AbstractMOOS
from morse.core import blenderapi

class PositionBoxReader(AbstractMOOS):
    """ Read commands and update local data. """

    def initialize(self):
        AbstractMOOS.initialize(self)
        # register for position variables from the database
        self.m.Register("posboxX")
        self.m.Register("posboxY")
        self.m.Register("posboxZ")
        self.m.Register("posboxLength")
        self.m.Register("posboxWidth")
        self.m.Register("posboxHeight")

    def default(self, ci='unused'):
        current_time = pymoos.MOOSCommClient.MOOSTime()
        # get latest mail from the MOOS comm client
        messages = self.getRecentMail()

        new_information = False

        # look for position messages
        for message in messages:
            # position box X position [m]
            if (message.GetKey() == "posboxX") and (message.IsDouble()):
                self.data['posbox_x'] = message.GetDouble() 
                new_information = True
            # position box Y position [m]
            elif (message.GetKey() == "posboxY") and (message.IsDouble()):
                self.data['posbox_y'] = message.GetDouble()
                new_information = True
            # position box Z position [m]
            elif (message.GetKey() == "posboxZ") and (message.IsDouble()):
                self.data['posbox_z'] = message.GetDouble()
                new_information = True
            # position box length
            elif (message.GetKey() == "posboxLength") and (message.IsDouble()):
                self.data['posbox_l'] = message.GetDouble()
                new_information = True
            # position box width
            elif (message.GetKey() == "posboxWidth") and (message.IsDouble()):
                self.data['posbox_w'] = message.GetDouble()
                new_information = True
            # position box height
            elif (message.GetKey() == "posboxHeight") and (message.IsDouble()):
                self.data['posbox_h'] = message.GetDouble()
                new_information = True

        return new_information