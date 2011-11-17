import unittest
import sys
# I know this is bad, but I'm tired of trying to figure out the better way to do it
sys.path.append( '../' )
import os
from pveconfig import PVEConfig
from pveexceptions import MissingConfigurationFile
from util import read_test_config
from config import test_config

class BaseTest( unittest.TestCase ):
    def setUp( self ):
        self.config = PVEConfig()

class BaseSSHTest( BaseTest ):
    def setUp( self, *args, **kwargs ):
        super( BaseSSHTest, self ).setUp( *args, **kwargs )
        self.temp_config = test_config.ssh_config_fixture

class TestSSHReadConfig( BaseSSHTest ):
    def test_missing_config_file( self ):
        # Make sure the correct exception is thrown if missing config file
        self.assertRaises( MissingConfigurationFile, self.config.read_ssh_config, 'nohost','none123457' )

    def test_has_config_file( self ):
        # Make sure that no exception is thrown if config file exists and that the configis a dictionary object
        self.config.read_ssh_config( 'testhost', self.temp_config )
        self.assertTrue( type( self.config.ssh_config ) == type( {} ) )

    def test_sshread_lookup( self ):
        # Make sure that we can lookup values in the ssh config
        self.config.read_ssh_config( 'master.example.com', self.temp_config )
        ssh_config = self.config.ssh_config
        self.assertTrue( ssh_config['user'] == 'testuser', "Config: %s" % ssh_config )
        self.assertTrue( ssh_config['identityfile'] == '~/.ssh/id_dsa', "Config: %s" % ssh_config )

class TestSSHSetConfig( BaseSSHTest ):
    def test_sshset_lookup( self ):
        # Make sure that we can lookup values in the ssh config
        self.config.set_ssh_config_opt( 'User', 'testuser' )
        self.config.set_ssh_config_opt( 'IdentityFile', '~/.ssh/id_dsa' )
        ssh_config = self.config.ssh_config
        self.assertTrue( ssh_config['user'] == 'testuser', ssh_config )
        self.assertTrue( ssh_config['identityfile'] == '~/.ssh/id_dsa', ssh_config )

class BaseProxmoxTest( BaseTest ):
    def setUp( self, *args, **kwargs ):
        super( BaseProxmoxTest, self ).setUp( *args, **kwargs )
        self.temp_config = test_config.proxmox_config_fixture

class TestProxmoxReadConfig( BaseProxmoxTest ):
    def test_read_missing_file( self ):
        # Assert that if the proxmox config file is missing it will raise an error
        self.assertRaises( MissingConfigurationFile, self.config.read_proxmox_config, 'no_file_here' )

    def test_read_missing_file( self ):
        # Assert that if the proxmox config file is missing it will raise an error
        self.config.read_proxmox_config( self.temp_config )
        config = self.config.proxmox_config
        self.assertTrue( config['cluster_master'] == 'master.example.com' )

class TestProxmoxSetConfig( BaseProxmoxTest ):
    def test_set_get_config( self ):
        # Ensure we can set and retrieve options and that the opt value is returned lowercased
        self.config.set_proxmox_config_opt( 'Cluster_master', 'test.example.com' )
        option = self.proxmox_config
        self.assertTrue( option.get( 'cluster_master' ) == 'test.example.com' )

class PveAutoConfigureTest( unittest.TestCase ):
    def setUp( self ):
        # Write our test config files
        self.pve_cfg = test_config.proxmox_config_fixture
        self.ssh_cfg = test_config.ssh_config_fixture
        self.config = PVEConfig( self.pve_cfg )

    def test_autoconfigure( self ):
        # Make sure autoconfigure works correctly
        self.config.autoconfigure()
        self.assertTrue( self.config.ssh_config['user'], 'testuser' )

if __name__ == '__main__':
    sshreadsuit = unittest.TestLoader().loadTestsFromTestCase( TestSSHReadConfig )
    sshsetsuit = unittest.TestLoader().loadTestsFromTestCase( TestSSHSetConfig )
    pvereadsuit = unittest.TestLoader().loadTestsFromTestCase( TestProxmoxReadConfig )
    pveautoconfigure = unittest.TestLoader().loadTestsFromTestCase( PveAutoConfigureTest )
    if len( sys.argv ) == 1:
        suit = unittest.TestSuite( [sshreadsuit, sshsetsuit, pvereadsuit, pveautoconfigure] )
    elif sys.argv[1] == 'sshread':
        suit = sshreadsuit
    elif sys.argv[1] == 'sshset':
        suit = sshsetsuit
    elif sys.argv[1] == 'pveread':
        suit = pvereadsuit
    elif sys.argv[1] == 'autoconfigure':
        suit = pveautoconfigure
    else:
        print "Please specify a valid test suit to run"
        sys.exit( 0 )
    unittest.TextTestRunner().run( suit )

