import bpy
from pdb import set_trace

def add_spline(bone_chain, crv):
    # gather the data into an appropriate list.
    bone_data = []
    for bone in bone_chain:
        loc = bone.head_local
        bone_data.extend((loc.x, loc.y, loc.z))

    loc = bone_chain[-1].tail_local
    bone_data.extend((loc.x, loc.y, loc.z))

    # construct the spline itself.
    spline = crv.splines.new(type="BEZIER")
    num_points = len(bone_chain)
    spline.bezier_points.add(num_points)
    spline.bezier_points.foreach_set("co", bone_data)
    for point in spline.bezier_points:
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"

def get_bone_chain(arm):
    bone_chain = []

    for bone in arm.bones:
        bone_chain.append( bone )
        if len( bone.children ) != 1:
            yield bone_chain
            bone_chain = []

def make_arm_curve(arm_ob):
    crv = bpy.data.curves.new("crv", type="CURVE")
    crv_ob = bpy.data.objects.new("crv_ob", crv)
    
    for bone_chain in get_bone_chain(arm_ob.data):
        add_spline(bone_chain, crv)
    
    return crv_ob

def bind_curve_to_arm(arm_ob, crv_ob):
    pass
    

class CurveArmatureOp(bpy.types.Operator):
    '''Tooltip'''
    bl_idname = "curve.armature_curve"
    bl_label = "Curve Armature"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        if ob == None:
            return False
        if ob.type != 'ARMATURE':
            return False 
        return True


    def execute(self, context):
        scn = bpy.context.scene
        arm_ob = bpy.context.active_object
        crv_ob = make_arm_curve(arm_ob)
        bind_curve_to_arm(arm_ob, crv_ob)
        scn.objects.link(crv_ob)
        return {'FINISHED'}

class CurveArmaturePanel(bpy.types.Panel):
    bl_label = "Curve Armature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        layout.column().operator("curve.armature_curve")

def register():
    bpy.utils.register_class(CurveArmatureOp)
    bpy.utils.register_class(CurveArmaturePanel)


def unregister():
    bpy.utils.unregister_class(CurveArmatureOp)
    bpy.utils.unregister_class(CurveArmaturePanel)


if __name__ == "__main__":
    register()