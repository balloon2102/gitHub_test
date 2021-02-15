
bl_info = {
    "name": "advanced duplicate",
    "author": "copy bone chain",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D >  re name",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "bone",#맘대로 해도 상관 없음
}
    
# 1. 


import bpy
class rename_bone_chain(bpy.types.Panel):
    bl_label = "copy chain"
    bl_idname = "OBJECT_PT_advanced_copy_bone"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ad copy"

    def draw(self, context):
        layout = self.layout


        row = layout.row()
        row.operator("wm.myop")

class WM_OT_myOp(bpy.types.Operator):
    bl_label = "복제 하기"
    bl_idname = "wm.myop"
    # At what point does the function actually work?
    src_text = bpy.props.StringProperty(name = '바꾸고싶은 단어 :') 
    tgt_text = bpy.props.StringProperty(name = '바뀌어질 단어 :')
    parent_get = bpy.props.BoolProperty(name = '부모화 여부', default = False )


    # True of False return
    def execute(self, context):
          
        src_text = self.src_text
        tgt_text = self.tgt_text  
        parent_get = self.parent_get  
        # The function stops once and gets the next argument, where can I know that?
        dup_and_remane_chain(src = src_text, tgt= tgt_text, parent = parent_get)
        
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
        

def register():
    bpy.utils.register_class(rename_bone_chain)
    bpy.utils.register_class(WM_OT_myOp)

def unregister():
    bpy.utils.unregister_class(rename_bone_chain)
    bpy.utils.register_class(WM_OT_myOp)

if __name__ == "__main__":
    register()
    bpy.ops.wm.myop('INVOKE_DEFAULT')


def dup_and_remane_chain(src='', tgt= '', parent = True):
    arm = bpy.context.object.data
    bone_list =  bpy.context.selected_bones
    for b in bone_list:
        bone = b.name.replace(src, tgt)
        cb = arm.edit_bones.new(bone)
        cb.head = b.head
        cb.tail = b.tail
        cb.matrix = b.matrix
        
        if parent == True:
            cb.parent = b
        
        
        cb.select = True
        cb.select_head = True
        cb.select_tail = True
        
        b.select = False
        b.select_head = False
        b.select_tail = False
        
#dup_and_remane_chain(src='CTRL', tgt= 'MCH', parent = False)