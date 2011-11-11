from pyvmbuilder import vmbuilder
import os
import sys

def buildvm( ):
    builder = vmbuilder( )
    builder.setOpt( 'mirror', 'http://ubuntu.osuosl.org/ubuntu' )
    builder.setOpt( 'user', 'install' )
    builder.setOpt( 'pass', '123457' )
    builder.setOpt( 'hostname', 'acg01' )
    builder.setOpt( 'domain', 'msu.montana.edu' )
    builder.setOpt( 'ip', '153.90.237.133' )
    builder.setOpt( 'gw', '153.90.237.254' )
    builder.setOpt( 'destdir', 'acg01' )
    try:
        p = vmbuilder().build_vm()
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
