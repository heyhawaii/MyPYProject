#-*-coding: UTF-8-*-
from distutils.core import setup
import py2exe
# Powered by ***
INCLUDES = []
options = {"py2exe" :  
    {}}  
setup(
    options = options, 
    description = "DouYu SSH ×Ô¶¯µÇÂ¼",  
    zipfile=None,
    console=[{"script": "DouYuConnector.py"}],
    )