# external modules for main
import os
import time
import random
import pyautogui
import playsound
import mss
import mss.tools
from PIL import Image
from typing import List, Set, Tuple, Union, Dict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# my own modules
from .helpers import *
random.seed(0)