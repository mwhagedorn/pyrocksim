try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Py Rocket Sim',
    'author': 'Mike Hagedorn',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'mike@silverchairsolutions.com',
    'version': '0.1',
    'install_requires': ['nose2','couchbase','pyyaml','prettytable','scipy'],
    'packages': ['pyrocketsim'],
    'entry_points' : {
        'console_scripts': ['pyrocksim=pyrocketsim.command_line:main'],
    },
    'entry_points' :{
        'console_scripts':[
            'pyrocksim=pyrocketsim.cli:cli'
            ],
        },
    'test_suite': 'nose.collector',
    'tests_require' : ['nose'],
    'name': 'pyrocketsim'
}

setup(**config)
