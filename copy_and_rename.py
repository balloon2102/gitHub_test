
bl_info = {
    "name": "New Object",
    "author": "copy bone chain",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}



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
    bl_label = 'text tool'
    bl_idname = "wm.myop"
    
    src_text = bpy.props.StringProperty(name = 'src :')
    tgt_text = bpy.props.StringProperty(name = 'tgt :')
    

    def execute(self, context):
          
        src_text = self.src_text
        tgt_text = self.tgt_text  
          
        dup_and_remane_chain(src = src_text, tgt= tgt_text, parent = True)
        
        
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