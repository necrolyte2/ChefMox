from subprocess import Popen, PIPE, call, STDOUT
import os

class MissingSoftwareException( Exception ):
    """ Missing software exception"""

class vmbuilder:
    def __init__( self, hypervisor = 'kvm', distro = 'ubuntu', options = None, vmbuilder_path = '/usr/bin/vmbuilder' ):
        """
            PARAMS:
             - options should be a dictionary keyed by the same options that vmbuilder uses. The only exception is
                addpkg which the value is a list of additional packages to install to the base system
             - hypervisor is one of the following kvm, xen, vmw6, vmserver
             - distro can only have the value of ubuntu as of right now
             - vmbuilder_path is the path to the vmbuilder executable
        """
        self.hypervisor = 'kvm'
        self.distro = 'ubuntu'
        if not options:
            self.opts = { 
                 'rootsize': '8192',
                 'swapsize': '2048',
                 'suit': 'lucid',
                 'flavour': 'virtual',
                 'variant': 'minbase',
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
        return os.getuid() == 0

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

    def vm_image_path( self ):
        base_path = os.path.abspath( '.' )
        vm_path = os.path.join( base_path, 'ubuntu-kvm' )
        files = os.listdir( vm_path )
        vm_name = ''
        for f in files:
            if os.path.splitext( f )[1] == '.qcow2':
                vm_name = f
        return os.path.join( vm_path, vm_name )

    def setOpt( self, opt, value ):
        self.opts[opt] = value

    def get_build_command( self ):
        return [self.vmbuilder_path, self.hypervisor, self.distro] + self._build_opts( )

    def build_vm( self ):
        if not self._isRoot( ):
            raise
        p = Popen( self.get_build_command(), stdout = PIPE, stderr = STDOUT )
        return p
