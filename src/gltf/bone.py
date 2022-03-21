from gltf.mat import Mat4

class Bone:
    def __init__(self, name, children, rot, trans, scale):
        self.name=name
        self.children = children
        self.trans=trans
        self.rot = [-rot[0], -rot[1], -rot[2], rot[3]]
        rot_mat = Mat4.quaternion_to_matrix(self.rot)
        trans_mat = Mat4.transform_to_matrix([-x for x in trans])
        scale_mat = Mat4.scale_to_matrix(scale)
        self.local_matrix = trans_mat*rot_mat*scale_mat
        self.global_matrix = None

    def to_node(self):
        node = {'name': self.name}
        if self.children!=[]:      
            node['children']=self.children
        node['translation']=self.trans
        node['rotation']=self.rot
        return node

    def bones_to_nodes(bones):
        base_node = {'name': '', 'mesh': 0, 'skin': 0, 'children': [1]}
        nodes = [base_node]+[b.to_node() for b in bones]
        return nodes

    def update_global_matrix_rec(self, matrix, bones):
        self.global_matrix=matrix*self.local_matrix
        #self.matrix_bin = (self.global_matrix*Mat4.quaternion_to_matrix([0, -0.7071, 0, 0.7071])).to_bin()
        self.matrix_bin = self.global_matrix.to_bin()
        for c in self.children:
            bones[c-1].update_global_matrix_rec(self.global_matrix, bones)

    def update_global_matrix(bones):
        for b in bones:
            b.global_matrix = None

        for b in bones:
            if b.global_matrix is None:
                b.update_global_matrix_rec(Mat4.identity(), bones)
        
    