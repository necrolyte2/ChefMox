class MissingConfigurationFile( Exception ):
    def __init__( self, value ):
        self.value = value
    
    def __str__( self ):
        return "The file %s is missing or permission denied when accessed" % self.value

class NoFileOpenedException( Exception ):
    def __init__( self, value ):
        self.value = value
    
    def __str__( self ):
        return self.value
