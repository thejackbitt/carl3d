bl_info = {
    "name": "Carl3D",
    "author": "Jack Bittner",
    "version": (1, 0, 0),
    "blender": (4, 4, 0),
    "location": "3D Viewport > Sidebar > Carl3D",
    "description": "Gaussian Point Rendering + Ray Traced Rendering.",
    "category": "Import-Export"
}

import bpy
import os
import msvcrt
import subprocess
import time
import mmap
import ctypes
from ctypes import wintypes, byref
from . import ply, ui, writer, reader

FILE_MAP_READ = 0x0004

bN = ""
bS = 0
bN2 = ""
bS2 = 0

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
OpenFileMapping = kernel32.OpenFileMappingW
OpenFileMapping.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR)
OpenFileMapping.restype = wintypes.HANDLE
CloseHandle = kernel32.CloseHandle

path = os.path.dirname(__file__)
pathHelper = os.path.join(path, "C3D_HELPER.exe")
process = None

def handshake():
    bufferName = "Local\\C3DINPUT"
    bufferSize = 1024
    bufferName2 = 'Local\\C3DOUTPUT'
    bufferSize2 = 1024
    print(f"[Carl3D] Attempting handshake with C3D_HELPER.exe...")
    for attempt in range(10):
        print(f"[Carl3D] Polling Attempt {attempt}/10...")
        try:
            mem = mmap.mmap(-1, bufferSize, tagname=bufferName, access=mmap.ACCESS_READ)
        except OSError:
            print(f"[Carl3D] No mapping yet.  Retrying...")
            time.sleep(0.1)
            continue
        raw = mem.read(bufferSize)

        mem.close()
        message = raw.split(b"\x00", 1)[0].decode(errors="ignore")
        print(f"[Carl3D] Handshake successful.  Returned: {message!r}")
        # I think it's really flipping stupid that Python makes you specify that a global variable is a global variable
        global bN
        bN = bufferName
        global bS 
        bS = bufferSize
        global bN2
        bN2 = bufferName2
        global bS2
        bS2 = bufferSize2
        return True
    
    print(f"[Carl3D] Handshake failed after 10 attempts.")
    return False

def launchHelper():
    global process
    if process is None:
        try:
            process = subprocess.Popen(
                [pathHelper],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            print(f"[Carl3D] Successfully launched C3D_HELPER.exe")
        except Exception as e:
            print(f"[Carl3D] Failed to launch C3D_HELPER.exe")
    handshake()

def register():
    global bN
    global bS
    launchHelper()
    ui.register()
    ply.register()
    writer.register(bN=bN,
                    bS=bS)
    reader.register(bN=bN2, bS=bS2)
    
def unregister():
    ui.unregister()
    ply.unregister()
    writer.unregister()
    reader.unregister()

if __name__ == "__main__":
    register()