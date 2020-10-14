from PyQt5 import QtGui, QtCore
from Models.Anchor import Anchor

class Model(object):

    """ Holds information about the models of the app. 
        UI elements subscribe to listen for updates, triggering specific functions when announcing an update of the models. 
        
        Attributes:
            _update_funcs               The functions that have to be called.
            anchor1, anchor2            The anchor points of the projection.
    """

    def __init__(self):
        
        self._update_funcs = []
        
        self.anchor1 = Anchor(0, 0, 90, -180)
        self.anchor2 = Anchor(0, 0, -90, 180)

        self.anchor1.modelChanged.connect(self.announce_update)
        self.anchor2.modelChanged.connect(self.announce_update)

    def subscribe_update_func(self, func):
        
        """ Adds the specified function to the list of functions to be called. """
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    def unsubscribe_update_func(self, func):
        
        """ Removes the specified function from the list. """
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    def announce_update(self):
        
        """ Whenn announcing an update of the models, call every function that is subscribed. """
        for func in self._update_funcs:
            func()

