from setuptools import setup, find_packages

# Parse the version from the rasterio module.
with open('mapboxgl/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

setup(
    name='mapboxgl',
    version=version,
    description=u"MapboxGL plugin for Jupyter Notebooks",
    long_description="Use Mapbox GL natively in your Jupyter Notebook workflows",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Scientific/Engineering :: GIS'],
    author=u"Ryan Baumann",
    url='https://github.com/mapbox/mapboxgl-jupyter',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={
        'mapboxgl': ['templates/*']},
    include_package_data=True,
    zip_safe=False,
    install_requires=['jupyter', 'jinja2'],
    extras_require={
        'test': ['pytest', 'pytest-cov', 'codecov', 'mock']})
