# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:51:50 2018

@author: IbarraD
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
import xarray as xr
import cmocean
    
def map_density(BinNo,downLim,upLim,file_in,spatial=None):
    print('Mapping...')
    # -----------------------------------------------------------------------------
    
    # Load data
    d = xr.open_dataset(file_in)
    
    # Define boundaries
    if spatial == None:  
        minlat = d['lat'].values.min()
        maxlat = d['lat'].values.max()
        minlon = d['lon'].values.min()
        maxlon = d['lon'].values.max()
    else:
        minlat = spatial[0]
        maxlat = spatial[1]
        minlon = spatial[2]
        maxlon = spatial[3]
    
    # APply filter (i.e. get rid of points above and below the velocity thresholds)
    d = d.where((d['velocgridded'] >= downLim) & (d['velocgridded'] < upLim),drop=True)
    
    # Create map
    m = Basemap(projection='mill', llcrnrlat=minlat,urcrnrlat=maxlat,
                llcrnrlon=minlon, urcrnrlon=maxlon,resolution='h')
    
    # Create grid for mapping
    xx,yy = m(d['lon'].values,d['lat'].values)
    
#    # Calculate 2D histogram
#    H, xedges, yedges = np.histogram2d(d['xgridded'].values,d['ygridded'].values,bins=len(d['lat']))
    H, xedges, yedges = np.histogram2d(np.append(d['xgridded'].values,[0,BinNo]),np.append(d['ygridded'].values,[0,BinNo]),bins=BinNo)
    # Rotate and flip H...
    H = np.rot90(H)
    H = np.flipud(H)
     
    # Mask zeros
    Hmasked = np.ma.masked_where(H<2.1,H)
     
    # Log H for better display
    Hmasked = np.log10(Hmasked)
     
    m = Basemap(projection='mill', llcrnrlat=minlat,urcrnrlat=maxlat,llcrnrlon=minlon, urcrnrlon=maxlon,resolution='h')
    # Make map
    fig = plt.figure(figsize=(18,9))


    
    

    
    
    # TOPO
    # Read data from: http://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.html
    # using the netCDF output option
    import urllib.request
    import netCDF4
    isub = 5
    base_url='http://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.nc?'
    query='topo[(%f):%d:(%f)][(%f):%d:(%f)]' % (maxlat,isub,minlat,minlon,isub,maxlon)
    url = base_url+query
    # store data in NetCDF file
    file='usgsCeSrtm30v6.nc'
    urllib.request.urlretrieve(url, file)
    # open NetCDF data in 
    nc = netCDF4.Dataset(file)
    ncv = nc.variables
    lon = ncv['longitude'][:]
    lat = ncv['latitude'][:]
    lons, lats = np.meshgrid(lon,lat)
    topo = ncv['topo'][:,:]
    
    
    
#    # My-cmaps ===============================================================
#    cdict = {'red': ((0.0, 0.0, 0.0),
#                     (1.0, 0.7, 0.7)),
#           'green': ((0.0, 0.25, 0.25),
#                     (1.0, 0.85, 0.85)),
#            'blue': ((0.0, 0.5, 0.5),
#                     (1.0, 1.0, 1.0))}
#    my_cmap = LinearSegmentedColormap('my_colormap',cdict,256)
    
    cdict = {'red': ((0.0, 0.0, 0.0), # Dark
                     (1.0, 0.9, 0.9)), # Light
           'green': ((0.0, 0.9, 0.9),
                     (1.0, 1.0,1.0)),
            'blue': ((0.0, 0.9, 0.9),
                     (1.0, 1.0, 1.0))}
    my_cmap_lightblue = LinearSegmentedColormap('my_colormap',cdict,256)
    
#    # My-cmap
#    cdict = {'red': ((0.0, 1.0, 1.0),
#                     (1.0, 0.5, 0.5)),
#           'green': ((0.0, 1.0, 1.0),
#                     (1.0, 0.0, 0.0)),
#            'blue': ((0.0, 0.0, 0.0),
#                     (1.0, 0.0, 0.0))}
#    my_cmap_yellow2red = LinearSegmentedColormap('my_colormap',cdict,256)
    
    # My-cmap
    cdict = {'red': ((0.0, 1.0, 1.0),
                     (1.0, 0.5, 0.5)),
           'green': ((0.0, 0.85, 0.85),
                     (1.0, 0.0, 0.0)),
            'blue': ((0.0, 0.3, 0.3),
                     (1.0, 0.0, 0.0))}
    my_cmap_amber2red = LinearSegmentedColormap('my_colormap',cdict,256)
#    # My-cmaps ===============================================================
    
    
    
    
    TOPOmasked = np.ma.masked_where(topo>0,topo)
    
    # Log H for better display
#    TOPOmasked = -(np.log10(-TOPOmasked))
    
