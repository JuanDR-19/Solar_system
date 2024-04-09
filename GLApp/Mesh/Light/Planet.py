from GLApp.Mesh.Light.ObjTextureMesh import ObjTextureMesh
import math


class Planet(ObjTextureMesh):
    def __init__(self, program_id, filename, texture_filename, ra, rs, ta, ts, orbr):
        super().__init__(program_id, filename, texture_filename)
        self.rotation_angle = ra
        self.rotation_speed = rs
        self.translation_angle = ta
        self.translation_speed = ts * 0.1
        self.orbr = orbr

    @staticmethod
    def cal_x(orb, ta):
        return orb * math.cos(math.radians(ta))

    @staticmethod
    def cal_z(orb, ta):
        return orb * math.sin(math.radians(ta))
