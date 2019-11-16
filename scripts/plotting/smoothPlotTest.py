"""
The main driver script for plotting
"""

from old.databaseFuncs import get_conn
from gpxfuncs import loadgpxfiles
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import shapely.geometry as sgeom
import cartopy.io.img_tiles as cimgt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd


def setup_fig():
    sns.set(font_scale=1.6)
    stamen_terrain = cimgt.Stamen('terrain')
    fig = plt.figure(figsize=[10, 8])                                           # setup fig
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.add_image(stamen_terrain, 13)
    ax.set_extent([-66.025, -66.057, 18.025, 18.075], ccrs.Geodetic())  # left right down up
    fig.subplots_adjust(top=0.950,
                        bottom=0,
                        left=0,
                        right=1,
                        hspace=0.27,
                        wspace=0.02)
    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(False)
    ax.coastlines(resolution='50m', color='black', zorder=3)
    ax.stock_img()

    ax.set_title('Mulas Puerto Rico System [Rough Draft]')

    return fig, ax


def plot_track(fig, ax, files):
    clean = pd.read_csv(r'C:\Users\Jashan\PycharmProjects\ewb-pr\scripts\database\final_tracks.csv')

    # create line for plot
    line = sgeom.LineString(zip(clean['long'], clean['lat']))

    ax.add_geometries([line], ccrs.PlateCarree(),  # add to plot
                      facecolor='none', edgecolor='blue',
                      linewidth=2, label='Trajectories')
    print(f'track has been plotted')

    print('All Tracks have been added')
    print('Generating plot')

    # legend features
    patches = [mpatches.Rectangle((0, 0), 1, 1, facecolor='blue'),
               mpatches.Rectangle((0, 0), 1, 1, facecolor='red')]
    labels = ['Distribution Path', 'Points of Interest']
    ax.legend(handles=patches, loc='lower left',
              fancybox=True, labels=labels,
              bbox_to_anchor=(-0.1, 0.01))

    plt.show()


if __name__ == "__main__":
    conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')
    files = loadgpxfiles()

    fig, ax = setup_fig()
    plot_track(fig, ax, files)
