import bpy
from pdb import set_trace

def make_arm_curve(arm_ob):
    crv = bpy.data.curves.new("arm_curve",type="CURVE")
    crv_ob = bpy.data.objects.new("arm_curve_ob", crv)
    
    arm = arm_ob.data
    bones = arm.bones
    
    return crv_ob

def bind_curve_to_arm(arm_ob, crv_ob):
    pass
        

class CurveArmatureOp(bpy.types.Operator):
    '''Tooltip'''
    bl_idname = "curve.armature_curve"
    bl_label = "Curve Armature"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        arm_ob = bpy.context.active_object
        crv_ob = make_arm_curve(arm_ob)
        bind_curve_to_arm(arm_ob, crv_ob)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CurveArmatureOp)


def unregister():
    bpy.utils.unregister_class(CurveArmatureOp)


if __name__ == "__main__":
    register()