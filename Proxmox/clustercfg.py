from pvecommand import PVECommand

class ClusterCfg( PVECommand ):
    def __init__( self, *args, **kwargs ):
        """
            Call super and connect the client
        """
        super( ClusterCfg, self ).__init__( *args, **kwargs )

    def _read_cluster_config( self ):
        """
            Reads the cluster config file from either locally or remote host

            @return A dictionary containing the cluster.cfg
            @rtype dict
        """
        cfg = None
        cfg_path = self.config.proxmox_config.get( 'pve_config' )
        # Is the file local or remote
        if cfg_path:
            with open( cfg_path ) as fh:
                cfg = fh.readlines()
        else:
            # We will need to connect to do this operation
            self.connect()
            with self.open_file( '/etc/pve/cluster.cfg' ) as fh:
                cfg = fh.readlines()

        # Strip the newlines from each entry and return the parsed dict
        return self._parse_cluster_config( [x.strip() for x in cfg] )

    def _parse_cluster_config( self, cfg ):
        """
            Parse a Proxmox cluster.cfg file into a dictionary
            @param cfg: Contents of a cluster.cfg file as a list
            @type cfg: list

            @return: Dictionary containing the elements from the cfg cluster.cfg file
            @rtype: dict
        """
        ret_dict = { 'maxcid' : int( cfg[0].split()[1] ) }
        cur_key = ''
        for line in cfg:
            if line == '' or line.startswith( 'maxcid' ):
                pass
            elif line.endswith( '}' ):
                cur_key = ''
            elif line.endswith( '{' ):
                node, cid, ignore = line.split( ' ', 2 )
                cur_key = int( cid )
                ret_dict[cur_key] = { 'cid': int( cid ) }
            else:
                key, val = line.replace( ' ', '' ).split( ':' )
                ret_dict[cur_key][key] = val

        return ret_dict
