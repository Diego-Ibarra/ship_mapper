import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap

import numpy as np
# Suppress matplotlib warnings
np.warnings.filterwarnings('ignore')

import xarray as xr
import cmocean
from pathlib import Path
import _pickle as pickle
import os
import ship_mapper as sm
import urllib.request
import netCDF4


def map_density(info, file_in=None, cmap='Default', sidebar=False,
                to_screen=True, save=True,
                filename_out='auto',filedir_out='auto'):
    '''
    Plots a map using a gridded (or merged) file
    
    Arguments:
        info (info): ``info`` object containing metadata
        
    Keyword Arguments:
        file_in (str): Gridded or merged file to map. If ``None`` it looks for 
            ``merged_grid.nc`` in the `\merged` directory
            
        cmap (str): Colormap to use
        
        sidebar (bool): If ``True``, includes side panel with metadata
        
        to_screen (bool): If ``True``, a plot is printed to screen
        
        save (bool): If ``True`` a ``.png`` figure is saved to hardrive
        
        filename_out (str): Name of produced figure. 
            If ``auto`` then name is ``info.run_name + '__' + file_in + '.png'``
            
        filedir_out (str): Directory where figure is saved.
            If ``auto`` then output directory is ``info.dirs.pngs``

    Returns:
        Basemap object
        
    '''
    
    print('map_density ------------------------------------------------------')
    
    # Load data
    if file_in == None:
        file_in = os.path.join(str(info.dirs.merged_grid),'merged_grid.nc')
        
    print(file_in)
        
    d = xr.open_dataset(file_in)
    
    # Define boundaries
    if info.grid.minlat == None or info.grid.maxlat == None or info.grid.minlon == None or info.grid.maxlon == None:  
        minlat = d['lat'].values.min()
        maxlat = d['lat'].values.max()
        minlon = d['lon'].values.min()
        maxlon = d['lon'].values.max()
    else:
        minlat = d.attrs['minlat']
        maxlat = d.attrs['maxlat']
        minlon = d.attrs['minlon']
        maxlon = d.attrs['maxlon']
    
    basemap_file = info.dirs.basemap
    print('Basemap file: ' + basemap_file)
    
    
    # Check for basemap.p and, if doesn;t exist, make it
    if not os.path.exists(basemap_file):
        m = sm.make_basemap(info,info.dirs.project_path,[minlat,maxlat,minlon,maxlon])
    else:
        print('Found basemap...')
        m = pickle.load(open(basemap_file,'rb'))

    
    # Create grid for mapping
    lons_grid, lats_grid = np.meshgrid(d['lon'].values,d['lat'].values)
    xx,yy = m(lons_grid, lats_grid)
    
    H = d['ship_density'].values
    
    # Rotate and flip H... ----------------------------------------------------------------------------
    H = np.rot90(H)
    H = np.flipud(H)
     
    # Mask zeros
    d.attrs['mask_below'] = info.maps.mask_below
    Hmasked = np.ma.masked_where(H<=d.attrs['mask_below'],H)
     
    # Set vman and vmin
    print('Min: ' + str(np.min(Hmasked)))
    print('Max: ' + str(np.max(Hmasked)))
    print('Mean: ' + str(np.nanmean(Hmasked)))
    print('Std: ' + str(Hmasked.std()))
    
    if info.maps.cbarmax == 'auto':
#        vmax = (np.median(Hmasked)) + (4*Hmasked.std())
        vmax = (np.max(Hmasked)) - (2*Hmasked.std())
    elif info.maps.cbarmax != None:
        vmax = info.maps.cbarmax
    else:
        vmax = None
        
    if info.maps.cbarmin == 'auto':
#        vmin = (np.median(Hmasked)) - (4*Hmasked.std())
        alat = (d.attrs['maxlat'] - d.attrs['minlat'])/2
        cellsize = sm.degrees_to_meters(d.attrs['bin_size'], alat)
