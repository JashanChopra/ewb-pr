from gpxfuncs import get_track_names, loadgpxfiles, createcontours_smooth

import pathlib
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import shapely.geometry as sgeom
import cartopy.io.img_tiles as cimgt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import pandas as pd
import os


class TempDir:
    """
    Context manager for working in a directory.
    """
    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = path

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        os.chdir(self.old_dir)


def setup_fig():
    sns.set(font_scale=3)
    stamen_terrain = cimgt.Stamen('terrain')
    fig = plt.figure(figsize=[10, 8])                                           # setup fig
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    original = [-66.025, -66.052, 18.028, 18.068]
    zoomed = [-66.031398, -66.032, 18.05867, 18.059456]
    ax.set_extent(original, ccrs.Geodetic())  # right left down up
    fig.subplots_adjust(top=0.950,
                        bottom=0,
                        left=0,
                        right=1,
                        hspace=0.27,
                        wspace=0.02)
    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(True)
    fig.patch.set_facecolor('none')
    ax.patch.set_alpha(0.0)

    # ax.set_title('Mulas Puerto Rico System [Key Points]')
    return fig, ax


def plot_track(fig, ax, trackdir, plotdir):

    tracks = pd.read_csv(trackdir)
    # titles = get_track_names(tracks)
    titles = ['small sidepath near community end', 'filtration better details',
              'trip to source', 'more accurate points of interest', 'walk along road from sidepath to sidepath',
              'community side trails', 'sidepath (08-06)', 'steep path more details', 'small sidepath',
              'gate to roughing filter', 'extra notes from looped community', 'quick side', 'sidepath 2 (08-06)',
              'more details last path', 'Sun 4 Aug 2019 3:01PM', 'more road points and bridge start',
              'system to first house', 'another path']

    for title in titles:
        lats = []
        longs = []
        # elevation = []
        for index, track in tracks.iterrows():
            if track[1] == title:
                lats.append(track[2])
                longs.append(track[3])
                # elevation.append(track[3])

        # create line for plot
        line = sgeom.LineString(zip(longs, lats))

        ax.add_geometries([line], ccrs.PlateCarree(),  # add to plot
                          facecolor='none', edgecolor='blue',
                          linewidth=2, label='Trajectories')

        print(f'{title} has been plotted')

    print('All Tracks and Points of Interest have been added')
    print('Generating plot')

    # legend features
    patches = [mpatches.Rectangle((0, 0), 1, 1, facecolor='blue'),
               mpatches.Rectangle((0, 0), 1, 1, facecolor='red')]
    labels = ['Distribution Path', 'Points of Interest']
    # ax.legend(handles=patches, loc='lower left',
    #           fancybox=True, labels=labels,
    #           bbox_to_anchor=(-0.1, 0.01))

    plt.figure(dpi=2400)
    with TempDir(plotdir):
        fig.savefig('main.png', transparent=True, dpi=2400)
        print(f'Created figure: Name: main.png')

    plt.show()


def plot_poi(fig, ax, poidir):

    points = pd.read_csv(poidir)

    for index, row in points.iterrows():
        if index in [0, 1, 2]:
            ax.plot(row[3], row[2], marker='*', color='red', markersize=22, alpha=0.9,
                    transform=ccrs.Geodetic())
        if index in [0, 1]:
            ax.text(row[3] + .0008, row[2] + .0005, f'{index}', color='black', transform=ccrs.Geodetic())
        elif index in [2]:
            ax.text(row[3] + .0008, row[2] - .0020, f'{index}', color='black', transform=ccrs.Geodetic())

    print('All points of interest have been plotted')


if __name__ == "__main__":

    # get directories
    homedir = pathlib.PurePath(r'C:\Users\jasha\PycharmProjects\ewb-pr')
    datadir = homedir.joinpath('data')
    poidir = datadir.joinpath('keyPoints.csv')
    trackdir = datadir.joinpath('smoothTest.csv')
    plotdir = homedir.joinpath('mapping')

    # initial file loads
    newfiles = loadgpxfiles()

    # create contours
    contour = createcontours_smooth(newfiles)
    contour.to_csv(r'C:\Users\jasha\PycharmProjects\ewb-pr\data\smoothTest.csv')

    fig, ax = setup_fig()
    plot_poi(fig, ax, poidir)
    plot_track(fig, ax, trackdir, plotdir)