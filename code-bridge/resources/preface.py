"""
IGNORE me. 
This is just a preface to make the language server happy.
If it is not meaningful to you, you can safely ignore me.
Copied from built PsychoPy project.
"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard
win = visual.Window( screen=0,
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True,
    units='height', 
    checkTiming=False  # we're going to do this ourselves in a moment
)

thisExp = data.ExperimentHandler(
    name="exp", version='',
    extraInfo={}, runtimeInfo=None,
    originPath='C:\\Users\\spike\\OneDrive\\workspace\\motion-induced-LSNR\\lsnr_only\\main.py',
    savePickle=True, saveWideText=True
)
    # --- Initialize components for Routine "trial" ---