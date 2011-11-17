#!/usr/bin/env pythonfrom distutils.core import setup

setup( name='pyProxmox',
      version='0.1.0',
      description='Python Wrapper for Proxmox commands',
      author='Tyghe Vallard',
      author_email='vallardt@gmail.com',
      package_dir={'pyproxmox':''},
      packages=['pyproxmox'],
      requires=['pyyaml']
    )
