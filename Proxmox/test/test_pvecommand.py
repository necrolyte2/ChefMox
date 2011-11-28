import unittest
import sys
# I know this is bad, but I'm tired of trying to figure out the better way to do it
sys.path.append( '../' )
from pvecommand import PVECommand
from clustercfg import ClusterCfg
from pveconfig import PVEConfig
from test_pveconfig import BaseProxmoxTest, BaseSSHTest
from config import test_config
from pveexceptions import *

class TestBase( unittest.TestCase ):
    def setUp( self ):
        self.pvecfg = PVEConfig( test_config.proxmox_config ) 

class TestPVECommand( TestBase ):
    def setUp( self ):
        super( TestPVECommand, self ).setUp( )
        self.command = PVECommand( self.pvecfg )
        
    def test_connect( self ):
        self.command.connect()

    def test_fileopened( self ):
        # Not sure how to test this right now
        pass

    def test_nofileopened( self ):
        flag = False
        try:
            self.command.fh
        except NoFileOpenedException:
            flag = True
        self.assertTrue( flag )

class TestClusterCfgLocal( unittest.TestCase ):
    def setUp( self ):
        self.pvecfg = PVEConfig( test_config.proxmox_config_fixture ) 
        self.cfg = ClusterCfg( self.pvecfg )

    def test_read_cluster_config( self ):
        # Make sure the config was fully parsed
        self.cfg._read_cluster_config()
        cfg = self.cfg._cluster_config
        self.assertTrue( cfg['maxcid'] == 3 )
        self.assertTrue( type( cfg[3] ) == type( dict() ) )
        self.assertTrue( cfg[3]['NAME'] == 'host3' )
        self.assertTrue( cfg[3]['IP'] == '1.1.1.3' )

    def test_cluster_config( self ):
        # Ensure the cluster_config property works properly
        cfg = self.cfg.cluster_config
        self.assertTrue( cfg['maxcid'] == 3 )
        self.assertTrue( type( cfg[3] ) == type( dict() ) )
        self.assertTrue( cfg[3]['NAME'] == 'host3' )
        self.assertTrue( cfg[3]['IP'] == '1.1.1.3' )

class TestClusterCfgRemote( unittest.TestCase ):
    def setUp( self ):
        self.pvecfg = PVEConfig( test_config.proxmox_config ) 
        self.cfg = ClusterCfg( self.pvecfg )

    def test_read_cluster_config( self ):
        # Make sure the config was fully parsed
        self.cfg._read_cluster_config()
        cfg = self.cfg._cluster_config
        self.failIf( cfg['maxcid'] == None )
        self.assertTrue( type( cfg[1] ) == type( dict() ) )
        self.failIf( cfg[1]['NAME'] == '' )
        self.assertTrue( cfg[1]['IP'].count( '.' ) == 3 )

    def test_cluster_config( self ):
        # Ensure the cluster_config property works properly
        cfg = self.cfg.cluster_config
        self.failIf( cfg['maxcid'] == None )
        self.assertTrue( type( cfg[1] ) == type( dict() ) )
        self.failIf( cfg[1]['NAME'] == '' )
        self.assertTrue( cfg[1]['IP'].count( '.' ) == 3 )

if __name__ == '__main__':
    pvecmd = unittest.TestLoader().loadTestsFromTestCase( TestPVECommand )
    cluscfglocal = unittest.TestLoader().loadTestsFromTestCase( TestClusterCfgLocal )
    cluscfgremote = unittest.TestLoader().loadTestsFromTestCase( TestClusterCfgRemote )
    suits = {'pvecmd':pvecmd,'cluscfglocal':cluscfglocal,'cluscfgremote':cluscfgremote}
    if len( sys.argv ) == 1:
        suit = unittest.TestSuite( suits.values() )
    elif sys.argv[1] == 'pvecmd':
        suit = pvecmd
    elif sys.argv[1] == 'cluscfglocal':
        suit = cluscfglocal
    elif sys.argv[1] == 'cluscfgremote':
        suit = cluscfgremote
    else:
        print "Please specify a valid test suit from the following:\n %s" % "\n ".join( suits.keys() )
        sys.exit( 0 ) 
    unittest.TextTestRunner().run( suit )
