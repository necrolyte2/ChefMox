from paramiko import SSHClient, AutoAddPolicy, SSHConfig
from pveconfig import PVEConfig
from pveexceptions import NoFileOpenedException
import os

class PVECommand(object):
    def __init__( self, pveconfig = None ):
        """
            @param pveconfig: PVEConfig object to use. Default is to create one from scratch
            @type pveconfig: L{PVEConfig}
        """
        self._ssh_client = SSHClient()
        self._ssh_client.set_missing_host_key_policy( AutoAddPolicy() )
        if pveconfig == None:
            self.config = PVEConfig()
        else:
            self.config = pveconfig
        self.config.autoconfigure()
        self._sftp = None
        self._fh = None

    def connect( self ):
        """ Connect to the server defined in the config files """
        host = self.config.proxmox_config.get( 'cluster_master' )
        user = self.config.ssh_config.get( 'user' )
        password = self.config.ssh_config.get( 'password', None )
        key = os.path.expanduser( self.config.ssh_config.get( 'identityfile' ) )
        port = self.config.ssh_config.get( 'port', 22 )
        self._ssh_client.connect( host, port, user, password, key_filename = key )

    def ssh_command( self, command ):
        """
            Simple wrapper to run the paramiko exec_command
            @param command: Command to run on the remote server
            @type command: str

            @return: the stdin, stdout, and stderr of the executing command 
            @rtype: tuple(L{ChannelFile}, L{ChannelFile}, L{ChannelFile})
        """
        return self._ssh_client.exec_command( command )

    def _open_sftp( self ):
        """
            Helper method to keep sftp session open for entire class so we don't keep recreating it
        """
        if self._sftp == None:
            self._sftp = self._ssh_client.open_sftp()

    def send_file( self, local, dest ):
        """
            Wrapper for sftp put command
            @param local: Local file path
            @type local: str
            @param dest: Destination path for file
            @type dest: str
        """
        self._open_sftp()
        self._sftp.put( local, dest )

    def get_file( self, dest, local ):
        """
            Wrapper for sftp get command
            @param dest: Path of file to fetch
            @type dest: str
            @param local: Path to put the file locally
            @type local: str
        """
        self._open_sftp()
        self._sftp.get( dest, local )

    def open_file( self, filep, mode = 'r' ):
        """
            Wrapper for sftp open command
            @parmam filep: Path of file on remote host to open
            @type filep: str
            @param mode: File mode for open command(http://www.lag.net/paramiko/docs/paramiko.SFTPClient-class.html#open)
            @type mode: str
        """
        self._open_sftp()
        self._fh = self._sftp.open( filep, mode )

    @property
    def fh( self ):
        """
            Gives access to the file handle of the opened file if opened otherwise
            throws exception

            @return file handle
            @rtype C{file_handle}
        """
        if not self._fh == None:
            return self._fh
        raise NoFileOpenedException( "No file has been previously opened" )

    def close_file( self ):
        """
            Gives the ability to implicitly close the file
        """
        self._fh.close()

    def __del__( self ):
        try:
            self._sftp.close()
        except:
            pass
        self._ssh_client.close()
