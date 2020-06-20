from matplotlib import pyplot as plt
import numpy as np
import matplotlib as mpl
from draw_ball_field import draw_court

cdict = {
    'blue': [(0.0, 0.6313725709915161, 0.6313725709915161), (0.25, 0.4470588266849518, 0.4470588266849518), (0.5, 0.29019609093666077, 0.29019609093666077), (0.75, 0.11372549086809158, 0.11372549086809158), (1.0, 0.05098039284348488, 0.05098039284348488)],
    'green': [(0.0, 0.7333333492279053, 0.7333333492279053), (0.25, 0.572549045085907, 0.572549045085907), (0.5, 0.4156862795352936, 0.4156862795352936), (0.75, 0.0941176488995552, 0.0941176488995552), (1.0, 0.0, 0.0)],
    'red': [(0.0, 0.9882352948188782, 0.9882352948188782), (0.25, 0.9882352948188782, 0.9882352948188782), (0.5, 0.9843137264251709, 0.9843137264251709), (0.75, 0.7960784435272217, 0.7960784435272217), (1.0, 0.40392157435417175, 0.40392157435417175)]
}

mymap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)



def find_shootingPcts(shot_df, gridNum):
    x = shot_df.loc_x[shot_df['loc_y']<425.1] #i want to make sure to only include shots I can draw
    y = shot_df.loc_y[shot_df['loc_y']<425.1]

    x_made = shot_df.loc_x[(shot_df['shot_made_flag']==1) & (shot_df['loc_y']<425.1)]
    y_made = shot_df.loc_y[(shot_df['shot_made_flag']==1) & (shot_df['loc_y']<425.1)]

    #compute number of shots made and taken from each hexbin location
    hb_shot = plt.hexbin(x, y, gridsize=gridNum, extent=(-250,250,425,-50));
    plt.close() #don't want to show this figure!
    hb_made = plt.hexbin(x_made, y_made, gridsize=gridNum, extent=(-250,250,425,-50),cmap=plt.cm.Reds);
    plt.close()

    #compute shooting percentage
    ShootingPctLocs = hb_made.get_array() / hb_shot.get_array()
    ShootingPctLocs[np.isnan(ShootingPctLocs)] = 0 #makes 0/0s=0
    return (ShootingPctLocs, hb_shot)



def acquire_playerPic(PlayerID, zoom, offset=(250,400)):
    from matplotlib import  offsetbox as osb
    import urllib
    pic = urllib.urlretrieve("http://stats.nba.com/media/players/230x185/"+PlayerID+".png",PlayerID+".png")
    player_pic = plt.imread(pic[0])
    img = osb.OffsetImage(player_pic, zoom)
    #img.set_offset(offset)
    img = osb.AnnotationBbox(img, offset,xycoords='data',pad=0.0, box_alignment=(1,0), frameon=False)
    return img



def shooting_plot(shot_df, plot_size=(12,8),gridNum=30):
    from matplotlib.patches import Circle
    x = shot_df.loc_x[shot_df['loc_y']<425.1]
    y = shot_df.loc_y[shot_df['loc_y']<425.1]

    #compute shooting percentage and # of shots
    (ShootingPctLocs, shotNumber) = find_shootingPcts(shot_df, gridNum)

    #draw figure and court
    fig = plt.figure(figsize=plot_size)#(12,7)
    cmap = mymap #my modified colormap
    ax = plt.axes([0.1, 0.1, 0.8, 0.8]) #where to place the plot within the figure
    draw_court(outer_lines=False)
    plt.xlim(-250,250)
    plt.ylim(400, -25)

    #draw player image
    #zoom = np.float(plot_size[0])/(12.0*2) #how much to zoom the player's pic. I have this hackily dependent on figure size
    #img = acquire_playerPic(PlayerID, zoom)
    #ax.add_artist(img)

    #draw circles
    for i, shots in enumerate(ShootingPctLocs):
        restricted = Circle(shotNumber.get_offsets()[i], radius=shotNumber.get_array()[i],
                            color=cmap(shots),alpha=0.8, fill=True)
        if restricted.radius > 240/gridNum: restricted.radius=240/gridNum
        ax.add_patch(restricted)

    #draw color bar
    ax2 = fig.add_axes([0.92, 0.1, 0.02, 0.8])
    cb = mpl.colorbar.ColorbarBase(ax2,cmap=cmap, orientation='vertical')
    cb.set_label('Shooting %')
    cb.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
    cb.set_ticklabels(['0%','25%', '50%','75%', '100%'])

    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()
    return ax