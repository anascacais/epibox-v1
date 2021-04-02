class Sense(object):

    def __init__(self, macAddress):
        self.macAddress = macAddress
        version = self.version()
        
    def version(self):
        return 'ScientISST'
