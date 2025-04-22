import bpy
import json
import mmap

bufferName = None
bufferSize = 0

data_state = {"view": None, "proj": None}

def write_buffer(payload: dict):
    if bpy.context.scene.get("gsplat_enable_overlay", True):
        try:
            mem = mmap.mmap(-1, bufferSize, tagname=bufferName, access=mmap.ACCESS_WRITE)
            data_bytes = json.dumps(payload).encode('utf-8')
            mem.seek(0)
            mem.write(data_bytes[:bufferSize-1])
            mem.write(b'\x00')
            mem.close()
        except Exception as e:
            print(f"[Carl3D] Failed to write to buffer: {e}")


def capture_view():
    global data_state
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                region = next(r for r in area.regions if r.type == 'WINDOW')
                rv3d = area.spaces.active.region_3d
                width, height = region.width, region.height
                view_mat = rv3d.view_matrix
                proj_mat = rv3d.perspective_matrix
                view_list = [list(row) for row in view_mat]
                proj_list = [list(row) for row in proj_mat]
                cam_pos = list(rv3d.view_matrix.inverted().translation)
                state = (tuple(sum(view_list, [])), tuple(sum(proj_list, [])))
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
                return 0.1
    return 0.1

def render_handler(scene):
    cam = scene.camera
    if cam:
        view_mat = cam.matrix_world.inverted()
        width = scene.render.resolution_x
        height = scene.render.resolution_y
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
    if render_handler in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.remove(render_handler)

if __name__ == "__main__":
    register()
