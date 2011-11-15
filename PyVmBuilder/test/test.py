from ..pyvmbuilder import vmbuilder
import os
import sys

def buildvm( ):
    builder = vmbuilder( )
    builder.setOpt( 'mirror', 'http://ubuntu.osuosl.org/ubuntu' )
    builder.setOpt( 'user', 'install' )
    builder.setOpt( 'pass', 'password' )
    builder.setOpt( 'hostname', 'ubuntu-01' )
    builder.setOpt( 'domain', 'example.com' )
    builder.setOpt( 'ip', '1.1.1.2' )
    builder.setOpt( 'gw', '1.1.1.1' )
    builder.setOpt( 'dest', 'some-dest-folder' )
    builder.setOpt( 'timezone', 'America/Denver' )
    try:
        p = builder.build_vm()
    except Exception as e:
        print "Make sure you run as root"
        print e
        sys.exit( -1 )
    for line in iter( p.stdout.readline, ''):
        print line
    p.stdout.close()
    return builder.vm_image_path()

if __name__ == '__main__':
    print buildvm( )
