from io import BytesIO
from concurrent import futures

import rasterio
from rasterio.warp import transform_bounds

from rio_tiler.main import tile
from rio_tiler.utils import array_to_img
from rio_tiler import profiles as TileProfiles

from tornado import web
from tornado import gen
from tornado.httpserver import HTTPServer
from tornado.concurrent import run_on_executor


class TileServer(object):
    """creates a very minimal slippy map tile server
    uses the jupyter notebook tornado.ioloop"""

    def __init__(self, path, bidx=None, nodata=None, tile_format='png', tile_size=512, port=8080):
        self.path = path
        self.port = port
        self.tilesize = tile_size
        self.tileformat = tile_format

        if bidx:
            bidx = [int(b) for b in bidx.split(',')]

        # TODO: Check if the raster is a CloudOptimized Geotiff

        with rasterio.open(path) as src:
            self.bounds = list(transform_bounds(*[src.crs, 'epsg:4326'] + list(src.bounds), densify_pts=0))
            self.nodata = nodata if nodata is not None else src.nodata
            self.indexes = bidx if bidx is not None else src.indexes

        app_params = dict(
            path=self.path,
            indexes=self.indexes,
            nodata=self.nodata,
            tilesize=self.tilesize,
            tileformat=self.tileformat)

        application = web.Application([
            (r'^/tiles/(\d+)/(\d+)/(\d+)\.\w+$', RasterTileHandler, app_params),
            (r"/.*", ErrorHandler)])

        self.server = HTTPServer(application)

    def get_bounds(self):
        return list(self.bounds)

    def get_center(self):
        lat = (self.bounds[3] - self.bounds[1]) / 2 + self.bounds[1]
        lng = (self.bounds[2] - self.bounds[0]) / 2 + self.bounds[0]
        return [lng, lat]

    def get_url(self):
        return 'http://127.0.0.1:8080/tiles/{{z}}/{{x}}/{{y}}.{}'.format(self.tileformat)

    def start(self):
        self.server.listen(self.port)

    def stop(self):
        self.server.stop()


class ErrorHandler(web.RequestHandler):
    def get(self):
        raise web.HTTPError(404)


class RasterTileHandler(web.RequestHandler):
    """
    """
    executor = futures.ThreadPoolExecutor(max_workers=16)

    def initialize(self, path, indexes, nodata, tilesize, tileformat):
        self.path = path
        self.nodata = nodata
        self.indexes = indexes
        self.tilesize = tilesize
        self.tileformat = 'jpeg' if tileformat == 'jpg' else tileformat

    @run_on_executor
    def _get_tile(self, z, x, y):
        data, mask = tile(self.path, int(x), int(y), int(z), rgb=self.indexes, tilesize=self.tilesize, nodata=self.nodata)
        img = array_to_img(data, mask=mask)
        params = TileProfiles.get(self.tileformat)
        if self.tileformat == 'jpeg':
            img = img.convert('RGB')

        sio = BytesIO()
        img.save(sio, self.tileformat.upper(), **params)
        sio.seek(0)
        return sio

    @gen.coroutine
    def get(self, z, x, y):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET')
        self.set_header('Content-Type', 'image/{}'.format(self.tileformat))
        # self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        res = yield self._get_tile(z, x, y)
        self.write(res.getvalue())
