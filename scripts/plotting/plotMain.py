"""
The main driver script for plotting
"""

from databaseFuncs import get_conn, get_poi, get_track
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import shapely.geometry as sgeom
import cartopy.io.img_tiles as cimgt


def setup_fig():
    stamen_terrain = cimgt.Stamen('terrain')
    fig = plt.figure(figsize=[10, 8])                                           # setup fig
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.add_image(stamen_terrain, 14)
    ax.set_extent([-66.025, -66.057, 18.025, 18.065], ccrs.Geodetic())  # left right down up
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


def plot_poi(conn, fig, ax):

    points = get_poi(conn)
    print(points[0])

    for point in points:
        ax.plot(point[3], point[2], marker='*', color='red', markersize=10, alpha=0.9,
                transform=ccrs.Geodetic(), label=point[1])

    print('All points of interest have been plotted')


def plot_track(conn, fig, ax):

    tracks = get_track(conn)

    lats = []
    longs = []
    elevation = []
    # todo: this needs to be improved as far as efficciency goes big time
    for track in tracks:
        lats.append(track[1])
        longs.append(track[2])
        elevation.append(track[3])

    # create line for plot
    line = sgeom.LineString(zip(longs, lats))

    ax.add_geometries([line], ccrs.PlateCarree(),  # add to plot
                      facecolor='none', edgecolor='blue',
                      linewidth=0.5, label='Trajectories')
    print('All Tracks Plotted')
    plt.show()


if __name__ == "__main__":
    conn = get_conn(r'C:\Users\Jashan\PycharmProjects\ewb-pr\data\gpspoints.db')

    fig, ax = setup_fig()
    plot_poi(conn, fig, ax)
    plot_track(conn, fig, ax)
