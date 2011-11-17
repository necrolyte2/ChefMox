from paramiko import SSHClient, AutoAddPolicy, SSHConfig
from pveexceptions import MissingConfigurationFile
import yaml
import os

class PVEConfig:
    def __init__( self, main_config = '/etc/chefmox/config/proxmox.cfg' ):
        """
            Setup the configuration for Proxmox Commands
            @param main_config: location of the main config file
            @type main_config: str
        """
        self.main_config = main_config
        self._ssh_config = {}
        self._proxmox_config = {}

    def autoconfigure( self ):
        """
            Reads all of the configuration values from various config files
            assuming they are all in their default locations
        """
        self.read_proxmox_config( self.main_config )
        self.read_ssh_config( self.proxmox_config['cluster_master'], self.proxmox_config['ssh_config_file'] )

    def read_proxmox_config( self, cnf_file = '/etc/chefmox/config/proxmox.cfg' ):
        """
            Read the proxmox configuration which should be yaml formatted
            @param cnf_file: The configuration file to read
            @type cnf_file: str
        """
        if os.path.exists( cnf_file ):
            with open( cnf_file ) as fh:
                self._proxmox_config = yaml.load( fh.read() )
        else:
            raise MissingConfigurationFile( cnf_file )

    @property
    def proxmox_config( self ):
        return self._get_config( self._proxmox_config )

    def set_proxmox_config_opt( self, opt, value ):
        self._proxmox_config[opt] = value

    def read_ssh_config( self, hostname, cnf_file = '~/.ssh/config' ):
        """
            Read an ssh config file and store it in this class
            @param cnf_file: The configuration file for ssh
            @type cnf_file: str
            @raise MissingConfigurationFile: If the file does not exist
        """
        cnf_file = os.path.expanduser( cnf_file )
        if os.path.exists( cnf_file ):
            with open( cnf_file ) as fh:
                ssh_config = SSHConfig()
                ssh_config.parse( fh )
                self._ssh_config = ssh_config.lookup( hostname )
        else:
            raise MissingConfigurationFile( cnf_file )

    def set_ssh_config_opt( self, opt, value ):
        """
            Provide a way to set the ssh config options
            @param opt: Option name
            @type opt: str
            @param value: Value of the option
            @type value: C{str} or C{sequence}
        """
        self._ssh_config[opt] = value

    @property
    def ssh_config( self ):
        return self._get_config( self._ssh_config )
        
    def _get_config( self, config ):
        """
            Get the ssh config.
            @param config: Which configuration to get
            @type config: L{dict}
        """
        # Returns the dictionary with lowercase keys
        return dict( zip( map( lambda x: x.lower(), config.keys() ), config.values() ) )
