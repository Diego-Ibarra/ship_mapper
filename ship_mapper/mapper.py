# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:51:50 2018

@author: IbarraD
"""
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



def map_density(info, file_in=None, cmap='Default', sidebar=False, to_screen=True, save=True):
    
    print('map_density ------------------------------------------------------')
    
    # Load data
    if file_in == None:
        file_in = os.path.join(str(info.dirs.merged_grid),'merged_grid.nc')
        
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
    
    # Some address
    path_to_basemap = info.dirs.project_path / 'ancillary'
    
    if sidebar:
        basemap_file = str(path_to_basemap / 'basemap_sidebar.p')
    else:
        basemap_file = str(path_to_basemap / 'basemap.p')
    
    
    # Check for basemap.p and, if doesn;t exist, make it
#    if not os.path.exists(str(path_to_basemap / 'basemap.p')):
    if not os.path.exists(basemap_file):
        m = sm.make_basemap(info,info.dirs.project_path,[minlat,maxlat,minlon,maxlon])
    else:
        print('Found basemap...')
        m = pickle.load(open(basemap_file,'rb'))

    
#    # Create grid for mapping
#    lons_grid, lats_grid = np.meshgrid(d['lon'].values,d['lat'].values)
#    xx,yy = m(lons_grid, lats_grid)
#    
#    H = d['ship_density'].values
#    
#    # Rotate and flip H... ----------------------------------------------------------------------------
#    H = np.rot90(H)
#    H = np.flipud(H)
#     
#    # Mask zeros
#    Hmasked = np.ma.masked_where(H<info.maps.mask_below,H)
#     
#    # Log H for better display
#    Hmasked = np.log10(Hmasked)
#    
#
#    # Make colormap
#    fig = plt.gcf()
#    ax = plt.gca()
#    
#    if cmap == 'Default':
#        cmapcolor = load_my_cmap('my_cmap_amber2red')
#    elif cmap == 'red2black':
#        cmapcolor = load_my_cmap('my_cmap_red2black')
#    else:
#        cmapcolor =plt.get_cmap(cmap)
#       
#    cs = m.pcolor(xx,yy,Hmasked, cmap=cmapcolor, zorder=10)
#    
#    #scalebar
#    sblon = info.grid.minlon + ((info.grid.maxlon-info.grid.minlon)/10)
#    sblat = info.grid.minlat + ((info.grid.maxlat-info.grid.minlat)/20)
#    m.drawmapscale(sblon, sblat,
#           info.grid.minlon, info.grid.minlat,
#           info.maps.scalebar_km, barstyle='fancy',
#           units='km', fontsize=8,
#           fontcolor='#808080',
#           fillcolor1 = '#cccccc',
#           fillcolor2 = '#a6a6a6',
#           yoffset = (0.01*(m.ymax-m.ymin)),
#           labelstyle='simple',zorder=60)
#
#    
#
##    if info.maps.title == 'auto':
##        plot_title = info.run_name
##    else:
##        plot_title = info.maps.title
##
##    plt.title(plot_title)
##  
##    plt.title('Vessels density (' + str(BinNo,) + ' X ' + str(BinNo,) + ' grid) from file:' + filename +
##              '\n Filter: Apparent speed between ' + str(downLim) + ' and ' + str(upLim) + ' knots')
#
#
#
#    if not sidebar:
#        cbaxes2 = fig.add_axes([0.70, 0.18, 0.2, 0.03],zorder=60)
#        cbar = plt.colorbar(extend='both', cax = cbaxes2, orientation='horizontal')
#        
#        # Change colorbar labels for easier interpreting
#        label_values = cbar._tick_data_values
#        log_label_values = np.round(10 ** label_values,decimals=0)
#        labels = []
#        for log_label_value in log_label_values:
#            labels.append(str(int(log_label_value)))
#        
#        cbar.ax.set_yticklabels(labels)
#        cbar.ax.set_xlabel('No. of vessels within grid-cell')
#    
#    
##    legend_content = ('--- Vessel Density Map ---\n\n' +
##                      'Test'
##            )
#    
#    
#
##    props = dict( facecolor='#e6e6e6', alpha=1,edgecolor='#a6a6a6',boxstyle="Square,pad=0.5",zorder=1)  
##    plt.figtext(0.85, 0.1,
##                legend_content,
##                linespacing=1.0,
##                bbox=props,
##                zorder=0)
#
##    ax2 = fig.add_axes([0.80,0,1,1])
##    ax2 = fig.add_axes([0,0,0.2,1])
#    if sidebar:
#        
#        text1, text2, text3, text4 = make_legend_text(info)
#        
#        ax2 = plt.subplot2grid((1,24),(0,0),colspan=4)
#                
#        # Turn off tick labels
#        ax2.get_xaxis().set_visible(False)
#        ax2.get_yaxis().set_visible(False)
#        ax2.add_patch(FancyBboxPatch((0,0),
#                                width=1, height=1, clip_on=False,
#                                boxstyle="square,pad=0", zorder=3,
#                                facecolor='#e6e6e6', alpha=1.0,
#                                edgecolor='#a6a6a6',
#                                transform=plt.gca().transAxes))
#        plt.text(0.15, 0.99, text1,
#                verticalalignment='top',
#                horizontalalignment='left',
#                weight='bold',
#                size=10,
#                color= '#737373',
#                transform=plt.gca().transAxes)
#        
#        plt.text(0.02, 0.83, text2,
#                horizontalalignment='left',
#                verticalalignment='top',
#                size=9,
#                color= '#808080',
#                transform=plt.gca().transAxes)
#        
#        plt.text(0.02, 0.145, text3,
#                horizontalalignment='left',
#                verticalalignment='top',
#                size=7,
#                color= '#808080',
#                transform=plt.gca().transAxes)
#        
#        plt.text(0.02, 0.25, text4,
#                style='italic',
#                horizontalalignment='left',
#                verticalalignment='top',
#                size=8,
#                color= '#808080',
#                transform=plt.gca().transAxes)
#        
#        
#        cbaxes2 = fig.add_axes([0.019, 0.9, 0.15, 0.02],zorder=60)
#        cbar = plt.colorbar(extend='both', cax = cbaxes2, orientation='horizontal')
#        cbar.ax.tick_params(labelsize=8, labelcolor='#808080') 
#        
#        # Change colorbar labels for easier interpreting
#        label_values = cbar._tick_data_values
#        print("values")
#        print(label_values)
#        log_label_values = np.round(10 ** label_values,decimals=0)
#        print(log_label_values)
#        labels = []
#        for log_label_value in log_label_values:
#            labels.append(str(int(log_label_value)))
#        
#        cbar.ax.set_xticklabels(labels)
#        cbar.ax.set_xlabel('No. of vessels within grid-cell', size=9, color='#808080') 
#                           
#                           
#                           
#                           
#
#
#        
#        
#    #    plt.text(-0.04, 0.95, " Regular Plot:      plt.plot(...)\n Just a test",
#    #            horizontalalignment='left',
#    #            verticalalignment='top',
#    #            size='xx-large',
#    #            transform=plt.gca().transAxes)
#        
#    #    ax2.text(left, bottom, 'left top',
#    #            horizontalalignment='left',
#    #            verticalalignment='top',
#    #            transform=ax.transAxes)
#    #    
#    
#    
#    # TODO: maybe delete this?
##    mng = plt.get_current_fig_manager()
##    mng.frame.Maximize(True)
##
##    fig.tight_layout()
#
#    plt.show()

    
    # Save map as png
    if save:
        filedir = str(info.dirs.pngs)
        sm.checkDir(filedir)
        filename = info.run_name + '__' + sm.get_filename_from_fullpath(file_in) + '.png'
        print(filedir)
        print(filename)
#        if info.maps.title == 'auto':
#            filename = info.project_name + '_' + str(info.grid.bin_number) + '.png'
#        else:
#            filename = info.maps.title + '.png'
        plt.savefig(os.path.join(filedir,filename), dpi=300)
    
    # Close netCDF file
    d.close()
    
    if to_screen == False:
        plt.close()
    
    return


def make_legend_text(info):
    import datetime
    
    alat = (info.grid.maxlat - info.grid.minlat)/2
    
    text1 = 'VESSEL DENSITY HEATMAP'
    # --------------------------------------------------------
    text2 = ('Unit description: ' + info.sidebar.unit_description + '\n\n' +
             'Data source: ' + info.sidebar.data_source + '\n\n' +
             'Data source description: ' + info.sidebar.data_description + '\n\n' +
             'Time range: ' + info.sidebar.time_range + '\n\n' +
             'Included speeds: ' + info.sidebar.included_speeds + '\n\n' +
             'Grid size: ' + str(info.grid.bin_size) + ' degrees (~' + str(int(round(sm.degrees_to_meters(info.grid.bin_size, alat))))+ ' m)\n' +
             'EPGS code: ' + str(info.grid.epsg_code) + '\n' +
             'Interpolation: ' + info.sidebar.interpolation + '\n' +
             'Interpolation threshold: ' + str(info.grid.interp_threshold) + ' knots\n' +
             'Time bin: ' + str(info.sidebar.time_bin) +  ' minutes\n' +
             'Mask below: ' + str(info.maps.mask_below) + ' vessels per grid'
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
        m = sm.make_basemap(info,info.dirs.project_path,[minlat,maxlat,minlon,maxlon])
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





def make_basemap(info,project_path,spatial,sidebar=False):
    print('Mapping...')
    # -----------------------------------------------------------------------------
    
    path_to_map = Path(project_path) / 'ancillary'
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
    bathymetry_file = str(path_to_map / 'usgsCeSrtm30v6.nc')
    
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
    par = m.drawparallels(parallels,labels=[True,False,False,False],dashes=[1,2],color='#00a3cc', zorder=25)
    setcolor(par,'#00a3cc')                      
    meridians = np.arange(minlon,maxlon,info.maps.meridians)
    mers =  m.drawmeridians(meridians,labels=[False,False,False,True],dashes=[1,2],color='#00a3cc', zorder=25)
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
    
    # Save basemap
    picklename = str(path_to_map / basemap_name)
    pickle.dump(m,open(picklename,'wb'),-1)
    print('!!! Pickle just made: ' + picklename)
#    
##    pngDir = 'C:\\Users\\IbarraD\\Documents\\VMS\\png\\'
##    plt.savefig(datadir[0:-5] + 'png\\' + filename + '- Grid' + str(BinNo) + ' - Filter' +str(downLim) + '-' + str(upLim) + '.png')
#    plt.savefig('test.png')
    
    return m






def load_my_cmap(name):
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

