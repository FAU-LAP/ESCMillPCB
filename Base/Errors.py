"""
Created on 21.03.2018

@author: Christian Ott
"""


class ESCError(Exception):
    """
    Base class for ESCMillPCB exceptions.
    """
    pass



class MachineError(ESCError):
    """
    Base class for machine related exceptions.
    """
    pass


class CommunicationError(MachineError):
    """
    Errors during communication with the machine.
    """
    
    def __init__(self, command, message):
        """
        Constructor

        :param str command: Command during which the error occured
        :param str message: Error message
        """
        super().__init__()
        self.command = str(command)
        self.message = str(message)
        
    def __str__(self):
        return "Communication error: {} (during {})".format(self.message, self.command)
    
    
    
class ImplementationMissing(ESCError):
    """
    This error is emitted when an "abstract" base class method is called which is
    mandatory to be overridden or if the implementation of the method is still missing.
    """
    
    def __init__(self, methodname):
        """
        Constructor

        :param str methodname: Method with missing implementation
        """
        super().__init__()
        self.methodname = methodname
        
    def __str__(self):
        return "Method not implemented: " + self.methodname
    
    
class InvalidArgument(ESCError):
    """
    Emitted if a function argument is invalid.
    """
    
    def __init__(self, argument, description):
        """
        Constructor

        :param str argument: Name of invalid argument
        :param str description: Error description
        """
        super().__init__()
        self.argument = argument
        self.description = description
        
    def __str__(self):
        return "Invalid argument: {} ({})".format(self.argument, self.description)