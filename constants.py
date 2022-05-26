import os

if 'DBPATH' not in os.environ:
    os.environ['DBPATH'] = os.path.dirname(__file__)

dburl='sqlite:///'+os.environ.get('DBPATH','')+'/'+os.environ.get('DBFILENAME','test.db')
hostname = 'localhost'
port = 5000
