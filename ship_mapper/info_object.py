

class info:
    """
    info class makes and 'info object' which contains all the metadata
    needed to run a project.
    """
    
    
    def __init__(self, dir_data_original, filedash):
        import os
        from pathlib import Path
        from types import SimpleNamespace

        self.project_name = os.path.split(os.path.split(filedash)[0])[1]   
        self.run_name = os.path.split(filedash)[1][:-3]
        
        project_path = Path(os.path.split(filedash)[0])

        dirs = {}  
        dirs['top'] = os.path.abspath(os.path.join(os.path.dirname( filedash ), '../..'))
        dirs['project_path'] = Path(project_path)
        
        dirs['data_original'] = Path(dir_data_original)
        dirs['data_nc'] = Path(dir_data_original.replace('data_original', 'data_nc'))
        
        dirs['ancillary'] = Path(project_path / 'ancillary')
        dirs['gridded_data'] = Path(project_path / 'gridded_data')
        dirs['merged_grid'] = Path(project_path / 'merged_grid')
        dirs['pngs'] = Path(project_path / 'pngs')
        dirs['shapefiles'] = Path(project_path / 'shapefiles')
        
        grid ={}
        grid['bin_number'] = None
        grid['minlat'] = None
        grid['maxlat'] = None
        grid['minlon'] = None
        grid['maxlon'] = None
        grid['interp_threshold'] = 40 #knots
        grid['epsg_code'] = None
        
        filt ={}
        filt['speed_low'] = None
        filt['speed_high'] = None
        
        maps = {}
        maps['mask_below'] = 1
        maps['scalebar_km'] = 100
        maps['title'] = 'auto'
        
        legend = {}
        legend['source'] = None
        legend['filter'] = None
        
        self.grid = SimpleNamespace(**grid)
        self.filt = SimpleNamespace(**filt)
        self.dirs = SimpleNamespace(**dirs)
        self.maps = SimpleNamespace(**maps)
        
        return
    
    
    
    def __repr__(self):
        to_screen = ('*** Project information***' + '\n' +
                     'project_name: ' + self.project_name + '\n' +
                     'run_name: ' + self.run_name + '\n' +
                     'grid.bin_number: ' + str(self.grid.bin_number) + '\n' +
                     'grid.minlat: ' + str(self.grid.minlat) + '\n' +
                     'grid.maxlat: ' + str(self.grid.maxlat) + '\n' +
                     'grid.minlon: ' + str(self.grid.minlon) + '\n' +
                     'grid.maxlon: ' + str(self.grid.maxlon) + '\n' +
                     'filt.speed_low: ' + str(self.filt.speed_low) + '\n' +
                     'filt.speed_high: ' + str(self.filt.speed_high) + '\n' +
                     'dirs.top: ' + str(self.dirs.top) + '\n' +
                     'dirs.project_path: ' + str(self.dirs.project_path) + '\n' +
                     'dirs.data_original: ' + str(self.dirs.data_nc) + '\n' +
                     'dirs.data_nc: ' + str(self.dirs.data_nc) + '\n' +
                     'dirs.ancillary: ' + str(self.dirs.ancillary) + '\n' +
                     'dirs.gridded_data: ' + str(self.dirs.gridded_data) + '\n' +
                     'dirs.merged_grid: ' + str(self.dirs.merged_grid) + '\n' +    
                     'dirs.pngs: ' + str(self.dirs.pngs)
                     )
        return to_screen
    
    
    
    def save(self):
        '''
        Save info into pickle
        '''
        import _pickle as pickle
        import os
        import ship_mapper as sm
        
        sm.checkDir(str(self.dirs.ancillary))
        full_filename = os.path.join(self.dirs.ancillary, 'info.p')
        
        pickle.dump(self,open(full_filename,'wb'),-1)
        print('!!! Pickle info.p file just got saved ')
        return
    
    
def load_info(filedash):
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