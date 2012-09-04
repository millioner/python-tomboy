### -*- coding: utf-8 -*- ###

try:
    import tomboy
except ImportError:
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))