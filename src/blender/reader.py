import bpy
import json
import mmap

bufferName = None
bufferSize = 0

def read_buffer():
    try:
        mem = mmap.mmap(-1, bufferSize, tagname=bufferName, access=mmap.ACCESS_READ)
        raw = mem.read(bufferSize)
        mem.close()

        raw = raw.split(b'\x00', 1)[0]
        if not raw:
            return 0.1
        
        text = raw.decode('utf-8', errors='ignore')
        try:
            payload = json.loads(text)
            print(f"[Carl3D] Payload: ", payload)
        except json.JSONDecodeError:
            print(f"[Carl3D] Error: ", text)

    except OSError:
        pass
    except Exception as e:
        print(f"[Carl3D] Failed to read buffer: {e}")

    return 0.1

def register(bN, bS):
    global bufferName, bufferSize
    bufferName = bN
    bufferSize = int(bS)
    bpy.app.timers.register(read_buffer)

def unregister():
    bpy.app.timers.unregsiter(read_buffer)
    pass

if __name__ == "__main__":
    register("Local\\C3DOUTPUT", 1024)
