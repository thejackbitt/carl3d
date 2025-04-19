import bpy
import json
import mmap

# Shared memory settings
bufferName = None
bufferSize = 0

data_state = {"view": None, "proj": None}

def write_buffer(payload: dict):
    """
    Write JSON payload into the shared memory buffer.
    """
    try:
        # Open the named shared memory mapping
        mem = mmap.mmap(-1, bufferSize, tagname=bufferName, access=mmap.ACCESS_WRITE)
        # Serialize and write
        data_bytes = json.dumps(payload).encode('utf-8')
        mem.seek(0)
        mem.write(data_bytes[:bufferSize-1])
        mem.write(b'\x00')  # Null-terminate
        mem.close()
    except Exception as e:
        print(f"[Carl3D] Failed to write to buffer: {e}")


def capture_view():
    """
    Timer callback: checks all 3D viewports for view changes, writes on change.
    Returns interval (in seconds) for next run.
    """
    global data_state
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                # Find the region
                region = next(r for r in area.regions if r.type == 'WINDOW')
                rv3d = area.spaces.active.region_3d
                width, height = region.width, region.height
                # Extract matrices and camera position
                view_mat = rv3d.view_matrix
                proj_mat = rv3d.perspective_matrix
                view_list = [list(row) for row in view_mat]
                proj_list = [list(row) for row in proj_mat]
                cam_pos = list(rv3d.view_matrix.inverted().translation)
                state = (tuple(sum(view_list, [])), tuple(sum(proj_list, [])))
                # On change, write payload
                if state != (data_state['view'], data_state['proj']):
                    payload = {
                        "view_width": width,
                        "view_height": height,
                        "view_matrix": view_list,
                        "projection_matrix": proj_list,
                        "camera_position": cam_pos,
                    }
                    write_buffer(payload)
                    data_state['view'], data_state['proj'] = state
                return 0.1  # check every 0.1s
    return 0.1

def render_handler(scene):
    """
    Pre-render handler: writes active camera's transform & projection.
    """
    cam = scene.camera
    if cam:
        # Invert camera world matrix to get view matrix
        view_mat = cam.matrix_world.inverted()
        width = scene.render.resolution_x
        height = scene.render.resolution_y
        # Calculate camera projection matrix
        deps = bpy.context.evaluated_depsgraph_get()
        proj_mat = cam.calc_matrix_camera(
            deps,
            x=width, y=height,
            scale_x=scene.render.pixel_aspect_x,
            scale_y=scene.render.pixel_aspect_y
        )
        view_list = [list(row) for row in view_mat]
        proj_list = [list(row) for row in proj_mat]
        cam_pos = list(cam.matrix_world.translation)
        payload = {
            "view_width": width,
            "view_height": height,
            "view_matrix": view_list,
            "projection_matrix": proj_list,
            "camera_position": cam_pos,
        }
        write_buffer(payload)

def register(bN, bS):
    global bufferName, bufferSize
    bufferName = bN
    bufferSize = int(bS)
    bpy.app.timers.register(capture_view)
    bpy.app.handlers.render_pre.append(render_handler)

def unregister():
    # Remove render handler
    if render_handler in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.remove(render_handler)
    # Timers auto-stop when addon is disabled

if __name__ == "__main__":
    register()