#        max_speed = 616.66 # m/min ...roughly 20 knots
        max_speed = 316.66 # m/min ...roughly 20 knots
        vmin = cellsize / max_speed
    elif info.maps.cbarmin != None:
        vmin = info.maps.cbarmin
    else:
        vmin = None
    
    
    
    # Log H for better display
    Hmasked = np.log10(Hmasked)
    if vmin != None:
        vmin = np.log10(vmin)
    if vmax != None:
        vmax = np.log10(vmax)
    

    # Make colormap
    fig = plt.gcf()
    ax = plt.gca()
    
    if cmap == 'Default':
        cmapcolor = load_my_cmap('my_cmap_amber2red')
    elif cmap == 'red2black':
        cmapcolor = load_my_cmap('my_cmap_red2black')
    else:
        cmapcolor =plt.get_cmap(cmap)
        


        
    cs = m.pcolor(xx,yy,Hmasked, cmap=cmapcolor, zorder=10, vmin=vmin, vmax=vmax)
    
    #scalebar
    sblon = minlon + ((maxlon-minlon)/10)
    sblat = minlat + ((maxlat-minlat)/20)
    m.drawmapscale(sblon, sblat,
           minlon, minlat,
           info.maps.scalebar_km, barstyle='fancy',
           units='km', fontsize=8,
           fontcolor='#808080',
           fillcolor1 = '#cccccc',
           fillcolor2 = '#a6a6a6',
           yoffset = (0.01*(m.ymax-m.ymin)),
           labelstyle='simple',zorder=60)


    if not sidebar:
        cbaxes2 = fig.add_axes([0.70, 0.18, 0.2, 0.03],zorder=60)
        cbar = plt.colorbar(extend='both', cax = cbaxes2, orientation='horizontal')
        
        # Change colorbar labels for easier interpreting
        label_values = cbar._tick_data_values
        log_label_values = np.round(10 ** label_values,decimals=0)
        labels = []
        for log_label_value in log_label_values:
            labels.append(str(int(log_label_value)))
        
        cbar.ax.set_yticklabels(labels)
        cbar.ax.set_xlabel(d.attrs['units'])
   

    if sidebar:
        
        text1, text2, text3, text4 = make_legend_text(info,d.attrs)
        
        ax2 = plt.subplot2grid((1,24),(0,0),colspan=4)
                
        # Turn off tick labels
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        ax2.add_patch(FancyBboxPatch((0,0),
                                width=1, height=1, clip_on=False,
                                boxstyle="square,pad=0", zorder=3,
                                facecolor='#e6e6e6', alpha=1.0,
                                edgecolor='#a6a6a6',
                                transform=plt.gca().transAxes))
        plt.text(0.15, 0.99, text1,
                verticalalignment='top',
                horizontalalignment='left',
                weight='bold',
                size=10,
                color= '#737373',
                transform=plt.gca().transAxes)
        
        plt.text(0.02, 0.83, text2,
                horizontalalignment='left',
                verticalalignment='top',
                size=9,
                color= '#808080',
                transform=plt.gca().transAxes)
        
        plt.text(0.02, 0.145, text3,
                horizontalalignment='left',
                verticalalignment='top',
                size=7,
                color= '#808080',
                transform=plt.gca().transAxes)
        
        plt.text(0.02, 0.25, text4,
                style='italic',
                horizontalalignment='left',
                verticalalignment='top',
                size=8,
                color= '#808080',
                transform=plt.gca().transAxes)
        
        
        cbaxes2 = fig.add_axes([0.019, 0.9, 0.15, 0.02],zorder=60)
        cbar = plt.colorbar(extend='both', cax = cbaxes2, orientation='horizontal')
        cbar.ax.tick_params(labelsize=8, labelcolor='#808080') 
        
        # Change colorbar labels for easier interpreting
        label_values = cbar._tick_data_values
#        print("values")
#        print(label_values)
        log_label_values = np.round(10 ** label_values,decimals=0)
#        print(log_label_values)
        labels = []
        for log_label_value in log_label_values:
            labels.append(str(int(log_label_value)))
        
        cbar.ax.set_xticklabels(labels)
        cbar.ax.set_xlabel(d.attrs['units'], size=9, color='#808080') 
                           

    
    
    # TODO: maybe delete this?
#    mng = plt.get_current_fig_manager()
#    mng.frame.Maximize(True)
#
#    fig.tight_layout()

    plt.show()

    
    # Save map as png
    if save:
        if filedir_out == 'auto':
            filedir = str(info.dirs.pngs)
        else:
            filedir = filedir_out
            
        if filename_out == 'auto':
            filename = info.run_name + '__' + sm.get_filename_from_fullpath(file_in) + '.png'
        else:
            filename = filename_out
            
        sm.checkDir(filedir)
        plt.savefig(os.path.join(filedir,filename), dpi=300)
            
    
    # Close netCDF file
    d.close()
    
    if to_screen == False:
        plt.close()
    
    return


