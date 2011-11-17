import yaml

def write_config( file_name, contents ):
    with open( file_name, 'w+' ) as fh:
        fh.write( contents )

def read_test_config( ):
    with open( test_config ) as fh:
        return yaml.load( fh.read() )
