

class info:
    """A simple example class"""
    
    
    def __init__(self,dir_top, dir_data_original, filedash):
        import os
        from pathlib import Path
        from types import SimpleNamespace

        self.project_name = os.path.split(os.path.split(filedash)[0])[1]   
        self.run_name = os.path.split(filedash)[1][:-3]
        
        project_path = Path(os.path.split(filedash)[0])

        dirs = {}  
        dirs['top'] = dir_top
        dirs['project_path'] = Path(project_path)
        
        dirs['data_original'] = Path(dir_data_original)
        dirs['data_nc'] = Path(dir_data_original.replace('data_original', 'data_nc'))
        
        dirs['gridded_data'] = Path(project_path / 'gridded_data')
        dirs['merged_grid'] = Path(project_path / 'merged_grid')
        dirs['pngs'] = Path(project_path / 'pngs')
        
        grid ={}
        grid['bin_number'] = None
        grid['minlat'] = None
        grid['maxlat'] = None
        grid['minlon'] = None
        grid['maxlon'] = None
        
        filt ={}
        filt['speed_low'] = None
        filt['speed_high'] = None
        
        self.grid = SimpleNamespace(**grid)
        self.filt = SimpleNamespace(**filt)
        self.dirs = SimpleNamespace(**dirs)
        
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
                     'dirs.gridded_data: ' + str(self.dirs.gridded_data) + '\n' +
                     'dirs.merged_grid: ' + str(self.dirs.merged_grid) + '\n' +    
                     'dirs.pngs: ' + str(self.dirs.pngs)
                     )
        return to_screen