def make_legend_text(info,md):
    '''
    Makes text for legend in left block of map
    
    :param info info: ``info`` object containing metadata
    
    :return: text for legend
    '''
    import datetime
    
    alat = (md['maxlat'] - md['minlat'])/2
    
    text1 = 'VESSEL DENSITY HEATMAP'
#    print(info)
    # --------------------------------------------------------
    text2 = ('Unit description: ' + md['unit_description'] + '\n\n' +
             'Data source: ' + md['data_source'] + '\n\n' +
             'Data source description:\n' + md['data_description'] + '\n\n' +
             'Time range: \n' + md['startdate'][0:-3] + ' to ' + md['enddate'][0:-3] + '\n\n' +
             'Included speeds: ' + info.sidebar.included_speeds + '\n' +
             'Included vessels: ' + info.sidebar.included_vessel_types + '\n\n' +
             'Grid size: ' + str(md['bin_size']) + ' degrees (~' + str(int(round(sm.degrees_to_meters(md['bin_size'], alat))))+ ' m)\n' +
             'EPGS code: ' + md['epsg_code'] + '\n' +
             'Interpolation: ' + md['interpolation'] + '\n' +
             'Interpolation threshold: ' + str(md['interp_threshold']) + ' knots\n' +
             'Time bin: ' + str(round(md['time_bin']*1440,1)) +  ' minutes\n' +
             'Mask below: ' + str(md['mask_below']) + ' vessels per grid'
             )
    
    text3 = ('Creation date: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n' + 
             'Creation script: ' + info.run_name + '.py\n' +
             'Software: ship mapper v0.1\n\n' +
             'Created by:\n' +
             'Oceans and Coastal Management Division\n' +
             'Ecosystem Management Branch\n' +
             'Fisheries and Oceans Canada – Maritimes Region\n' +
             'Bedford Institute of Oceanography\n' +
             'PO Box 1006, Dartmouth, NS, Canada, B2Y 4A2'
         )
    
    text4 = ('---------------------------------------------------------------\n' +
             'WARNING: This is a preliminary data product.\n' +
             'We cannot ​guarantee the validity, accuracy, \n' +
             'or quality of this product. ​Data is provided\n' +
             'on an "AS IS" basis. ​USE AT YOUR OWN RISK.\n' +
             '---------------------------------------------------------------\n'
         )
    
    
    
    return text1, text2, text3, text4



def map_dots(info, file_in, sidebar=False, save=True):
    '''
    Creates a map of "pings" rather than gridded density
    
    Arguments:
        info (info): ``info`` object containing metadata

    Keyword Arguments:
        file_in (str): Gridded or merged file to map. If ``None`` it looks for 
            ``merged_grid.nc`` in the `\merged` directory
        sidebar (bool): If ``True``, includes side panel with metadata
        save (bool): If ``True`` a ``.png`` figure is saved to hardrive
    '''
    print('Mapping...')
    # -----------------------------------------------------------------------------
        
    d = xr.open_dataset(file_in)
    
    # Define boundaries
    if info.grid.minlat == None or info.grid.maxlat == None or info.grid.minlon == None or info.grid.maxlon == None:  
        minlat = d['lat'].values.min()
        maxlat = d['lat'].values.max()
        minlon = d['lon'].values.min()
        maxlon = d['lon'].values.max()
    else:
        minlat = info.grid.minlat
        maxlat = info.grid.maxlat
        minlon = info.grid.minlon
        maxlon = info.grid.maxlon
    
    
    
    path_to_basemap = info.dirs.project_path / 'ancillary'
    print('-----------------------------------------------------')
    print('-----------------------------------------------------')
    
    if sidebar:
        basemap_file = str(path_to_basemap / 'basemap_sidebar.p')
    else:
        basemap_file = str(path_to_basemap / 'basemap.p')
    
    if not os.path.exists(basemap_file):
        m = sm.make_basemap(info,[minlat,maxlat,minlon,maxlon])
    else:
        print('Found basemap...')
        m = pickle.load(open(basemap_file,'rb'))

    x, y = m(d['longitude'].values,d['latitude'].values)
    
    cs = m.scatter(x,y,s=0.1,marker='o',color='r',  zorder=10)
#    
    plt.show()
    
#    # Save map as png
#    if save:
#        filedir = str(info.dirs.pngs)
#        sm.checkDir(filedir)
#        filename = info.project_name + '_' + str(info.grid.bin_number) + '.png'
#        plt.savefig(os.path.join(filedir,filename), dpi=300)
   
    return




