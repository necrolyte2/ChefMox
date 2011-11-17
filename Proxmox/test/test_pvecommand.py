import unittest
import sys
# I know this is bad, but I'm tired of trying to figure out the better way to do it
sys.path.append( '../' )
from pvecommand import PVECommand
from clustercfg import ClusterCfg
from pveconfig import PVEConfig
from test_pveconfig import BaseProxmoxTest, BaseSSHTest
from config import test_config

class TestBase( unittest.TestCase ):
    def setUp( self ):
        self.pvecfg = PVEConfig( test_config.proxmox_config ) 

class TestPVECommand( TestBase ):
    def setUp( self ):
        super( TestPVECommand, self ).setUp( )
        self.command = PVECommand( self.pvecfg )
        
    def test_connect( self ):
        self.command.connect()

class TestClusterCfg( TestBase ):
    def setUp( self ):
        super( TestClusterCfg, self ).setUp( )
        self.cfg = ClusterCfg( self.pvecfg )

    def test_read_cluster_config( self ):
        # Make sure the config was fully parsed
        cfg = self.cfg._read_cluster_config()
        self.assertTrue( cfg['maxcid'] == 3 )
        self.assertTrue( type( cfg[3] ) == type( dict() ) )
        self.assertTrue( cfg[3]['NAME'] == 'host3' )
        self.assertTrue( cfg[3]['IP'] == '1.1.1.3' )

if __name__ == '__main__':
    pvecmd = unittest.TestLoader().loadTestsFromTestCase( TestPVECommand )
    cluscfg = unittest.TestLoader().loadTestsFromTestCase( TestClusterCfg )
    suits = {'pvecmd':pvecmd,'cluscfg':cluscfg,}
    if len( sys.argv ) == 1:
        suit = unittest.TestSuite( suits.values() )
    elif sys.argv[1] == 'pvecmd':
        suit = pvecmd
    elif sys.argv[1] == 'cluscfg':
        suit = cluscfg
    else:
        print "Please specify a valid test suit from the following:\n %s" % "\n ".join( suits.keys() )
        sys.exit( 0 ) 
    unittest.TextTestRunner().run( suit )
