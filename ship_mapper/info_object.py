class info:
    """
    info class makes and 'info object' which contains all the metadata
    needed to run a project.
    """
    
    
    def __init__(self, calling_file='.', run_name='auto', dir_data_original=None, grid_type=None):
        '''
        Initializes an "info" object
        '''
        import os
        from pathlib import Path
        from types import SimpleNamespace
        
        if calling_file == None:
            self.project_name = ''
        else:
            self.project_name = os.path.split(os.path.split(calling_file)[0])[1]
        
        if run_name == 'auto':
            self.run_name = os.path.split(calling_file)[1][:-3]
        else:
            self.run_name = run_name
        
        project_path = Path(os.path.split(calling_file)[0])

        dirs = {}  
        dirs['top'] = os.path.abspath(os.path.join(os.path.dirname( calling_file ), '../..'))
        dirs['project_path'] = Path(project_path)
        
        if dir_data_original != None:
            dirs['data_original'] = Path(dir_data_original)
            dirs['data_nc'] = Path(dir_data_original.replace('data_original', 'data_nc'))
        else:
            dirs['data_original'] = None
            dirs['data_nc'] = None          
        
        dirs['ancillary'] = Path(project_path / 'ancillary')
        dirs['gridded_data'] = Path(project_path / 'gridded_data')
        dirs['merged_grid'] = Path(project_path / 'merged_grid')
        dirs['pngs'] = Path(project_path / 'pngs')
        dirs['shapefiles'] = Path(project_path / 'shapefiles')
        
        grid ={}
        grid['region'] = None
        grid['basemap'] = None
        grid['type'] = None    
        grid['bin_number'] = None
        grid['minlat'] = None
        grid['maxlat'] = None
        grid['minlon'] = None
        grid['maxlon'] = None
        grid['interp_threshold'] = 40 #knots
        grid['time_bin'] = 10 #minutes
        grid['epsg_code'] = None
        grid['areas'] = None
        
        filt ={}
        filt['speed_low'] = None
        filt['speed_high'] = None
        
        maps = {}
        maps['mask_below'] = 1
        maps['scalebar_km'] = 100
        maps['title'] = 'auto'
        maps['resolution'] = 'i'
        maps['parallels'] = 1 # Deegres between lines
        maps['meridians'] = 1# Deegres between lines
        
        sidebar = {}
        sidebar['units'] = ''
        sidebar['unit_description'] = ''
        sidebar['data_source'] = ''
        sidebar['data_description'] = ''
        sidebar['time_range'] = ''
        sidebar['included_speeds'] = 'All'
        sidebar['interpolation'] = 'Linear'
        sidebar['interpolation_threshold'] = ''
        sidebar['time_bin'] = 10
        
        self.grid = SimpleNamespace(**grid)
        self.filt = SimpleNamespace(**filt)
        self.dirs = SimpleNamespace(**dirs)
        self.maps = SimpleNamespace(**maps)
        self.sidebar = SimpleNamespace(**sidebar)
        return

    
    
    def __repr__(self):
        '''
        Prints "info" to screen
        '''
        import types
        to_screen = ''    
        for row in self.__dict__.keys():
            if type(self.__dict__[row]) != types.SimpleNamespace:
                to_screen = to_screen + row + ': ' + str(self.__dict__[row]) + '\n'
            if type(self.__dict__[row]) == types.SimpleNamespace:
                to_screen = to_screen + row + '\n'
                for subrow in self.__dict__[row].__dict__.keys():
                    to_screen = to_screen + '    ' + subrow + ': ' + str(self.__dict__[row].__dict__[subrow]) + '\n'
        return to_screen  
        
    
    
    
    def save(self):
        '''
        Saves info into pickle
        '''
        import _pickle as pickle
        import os
        import ship_mapper as sm
        
        sm.checkDir(str(self.dirs.ancillary))
        full_filename = os.path.join(self.dirs.ancillary, 'info_' + self.run_name + '.p')
        
        pickle.dump(self,open(full_filename,'wb'),-1)
        print('!!! Pickle info.p file just got saved ')
        return
    
    
    
    
    
    
def load_info(run_name, path_to_info=None):
    '''
    Loads "info" file
    
    Input is full-path to a info.p file or, 
    if None, it will look for ./ancillary/info.p

    '''
    import _pickle as pickle
    import os
    from pathlib import Path
    import inspect
    
##    inspect.stack()
    print('-----------------')
    print(inspect.stack()[1][1])
    print('-----------------')
    print(os.path.split(inspect.stack()[1][1])[0])
    
    calling_path = Path(os.path.split(inspect.stack()[1][1])[0])
    
    if path_to_info == None:
        info_file = os.path.abspath(os.path.join(calling_path, 'ancillary','info_' + run_name + '.p'))
    elif os.path.isdir(path_to_info):
        info_file = os.path.abspath(os.path.join(os.path.dirname( path_to_info ), 'ancillary','info_' + run_name + '.p'))
      
    info = pickle.load(open(info_file,'rb'))
    return info

    