def map_dots_one_ship(info, file_in, Ship_No, save=True):
    '''
    Creates a map of "pings" (i.e. not gridded density) of only one ship
    
    Arguments:
        info (info): ``info`` object containing metadata

    Keyword Arguments:
        file_in (str): Gridded or merged file to map. If ``None`` it looks for 
            ``merged_grid.nc`` in the `\merged` directory
        Ship_No (str): Unique identifier of the ship to plot
        save (bool): If ``True`` a ``.png`` figure is saved to hardrive
    '''
    import pandas as pd
    print('Mapping...')
    # -----------------------------------------------------------------------------
        
    d = xr.open_dataset(file_in)
    
    # Define boundaries
    if info.grid.minlat == None or info.grid.maxlat == None or info.grid.minlon == None or info.grid.maxlon == None:  
        minlat = d['lat'].values.min()
        maxlat = d['lat'].values.max()
        minlon = d['lon'].values.min()
        maxlon = d['lon'].values.max()
    else:
        minlat = info.grid.minlat
        maxlat = info.grid.maxlat
        minlon = info.grid.minlon
        maxlon = info.grid.maxlon
    
    
    
    path_to_basemap = info.dirs.project_path / 'ancillary'
    print('-----------------------------------------------------')
    print('-----------------------------------------------------')
    
#    basemap_file = str(path_to_basemap / 'basemap_spots.p')
    
    m = sm.make_basemap(info.dirs.project_path,[minlat,maxlat,minlon,maxlon])
    
#    if not os.path.exists(str(path_to_basemap / 'basemap.p')):
#        m = sm.make_basemap(info.dirs.project_path,[minlat,maxlat,minlon,maxlon])
#    else:
#        print('Found basemap...')
#        m = pickle.load(open(basemap_file,'rb'))
        
    indx = ((d['longitude']>  minlon) &
            (d['longitude']<= maxlon) &
            (d['latitude']>  minlat) &
            (d['latitude']<= maxlat))
        
    filtered_data = d.sel(Dindex=indx)

    ship_id = info.ship_id
    unis = pd.unique(filtered_data[ship_id].values)
    ship = unis[Ship_No]
    indxship = (filtered_data[ship_id] == ship)
    singleship = filtered_data.sel(Dindex=indxship)
    print('Ship id:'+ str(ship))
    
#    print(singleship['longitude'].values)
#    print(singleship['latitude'].values)
    
        
    x, y = m(singleship['longitude'].values,singleship['latitude'].values)
#    x, y = m(d['longitude'].values,d['latitude'].values)
    
    cs = m.scatter(x,y,2,marker='o',color='r', zorder=30)
    
#    fig = plt.figure()
#    plt.plot(filtered_data['longitude'].values,filtered_data['latitude'].values,'.')
#    
    plt.show()
    
#    # Save map as png
#    if save:
#        filedir = str(info.dirs.pngs)
#        sm.checkDir(filedir)
#        filename = info.project_name + '_' + str(info.grid.bin_number) + '.png'
#        plt.savefig(os.path.join(filedir,filename), dpi=300)
   
    return



def define_path_to_map(info, path_to_basemap='auto'):
    '''
    Figures out where is the .basemap and .grid files
    
    Arguments:
        info (info): ``info`` object containing metadata
    '''
    if path_to_basemap == 'auto':
        if info.grid.type == 'one-off':
            path_to_map = os.path.join(info.dirs.project_path,info.grid.region,'ancillary')
        elif info.grid.type == 'generic':
            path_to_map = os.path.abspath(os.path.join(info.dirs.project_path,'ancillary'))
    else:
        path_to_map = path_to_basemap
    return path_to_map



def make_basemap(info,spatial,path_to_basemap='auto', sidebar=False):
    '''
    Makes a basemap
    
    Arguments:
        info (info): ``info`` object containing metadata
        spatial (list): List with corners... this will be deprecated soon
        
    Keyword arguments:
        path_to_basemap (str): Directory where to save the produced basemap. If ``'auto'``
            then path is setup by :func:`~ship_mapper.mapper.define_path_to_map`
        sidebar (bool): If ``True`` space for a side panel is added to the basemap
        
    Returns:
        A ``.basemap`` and a ``.grid`` files 
    '''
    print('Making basemap...')
    # -----------------------------------------------------------------------------
    
    path_to_map = define_path_to_map(info, path_to_basemap=path_to_basemap)
    
    sm.checkDir(str(path_to_map))
    

    minlat = spatial[0]
    maxlat = spatial[1]
    minlon = spatial[2]
    maxlon = spatial[3]

    # Create map
    m = Basemap(projection='mill', llcrnrlat=minlat,urcrnrlat=maxlat,
                llcrnrlon=minlon, urcrnrlon=maxlon,resolution=info.maps.resolution)


    
    # TOPO
    # Read data from: http://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.html
    # using the netCDF output option