#    cs = m.pcolormesh(lons,lats,TOPOmasked,cmap=plt.get_cmap('Blues_r'),latlon=True,zorder=5)
#    cs = m.pcolormesh(lons,lats,TOPOmasked,cmap=plt.get_cmap('Greys_r'),latlon=True,zorder=5)
#    cs = m.pcolormesh(lons,lats,TOPOmasked,cmap=cmocean.cm.deep_r,latlon=True,zorder=5)
    cs = m.pcolormesh(lons,lats,TOPOmasked,cmap=my_cmap_lightblue,latlon=True,zorder=5)

    

    
    
    # For topo
    x,y = m(lons,lats)
    depth_levels = [-1000,-900,-800,-700,-600,-500,-400,-300,-200,-150,-100,-75,-50,-20]
#    depth_levels = [-5000, -4000, -3000, -2000,-1000,-500,-400,-300,-200,-100]
#    depth_levels = np.linspace(TOPOmasked.min(), TOPOmasked.max(), 30)
#    cs = plt.contour(x,y,topo,depth_levels,cmap=plt.get_cmap('Greys'),linewidths=1,linestyles='solid',zorder=7)
    cs = plt.contour(x,y,topo,depth_levels,cmap=plt.get_cmap('Blues_r'),linewidths=1,linestyles='solid',zorder=7)
#    cs = plt.contour(x,y,topo,depth_levels,colors='#737373',linewidths=1,linestyles='solid',zorder=7,inline_spacing=0)
#    cs = plt.contourf(x,y,topo,depth_levels,cmap=my_cmap,linewidths=1,linestyles='solid',zorder=7)
#    plt.clabel(cs,fmt='%i') 
    
    
#    cs = m.pcolor(xx,yy,Hmasked, cmap=plt.get_cmap('jet'),zorder=10)
    cs = m.pcolor(xx,yy,Hmasked, cmap=my_cmap_amber2red,zorder=10)
#    cs = m.pcolor(xx,yy,Hmasked, cmap=cmocean.cm.amp,zorder=10)

    
    
    
    # Polygon +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    from matplotlib.patches import Polygon
        
    poly_lats = [44.0203, 41.225982, 41.6064488, 44.910864,]
    poly_lons = [-59.9863, -57.10252, -56.3708845,-56.86052,]
    poly_x, poly_y = m(poly_lons, poly_lats)
#    poly_xy = zip(poly_x,poly_y)
    poly_xy = np.transpose(np.array((poly_x,poly_y)))
    print(poly_xy)
    poly = Polygon(poly_xy, closed=True, edgecolor='red', alpha=0.8, fill=False, zorder=15)
    plt.gca().add_patch(poly)
    
    
    
    
    m.drawcoastlines(zorder=25)
    m.fillcontinents()
    m.drawmapboundary()
    
    
    def setcolor(x, color):
         for m in x:
             for t in x[m][1]:
                 t.set_color(color)
    
    
    
    parallels = np.arange(minlat,maxlat,1)
    # labels = [left,right,top,bottom]
    par = m.drawparallels(parallels,labels=[True,False,False,False],dashes=[1,2],color='#00a3cc', zorder=25)
    setcolor(par,'#00a3cc')                      
    meridians = np.arange(minlon,maxlon,1)
    mers =  m.drawmeridians(meridians,labels=[False,False,False,True],dashes=[1,2],color='#00a3cc', zorder=25)
    setcolor(mers,'#00a3cc') 
    
    
    plt.title('Vessels density (' + str(BinNo,) + ' X ' + str(BinNo,) + ' grid) from file:' + filename +
              '\n Filter: Apparent speed between ' + str(downLim) + ' and ' + str(upLim) + ' knots')
    cbar = plt.colorbar(extend='both')
    
    
    label_values = cbar._tick_data_values
    log_label_values = np.round(10 ** label_values,decimals=0)
    labels = []
    for log_label_value in log_label_values:
        labels.append(str(int(log_label_value)))
    
    cbar.ax.set_yticklabels(labels)

    
    
    cbar.ax.set_xlabel('No. of vessels \n within grid-cell')
    
#    mng = plt.get_current_fig_manager()
#    mng.frame.Maximize(True)
#    
#    plt.show()
    
#    pngDir = 'C:\\Users\\IbarraD\\Documents\\VMS\\png\\'
#    plt.savefig(datadir[0:-5] + 'png\\' + filename + '- Grid' + str(BinNo) + ' - Filter' +str(downLim) + '-' + str(upLim) + '.png')
    plt.savefig('test.png')
    
    return

if __name__ == "__main__":
    filename = '2012-2018 - Select Vessels - Clipped'
    datadir = 'C:\\Users\\IbarraD\\Documents\\VMS\\data_2012-2018 - Selected Vessels\\'
    BinNo = 300
    downLim = 1 # Knots
    upLim = 4.5 # Knots
    map_density(BinNo,downLim,upLim,datadir,filename,spatial=[41.5,46,-61,-55])