def grid_to_info(info, region, basemapName, grid_type=None):
    import _pickle as pickle
    import os
    import ship_mapper as sm
    
    info.grid.type = grid_type

    if info.grid.type == 'one-off':
        print('Using LOCAL grid (one-off)...')
        basemap_file = os.path.join(info.dirs.project_path,region,'ancillary',basemapName + '.grid')
        info.dirs.basemap = os.path.join(info.dirs.project_path,region,'ancillary',basemapName + '.basemap')
    elif info.grid.type == 'generic':
        print('Using GENERIC grid (settings.GRIDS)...')
        settings = sm.load_settings(info)
        basemap_file = os.path.abspath(os.path.join(settings.GRIDS,region,'ancillary',basemapName + '.grid'))
        info.dirs.basemap = os.path.abspath(os.path.join(settings.GRIDS,region,'ancillary',basemapName + '.basemap'))
    else:
        raise ValueError('info.grid.type can only be "one-off" or "generic"')
        
    
    print('Loading grid: ' + basemap_file)
    
    grid_info = pickle.load(open(basemap_file,'rb'))
    
    info.grid.region = grid_info.grid.region
    info.grid.basemap = grid_info.grid.basemap
    info.grid.bin_number =  grid_info.grid.bin_number
    info.grid.bin_size = grid_info.grid.bin_size
    info.grid.minlat = grid_info.grid.minlat
    info.grid.maxlat = grid_info.grid.maxlat
    info.grid.minlon = grid_info.grid.minlon
    info.grid.maxlon = grid_info.grid.maxlon
    info.grid.epsg_code = grid_info.grid.epsg_code
    info.grid.areas = grid_info.grid.areas
    
    info.maps.resolution = grid_info.maps.resolution
    info.maps.parallels = grid_info.maps.parallels
    info.maps.meridians = grid_info.maps.meridians
    info.maps.scalebar_km = grid_info.maps.scalebar_km
    return info




def data_to_info(info, data_source):
    '''
    Reads metadata from data source (i.e. data_info.yaml file)
    and appends it to ``info`` object
    
    :param info info: ``info`` object containing metadata
    '''
    import os
    import ship_mapper as sm
    import yaml
    
    settings = sm.load_settings(info)
    
    dinfo = yaml.load(open(os.path.join(settings.DATA, data_source,'data_info.yaml'), 'r'))
    
    info.converter = dinfo['converter']
    info.dirs.data_original = os.path.join(settings.DATA, data_source,'data_original') 
    info.dirs.data_nc = os.path.join(settings.DATA, data_source,'data_nc')
    
    return info





def info_to_attrs(info):
    '''
    Extracts `attibutes` from ``info`` object
    
    :param info info: ``info`` object containing metadata
    '''
    import types
    
    attributes = {}

    for row in info.__dict__.keys():
        if type(info.__dict__[row]) != types.SimpleNamespace:
            attributes[row] = info.__dict__[row]
        elif type(info.__dict__[row]) == types.SimpleNamespace:
            attributes[row] = {}
            for subrow in info.__dict__[row].__dict__.keys():
                attributes[row][subrow] = info.__dict__[row].__dict__[subrow]

    return attributes





def attrs_to_info(attrs):
    '''
    Appends `attributes` to ``info`` object
    '''
    import ship_mapper as sm

    info = sm.info()
    
    for row in attrs.keys():
        if not isinstance(attrs[row],dict):
            exec('info.' + row + '=attrs[row]')
        else:
            for subrow in attrs[row].keys():
                exec('info.' + row + '.' + subrow + '=attrs[row][subrow]')
    
    return info





def auto_update(filedash):
    '''
    Updates some metadata in ``info`` file
    '''
    import _pickle as pickle
    import os
    from pathlib import Path
    path_to_info = os.path.abspath(os.path.join(os.path.dirname( filedash ), 'ancillary','info.p'))
    
    info = pickle.load(open(path_to_info,'rb'))
    
    # Update run_name
    info.run_name = os.path.split(filedash)[1][:-3] 
    
    info.dirs.gridded_data = Path(os.path.join(str(info.dirs.project_path),'gridded_data',str(info.run_name)))
    info.dirs.merged_grid = Path(os.path.join(str(info.dirs.project_path),'merged_grid',str(info.run_name)))
    info.dirs.pngs = Path(os.path.join(str(info.dirs.project_path),'pngs',str(info.run_name)))
    info.dirs.shapefiles = Path(os.path.join(str(info.dirs.project_path),'shapefiles',str(info.run_name)))
#            str(info.dirs.project_path) / 'gridded_data' / str(info.run_name))
#    info.dirs['merged_grid'] = Path(str(info.dirs.project_path) / 'merged_grid' / str(info.run_name))
#    info.dirs['pngs'] = Path(str(info.dirs.project_path) / 'pngs' / str(info.run_name))
#    info.dirs['shapefiles'] = Path(str(info.dirs.project_path) / 'shapefiles' / str(info.run_name))

    return info



def make_info_from_GridData(calling_file='.', run_name=None,
                            region=None, basemap=None, grid_type='generic',
                            data_name = None):
    '''
    Makes ``info`` object and populates its metadata from ``.basemap`` and ``.grid`` files
    
    Keyword Arguments:
        calling_file (str): Usually this is ``__file__``, which returns the 
            full path and name of the calling file
        run_name (str): Usually the name of the script file
        region (str): Name of region
        basemap (str): Name of basemap
        grid_type (str): If ``'generic'`` grid is located in the ``grid`` directory.
            If ``'one-off'`` grid is located in the project directory
        data_name (str): Name of dataset (e.g. ``AIS_CCG`` or ``VMS_DFO``)
        
    Returns:
        info: Info object
    '''
    import ship_mapper as sm
    
    # Make info object
    info = sm.info(calling_file=calling_file, run_name=run_name)
    
    # Get metadata from "grid" and copy it into info
    info = sm.grid_to_info(info, region, basemap, grid_type=grid_type)
    
    # Get metadata from "data_info.yaml" and copy it into info
    info = sm.data_to_info(info, data_name)
    return info