#    bathymetry_file = str(path_to_map / 'usgsCeSrtm30v6.nc')
    bathymetry_file = os.path.join(path_to_map, 'usgsCeSrtm30v6.nc')

    if not os.path.isfile(bathymetry_file):
        isub = 1
        base_url='http://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.nc?'
        query='topo[(%f):%d:(%f)][(%f):%d:(%f)]' % (maxlat,isub,minlat,minlon,isub,maxlon)
        url = base_url+query
        # store data in NetCDF file
        urllib.request.urlretrieve(url, bathymetry_file)
    # open NetCDF data in 
    nc = netCDF4.Dataset(bathymetry_file)
    ncv = nc.variables
    lon = ncv['longitude'][:]
    lat = ncv['latitude'][:]
    lons, lats = np.meshgrid(lon,lat)
    topo = ncv['topo'][:,:]
#    
    fig = plt.figure(figsize=(19,9))
    
#    ax = fig.add_axes([0.05,0.05,0.80,1])
#    ax = fig.add_axes([0,0,0.80,1])
    


    
#    ax = fig.add_axes([0.23,0.035,0.85,0.9])
    if sidebar:
        ax = plt.subplot2grid((1,24),(0,5),colspan=19)
    else:
        ax = fig.add_axes([0.05,0.05,0.94,0.94])
    
    TOPOmasked = np.ma.masked_where(topo>0,topo)

    cs = m.pcolormesh(lons,lats,TOPOmasked,cmap=load_my_cmap('my_cmap_lightblue'),latlon=True,zorder=5)

#    m.drawcoastlines(color='#A27D0C',linewidth=0.5,zorder=25)
#    m.fillcontinents(color='#E1E1A0',zorder=23)
    m.drawcoastlines(color='#a6a6a6',linewidth=0.5,zorder=25)
    m.fillcontinents(color='#e6e6e6',zorder=23)
    m.drawmapboundary()
    
    def setcolor(x, color):
         for m in x:
             for t in x[m][1]:
                 t.set_color(color)


    parallels = np.arange(minlat,maxlat,info.maps.parallels)
    # labels = [left,right,top,bottom]
    par = m.drawparallels(parallels,labels=[True,False,False,False],dashes=[20,20],color='#00a3cc', linewidth=0.2, zorder=25)
    setcolor(par,'#00a3cc')                      
    meridians = np.arange(minlon,maxlon,info.maps.meridians)
    mers =  m.drawmeridians(meridians,labels=[False,False,False,True],dashes=[20,20],color='#00a3cc', linewidth=0.2, zorder=25)
    setcolor(mers,'#00a3cc') 

    ax = plt.gca()
#    ax.axhline(linewidth=4, color="#00a3cc")        
#    ax.axvline(linewidth=4, color="#00a3cc") 
#    
    ax.spines['top'].set_color('#00a3cc')
    ax.spines['right'].set_color('#00a3cc')
    ax.spines['bottom'].set_color('#00a3cc')
    ax.spines['left'].set_color('#00a3cc')
             
    for k, spine in ax.spines.items():  #ax.spines is a dictionary
        spine.set_zorder(35)    

#    ax.spines['top'].set_visible(False)
#    ax.spines['right'].set_visible(False)
#    ax.spines['bottom'].set_visible(False)
#    ax.spines['left'].set_visible(False)
  
#    fig.tight_layout(pad=0.25)
    fig.tight_layout(rect=[0.01,0.01,.99,.99])
    plt.show()
    
    if sidebar:
        basemap_name = 'basemap_sidebar.p'
    else:
        basemap_name = 'basemap.p'
        
    info = sm.calculate_gridcell_areas(info)
    
    # Save basemap
    save_basemap(m,info,path_to_basemap=path_to_map)
