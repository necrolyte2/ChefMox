from subprocess import Popen, PIPE, call
import os

class MissingSoftwareException( Exception ):
    """ Missing software exception"""

class vmbuilder:
    def __init__( self, hypervisor = 'kvm', distro = 'ubuntu', options = None, vmbuilder_path = '/usr/bin/vmbuilder' ):
        """
        sudo vmbuilder kvm ubuntu \
        --rootsize=$((1024*8)) \
        --swapsize=$((2*1024)) \
        --user=install \
        --pass=123457 \
        --suit=lucid \
        --flavour=virtual \
        --variant=minbase \
        --mirror=http://ubuntu.osuosl.org/ubuntu \
        --arch=i386 \
        --hostname=acg01 \
        --domain=msu.montana.edu \
        --ip=153.90.237.133 \
        --gw=153.90.237.254 \
        --mask=255.255.254.0 \
        --addpkg=sudo \
        --addpkg=acpid \
        --timezone=America/Denver
        """
        self.hypervisor = 'kvm'
        self.distro = 'ubuntu'
        if not options:
            self.opts = { 
                 'rootsize': '8192',
                 'swapsize': '2048',
                 'user': 'install',
                 'pass': '123457',
                 'suit': 'lucid',
                 'flavour': 'virtual',
                 'variant': 'minbase',
                 'mirror': 'http://ubuntu.osuosl.org/ubuntu',
                 'arch': 'i386',
                 'addpkg': ['sudo', 'acpid'],
                 'timezone': 'America/Denver',
                }
        else:
            self.opts = options

        self.vmbuilder_path = vmbuilder_path
        if not self._is_vmbuilder_installed( ):
            raise MissingSoftwareException( "vm builder is not installed or you need to set the path to it" )

    def _is_vmbuilder_installed( self ):
        return os.path.exists( self.vmbuilder_path )

    def _isRoot( self ):
        return os.getlogin() == 'root'

    def _build_opts( self ):
        """
            Returns the option list in the correct format
        """
        opts = []
        for k,v in self.opts.items():
            if not k == 'addpkg':
                opts.append( "--%s=%s" % (k,v) )
            else:
                for pkg in v:
                    opts.append( "--%s=%s" % (k,pkg) )
        return opts

    def setOpt( self, opt, value ):
        self.opts[opt] = value

    def get_build_command( self ):
        return [self.vmbuilder_path, self.hypervisor, self.distro] + self._build_opts( )

    def build_vm( self ):
        p = Popen( self.get_build_command(), stdout = PIPE, stderr = PIPE )
        return p.communicate()
