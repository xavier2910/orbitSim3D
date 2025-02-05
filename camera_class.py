import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from math_utils import *
from vector3 import *

class camera():
    def __init__(self, name, pos, orient, active, lock=None):
        self.name = name
        self.pos = pos
        self.orient = orient
        self.active = active
        self.lock = lock
        self.offset_amount = 100
        
    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def set_pos(self, new_pos):
        req_trans = new_pos - self.pos
        glTranslate(req_trans.x, req_trans.y, req_trans.z)
        self.pos = new_pos

    def move(self, movement):
        if not self.lock:
            glTranslate((movement.x * self.orient.m11) + (movement.y * self.orient.m21) + (movement.z * self.orient.m31),
                        (movement.x * self.orient.m12) + (movement.y * self.orient.m22) + (movement.z * self.orient.m32),
                        (movement.x * self.orient.m13) + (movement.y * self.orient.m23) + (movement.z * self.orient.m33))

            self.pos = vec3(lst=[self.pos.x + (movement.x * self.orient.m11) + (movement.y * self.orient.m21) + (movement.z * self.orient.m31),
                                 self.pos.y + (movement.x * self.orient.m12) + (movement.y * self.orient.m22) + (movement.z * self.orient.m32),
                                 self.pos.z + (movement.x * self.orient.m13) + (movement.y * self.orient.m23) + (movement.z * self.orient.m33)])

        else:
            # this handles zooming in and out
            self.offset_amount += movement.z
            if self.offset_amount <= 0:
                self.offset_amount -= movement.z

    def get_orient(self):
        return self.orient
    
    def get_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def get_lock(self):
        return self.lock

    def rotate(self, rotation):
        about_pos = self.pos
        
        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation[0], self.orient.m11, self.orient.m12, self.orient.m13)
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation[1], self.orient.m21, self.orient.m22, self.orient.m23)
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation[2], self.orient.m31, self.orient.m32, self.orient.m33)
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        self.orient = self.orient.rotate_legacy(rotation)

    def lock_to_target(self, target):
        self.lock = target
        if type(target).__name__ == "body":
            self.offset_amount = target.get_radius() * 3 * visual_scaling_factor
        else:
            self.offset_amount = 100

        self.set_pos(-self.lock.get_draw_pos() - self.orient.vz() * self.offset_amount)

    def unlock(self):
        self.lock = None

    def move_with_lock(self):
        if self.lock:
            self.set_pos(-self.lock.get_draw_pos() - self.orient.vz() * self.offset_amount)
