import bpy
import os

class ImportPly(bpy.types.Operator):
    """Import a .ply Gaussian Splat file"""
    bl_idname = "import_gaussian.ply"
    bl_label = "Import Gaussian Splat (.ply)"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if not self.filepath.lower().endswith(".ply"):
            self.report({'ERROR'}, "File must be of type .ply")
            return {'CANCELLED'}

        print(f"[GSPLAT] Importing .ply file: {self.filepath}")
        bpy.ops.wm.ply_import(filepath=self.filepath)

        obj = bpy.context.selected_objects[0]
        obj["is_gsplat"] = True
        obj.name = "Splat"
        obj.data.materials.append(self.create_gsplat_mat())

        self.report({'INFO'}, "Gaussian Splat Imported Successfully!")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def create_gsplat_mat(self):
        mat = bpy.data.materials.new(name="SplatMat")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (1.0, 0.5, 0.0, 1)
            bsdf.inputs['Emission Strength'].default_value = 5.0
        return mat

_classes = [ImportPly]

def register():
    for cls in _classes:
        if not hasattr(bpy.types, cls.__name__):
            bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(_classes):
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
