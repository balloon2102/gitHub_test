
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



def symmetry_weight(src_vt_sfx = 'R', tgt_vt_sfx = 'L'):#필터링할 서픽스
    vt_list =  bpy.context.selected_objects[0].vertex_groups.items()
    for vt in range(len(vt_list)):
        bpy.context.selected_objects[0].vertex_groups.active_index = vt #이로서 버텍스 그룹을 순차적으로 선택 할 수 있다. 순차적으로 선택 
        sel_vtg = bpy.context.object.vertex_groups.active.name #현제 활성화된  버텍스 그룹의 이름을 안다.  
        if tgt_vt_sfx in sel_vtg :
            trg_vtg_name = bpy.context.object.vertex_groups.active.name.replace( tgt_vt_sfx , src_vt_sfx ) #서픽스를 찾은후 변경한다.
            trg_vtg_ind = bpy.context.object.vertex_groups[trg_vtg_name].index #윗줄에서 서픽스를 바꾼 반대쪽 버텍스 그룹의 인덱스를 확인한다.

            bpy.ops.object.vertex_group_copy() #버텍스 그룹을 카피한다.
            bpy.ops.object.vertex_group_mirror(mirror_weights=True, flip_group_names=False, all_groups=False, use_topology=False) #버텍스 그룹을 미러 시킨다. 
            
            bpy.context.object.vertex_groups.active_index  = trg_vtg_ind #이미 기존에 서픽스가 붙어있는 반대쪽 버텍스그룹을 활성화 시킨다. 
            bpy.ops.object.vertex_group_remove() #삭제를시킨다.
            
            cp_vtg = bpy.context.object.vertex_groups[sel_vtg + "_copy" ].index #처음 버텍스를 미러시킬때 기존에 이미 미러상태의 버텍스 그룹이 있었기 때문에, 서픽스가 갱신된다. 
            print (cp_vtg)
            bpy.context.object.vertex_groups.active_index = cp_vtg #따라서 이 버텍스그룹의 이름을 수정시켜 줘야한다.
            trg_vtg_name = bpy.context.object.vertex_groups.active.name = trg_vtg_name #정상적으로 수정을 완료한다.     



#dup_and_remane_chain(src='CTRL', tgt= 'MCH', parent = False)