#    picklename = str(path_to_map / basemap_name)
#    pickle.dump(m,open(picklename,'wb'),-1)
#    print('!!! Pickle just made: ' + picklename)
#    
##    pngDir = 'C:\\Users\\IbarraD\\Documents\\VMS\\png\\'
##    plt.savefig(datadir[0:-5] + 'png\\' + filename + '- Grid' + str(BinNo) + ' - Filter' +str(downLim) + '-' + str(upLim) + '.png')
#    plt.savefig('test.png')
    
    return m






def load_my_cmap(name):
    '''
    Creates and loads custom colormap
    '''
#    cdict = {'red': ((0.0, 0.0, 0.0),
#                     (1.0, 0.7, 0.7)),
#           'green': ((0.0, 0.25, 0.25),
#                     (1.0, 0.85, 0.85)),
#            'blue': ((0.0, 0.5, 0.5),
#                     (1.0, 1.0, 1.0))}
#    my_cmap = LinearSegmentedColormap('my_colormap',cdict,256)
    if name == 'my_cmap_lightblue':
        cdict = {'red': ((0.0, 0.0, 0.0), # Dark
                         (1.0, 0.9, 0.9)), # Light
               'green': ((0.0, 0.9, 0.9),
                         (1.0, 1.0,1.0)),
                'blue': ((0.0, 0.9, 0.9),
                         (1.0, 1.0, 1.0))}
        my_cmap = LinearSegmentedColormap('my_colormap',cdict,256)
    elif name == 'my_cmap_amber2red':
    #    cdict = {'red': ((0.0, 1.0, 1.0),
    #                     (1.0, 0.5, 0.5)),
    #           'green': ((0.0, 1.0, 1.0),
    #                     (1.0, 0.0, 0.0)),
    #            'blue': ((0.0, 0.0, 0.0),
    #                     (1.0, 0.0, 0.0))}
    #    my_cmap_yellow2red = LinearSegmentedColormap('my_colormap',cdict,256)
        cdict = {'red': ((0.0, 1.0, 1.0),
                         (1.0, 0.5, 0.5)),
               'green': ((0.0, 0.85, 0.85),
                         (1.0, 0.0, 0.0)),
                'blue': ((0.0, 0.3, 0.3),
                         (1.0, 0.0, 0.0))}
        my_cmap = LinearSegmentedColormap('my_colormap',cdict,256)
    elif name == 'my_cmap_red2black':
        
#        c1 = np.array([252,142,110])/256 #RGB/256
        c1 = np.array([250,59,59])/256 #RGB/256
        c2 = np.array([103,0,13])/256 #RGB/256
        
        cdict = {'red': ((0.0, c1[0], c1[0]),
                         (1.0, c2[0], c2[0])),
               'green': ((0.0, c1[1], c1[1]),
                         (1.0, c2[1], c2[1])),
                'blue': ((0.0, c1[2], c1[2]),
                         (1.0, c2[2], c2[2]))}
        my_cmap = LinearSegmentedColormap('my_colormap',cdict,256)
    else:
        print('cmap name does not match any of the available cmaps')

    return  my_cmap


def save_basemap(m,info,path_to_basemap='auto'):
    '''
    Saves basemap (and correspoding info.grid) to a pickle file
    
    Arguments:
        m (mpl_toolkits.basemap.Basemap): Basemap object
        info (info): ``info`` object containing metadata
        
    Keyword Arguments:
        path_to_basemap (str): If ``'auto'`` it looks in ``grids`` directory
        
    Returns:
        Pickle file
        
    See also:
        :mod:`pickle`
    '''
#    
#    basemap = [grid, m]
#    f = open(str(path_to_map / (info.grid.basemap + '.p')),'w')
#    pickle.dump(grid, f)
#    pickle.dump(m, f)
#    f.close()
    
#    picklename = str(path_to_map / (info.grid.basemap + '.p'))
#    pickle.dump(basemap, open(picklename, 'wb'), -1)
#    print('!!! Pickle just made: ' + picklename)
    
    path_to_map = define_path_to_map(info, path_to_basemap=path_to_basemap)
        
#    basemap_picklename = str(path_to_map / (info.grid.basemap + '.basemap'))
    basemap_picklename = os.path.join(path_to_map,info.grid.basemap + '.basemap')
    pickle.dump(m, open(basemap_picklename, 'wb'), -1)
    
#    info_picklename = str(path_to_map / (info.grid.basemap + '.grid'))
    info_picklename = os.path.join(path_to_map, info.grid.basemap + '.grid')
    pickle.dump(info, open(info_picklename, 'wb'), -1)
    
    print('!!! Pickles were just made: ' +  basemap_picklename)
    return
