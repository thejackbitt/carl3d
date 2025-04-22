import bpy

class Carl3D_UI(bpy.types.Panel):
    bl_label = "Carl3D"
    bl_idname = "CARL3D_PT_UI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Carl3D"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "gsplat_enable_overlay", text="Enable Viewport Splats")
        layout.operator("import_gaussian.ply", text="Import Gaussian Splat (.ply)")

def register():
    bpy.utils.register_class(Carl3D_UI)
    bpy.types.Scene.gsplat_enable_overlay = bpy.props.BoolProperty(
        name="Enable Viewport Splats",
        description="Toggle live Gaussian splats in viewport",
        default=True
    )

def unregister():
    bpy.utils.unregister_class(Carl3D_UI)
    del bpy.types.Scene.gsplat_enable_overlay