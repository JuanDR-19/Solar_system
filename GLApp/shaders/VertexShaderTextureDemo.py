import pygame
from OpenGL.GL import *
from GLApp.BaseApps.BaseScene import BaseScene
from GLApp.Camera.Camera import Camera
from GLApp.Mesh.Light.Planet import Planet
from GLApp.Mesh.Light.ObjTextureMesh import ObjTextureMesh
from GLApp.Transformations.Transformations import identity_mat, scale, rotate, translate
from GLApp.Utils.Utils import create_program
import math

vertex_shader = r'''
#version 330 core

in vec3 position;
in vec3 vertexColor;
in vec3 vertexNormal;
in vec2 vertexUv;

uniform mat4 projectionMatrix;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;

out vec3 color;
out vec3 normal;
out vec3 fragPos;
out vec3 lightPos;
out vec3 viewPos;
out vec2 uv;
void main()
{
    lightPos = vec3(5, 5, 5);
    viewPos = vec3(inverse(modelMatrix) * vec4(viewMatrix[3][0], viewMatrix[3][1], viewMatrix[3][2], 1));
    gl_Position = projectionMatrix * inverse(viewMatrix) * modelMatrix * vec4(position, 1);
    normal = mat3(transpose(inverse(modelMatrix))) * vertexNormal;
    //normal = vertexNormal;
    fragPos = vec3(modelMatrix * vec4(position, 1));
    color = vertexColor;
    uv = vertexUv;
}
'''

fragment_shader = r'''
#version 330 core

in vec3 color;
in vec3 normal;
in vec3 fragPos;
in vec3 lightPos;
in vec3 viewPos;

in vec2 uv;
uniform sampler2D tex;

out vec4 fragColor;

void main(){
    
    vec3 lightColor = vec3(1, 1, 1);
    
    //ambient
    float a_strength = 0.1;
    vec3 ambient = a_strength * lightColor;
    
    //diffuse
    vec3 norm = normalize(normal);
    vec3 lightDirection = normalize(lightPos - fragPos);
    float diff = max(dot(norm, lightDirection), 0);
    vec3 diffuse = diff * lightColor;
    
    //specular
    float s_strength = 0.8;
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = normalize(-lightDirection - norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = s_strength * spec * lightColor;
     
    fragColor = vec4(color * (ambient + diffuse + specular), 1);
    fragColor = fragColor * texture(tex, uv);
}
'''


class VertexShaderCameraDemo(BaseScene):

    def __init__(self):
        super().__init__(1000, 800)
        self.vao_ref = None
        self.program_id = None
        self.axes = None
        self.earth = None
        self.mercury = None
        self.venus = None
        self.mars = None
        self.jupiter = None
        self.saturn = None
        self.uranus = None
        self.neptune = None
        self.pluto = None
        self.sun = None
        self.ship = None
        #mercurio y venus no tienen lunas
        self.e_moon = None
        #lunas de marte
        self.fobos = None
        self.deimos = None
        #lunas de jupiter
        #tiene 95 pero solo pondre 6
        self.io = None
        self.europa = None
        self.calisto = None
        self.j_moon_1 = None
        self.j_moon_2 = None
        self.j_moon_3 = None
        #lunas de saturno
        #tiene 146 pero solo pondre 6
        self.mimas = None
        self.encelado = None
        self.tetis = None
        self.titan = None
        self.s_moon_1 = None
        self.s_moon_2 = None
        #lunas de urano
        #tiene 27 pero usare 6
        self.u_moon_1 = None
        self.u_moon_2 = None
        self.u_moon_3 = None
        self.u_moon_4 = None
        self.u_moon_5 = None
        self.u_moon_6 = None
        # lunas de neptuno
        # tiene 14 lunas pero solo usaremos 6
        self.n_moon_1 = None
        self.n_moon_2 = None
        self.n_moon_3 = None
        self.n_moon_4 = None
        self.n_moon_5 = None
        self.n_moon_6 = None
        # Nave
        self.ship_angle_info = [0, 0.1]

    def initialize(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.earth = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/mapamundi301210.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.e_moon = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/e_moon.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.mercury = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/mercury.jpg",
            0,
            0.1,
            0,
            0.02,
            1
        )
        self.venus = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/venus.jpg",
            0,
            0.1,
            0,
            0.03,
            1.5
        )
        self.mars = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/mars.jpg",
            0,
            0.1,
            0,
            0.04,
            2.5
        )
        self.fobos = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/fobos.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.deimos = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/deimos.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.jupiter = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/jupiter.jpg",
            0,
            0.1,
            0,
            0.05,
            3
        )
        self.io = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/io.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.europa = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/europa.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.calisto = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/callisto.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.j_moon_1 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/io.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.j_moon_2 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/europa.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.j_moon_3 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/callisto.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.saturn = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/saturn.jpg",
            0,
            0.1,
            0,
            0.06,
            3.5
        )
        self.mimas = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/mimas.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.encelado = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/encelado.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.tetis = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/tetis.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.titan = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.s_moon_1 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/tetis.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.s_moon_2 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.uranus = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/uranus.jpg",
            0,
            0.1,
            0,
            0.07,
            4
        )
        self.u_moon_1 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.u_moon_2 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.u_moon_3 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.u_moon_4 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.u_moon_5 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.u_moon_6 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.neptune = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/neptune.jpg",
            0,
            0.1,
            0,
            0.08,
            4.5
        )
        self.n_moon_1 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.n_moon_2 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.n_moon_3 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.n_moon_4 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.n_moon_5 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.n_moon_6 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.01,
            2
        )
        self.pluto = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/pluto.jpg",
            0,
            0.1,
            0,
            0.09,
            5
        )
        self.sun = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/8k_sun.jpg",
            0,
            0.1,
            0,
            0.1,
            0
        )
        self.ship = ObjTextureMesh(
            self.program_id,
            "../../assets/models/Fighter_01.obj",
            "../../assets/textures/ship_metal.jpg"
        )
        self.camera = Camera(self.program_id, self.screen.get_width(), self.screen.get_height())
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        camera_transformation = self.camera.transformation

        # Tierra y lunas__________________________________________________________

        self.earth.rotation_angle += self.earth.rotation_speed
        self.earth.rotation_angle %= 360
        self.earth.translation_angle += self.earth.translation_speed
        self.earth.translation_angle %= 360
        transformation = identity_mat()
        transformation = translate(transformation,
                                   self.earth.cal_x(self.earth.orbr, self.earth.translation_angle),
                                   0,
                                   self.earth.cal_z(self.earth.orbr, self.earth.translation_angle))
        transformation = rotate(transformation, self.earth.rotation_angle, "y")
        transformation = scale(transformation, 0.0046, 0.0046, 0.0046)
        self.earth.draw(transformation)

        self.e_moon.rotation_angle += self.e_moon.rotation_speed
        self.e_moon.rotation_angle %= 360
        e_moon_transformation = identity_mat()
        #z es [2,2] en la matriz de transformacion
        e_moon_transformation = rotate(e_moon_transformation, 0.2, "y", False)
        e_moon_transformation = translate(e_moon_transformation, self.earth.cal_x(self.earth.orbr, self.earth.translation_angle),
                                          transformation[1][1],
                                          self.earth.cal_z(self.earth.orbr, self.earth.translation_angle))
        e_moon_transformation = rotate(e_moon_transformation, self.e_moon.rotation_angle, "y")
        e_moon_transformation = scale(e_moon_transformation, 0.0012, 0.0012, 0.0012)
        self.e_moon.draw(e_moon_transformation)

        # Tierra y lunas__________________________________________________________

        # sol__________________________________________________________

        transformation_sun = identity_mat()
        transformation_sun = translate(transformation_sun, 0, 0, 0)
        transformation_sun = scale(transformation_sun, 0.5, 0.5, 0.5)
        self.sun.draw(transformation_sun)

        # sol _________________________________________________________

        self.mercury.rotation_angle += self.mercury.rotation_speed
        self.mercury.rotation_angle %= 360
        self.mercury.translation_angle += self.mercury.translation_speed
        self.mercury.translation_angle %= 360
        transformation_mercury = identity_mat()
        transformation_mercury = translate(transformation_mercury,
                                           self.mercury.cal_x(self.mercury.orbr, self.mercury.translation_angle),
                                           0,
                                           self.mercury.cal_z(self.mercury.orbr, self.mercury.translation_angle))
        transformation_mercury = rotate(transformation_mercury, self.mercury.rotation_angle, "y")
        transformation_mercury = scale(transformation_mercury, 0.0017, 0.0017, 0.0017)
        self.mercury.draw(transformation_mercury)

        self.venus.rotation_angle += self.venus.rotation_speed
        self.venus.rotation_angle %= 360
        self.venus.translation_angle += self.venus.translation_speed
        self.venus.translation_angle %= 360
        transformation_venus = identity_mat()
        transformation_venus = translate(transformation_venus,
                                         self.venus.cal_x(self.venus.orbr, self.venus.translation_angle),
                                         0,
                                         self.venus.cal_z(self.venus.orbr, self.venus.translation_angle))
        transformation_venus = rotate(transformation_venus, self.venus.rotation_angle, "y")
        transformation_venus = scale(transformation_venus, 0.0043, 0.0043, 0.0043)
        self.venus.draw(transformation_venus)

        # marte y lunas__________________________________________________________
        self.mars.rotation_angle += self.mars.rotation_speed
        self.mars.rotation_angle %= 360
        self.mars.translation_angle += self.mars.translation_speed
        self.mars.translation_angle %= 360
        transformation_mars = identity_mat()
        transformation_mars = translate(transformation_mars,
                                        self.mars.cal_x(self.mars.orbr, self.mars.translation_angle),
                                        0,
                                        self.mars.cal_z(self.mars.orbr, self.mars.translation_angle))
        transformation_mars = rotate(transformation_mars, self.mars.rotation_angle, "y")
        transformation_mars = scale(transformation_mars, 0.0024, 0.0024, 0.0024)
        self.mars.draw(transformation_mars)

        self.fobos.rotation_angle += self.fobos.rotation_speed
        self.fobos.rotation_angle %= 360
        self.fobos.translation_angle += self.fobos.translation_speed
        self.fobos.translation_angle %= 360
        transformation_fobos = identity_mat()
        transformation_fobos = rotate(transformation_fobos, 0.2, "y", False)
        transformation_fobos = translate(transformation_fobos,
                                          self.mars.cal_x(self.mars.orbr, self.mars.translation_angle),
                                          transformation_mars[1][1],
                                          self.mars.cal_z(self.mars.orbr, self.mars.translation_angle))
        transformation_fobos = rotate(transformation_fobos, self.e_moon.rotation_angle, "y")
        transformation_fobos = scale(transformation_fobos, 0.00046, 0.00046, 0.00046)
        self.fobos.draw(transformation_fobos)

        self.deimos.rotation_angle += self.deimos.rotation_speed
        self.deimos.rotation_angle %= 360
        self.deimos.translation_angle += self.deimos.translation_speed
        self.deimos.translation_angle %= 360
        transformation_deimos = identity_mat()
        transformation_deimos = rotate(transformation_deimos, 0.3, "y", False)
        transformation_deimos = translate(transformation_deimos,
                                          self.mars.cal_x(self.mars.orbr, self.mars.translation_angle),
                                          transformation_mars[1][1],
                                          self.mars.cal_z(self.mars.orbr, self.mars.translation_angle))
        transformation_deimos = rotate(transformation_deimos, self.e_moon.rotation_angle, "y")
        transformation_deimos = scale(transformation_deimos, 0.00036, 0.00036, 0.00036)
        self.deimos.draw(transformation_deimos)
        # el tamaño de las lunas de marte es mucho menor, pero no se verian

        # marte y lunas__________________________________________________________

        # jupiter y lunas__________________________________________________________
        self.jupiter.rotation_angle += self.jupiter.rotation_speed
        self.jupiter.rotation_angle %= 360
        self.jupiter.translation_angle += self.jupiter.translation_speed
        self.jupiter.translation_angle %= 360
        transformation_jupiter = identity_mat()
        transformation_jupiter = translate(transformation_jupiter,
                                           self.jupiter.cal_x(self.jupiter.orbr, self.jupiter.translation_angle),
                                           0,
                                           self.jupiter.cal_z(self.jupiter.orbr, self.jupiter.translation_angle))
        transformation_jupiter = rotate(transformation_jupiter, self.jupiter.rotation_angle, "y")
        transformation_jupiter = scale(transformation_jupiter, 0.05, 0.05, 0.05)
        self.jupiter.draw(transformation_jupiter)

        self.io.rotation_angle += self.io.rotation_speed
        self.io.rotation_angle %= 360
        self.io.translation_angle += self.io.translation_speed
        self.io.translation_angle %= 360
        transformation_io = identity_mat()
        transformation_io = rotate(transformation_io, 1.5, "y", False)
        transformation_io = translate(transformation_io,
                                      self.jupiter.cal_x(self.jupiter.orbr, self.jupiter.translation_angle),
                                      transformation_jupiter[1][1],
                                      self.jupiter.cal_z(self.jupiter.orbr, self.jupiter.translation_angle))
        transformation_io = rotate(transformation_io, self.io.rotation_angle, "y")
        transformation_io = scale(transformation_io, 0.0013, 0.0013, 0.0013)
        self.io.draw(transformation_io)

        self.europa.rotation_angle += self.europa.rotation_speed
        self.europa.rotation_angle %= 360
        self.europa.translation_angle += self.europa.translation_speed
        self.europa.translation_angle %= 360
        transformation_europa = identity_mat()
        transformation_europa = rotate(transformation_europa, 1.6, "y", False)
        transformation_europa = translate(transformation_europa,
                                          self.jupiter.cal_x(self.jupiter.orbr, self.jupiter.translation_angle),
                                          transformation_jupiter[1][1],
                                          self.jupiter.cal_z(self.jupiter.orbr, self.jupiter.translation_angle))
        transformation_europa = rotate(transformation_europa, self.europa.rotation_angle, "y")
        transformation_europa = scale(transformation_europa, 0.0011, 0.0011, 0.0011)
        self.europa.draw(transformation_europa)

        self.calisto.rotation_angle += self.calisto.rotation_speed
        self.calisto.rotation_angle %= 360
        self.calisto.translation_angle += self.calisto.translation_speed
        self.calisto.translation_angle %= 360
        transformation_calisto = identity_mat()
        transformation_calisto = rotate(transformation_calisto, 1.7, "y", False)
        transformation_calisto = translate(transformation_calisto,
                                           self.jupiter.cal_x(self.jupiter.orbr, self.jupiter.translation_angle),
                                           transformation_jupiter[1][1],
                                           self.jupiter.cal_z(self.jupiter.orbr, self.jupiter.translation_angle))
        transformation_calisto = rotate(transformation_calisto, self.calisto.rotation_angle, "y")
        transformation_calisto = scale(transformation_calisto, 0.0017, 0.0017, 0.0017)
        self.calisto.draw(transformation_calisto)

        self.j_moon_1.rotation_angle += self.j_moon_1.rotation_speed
        self.j_moon_1.rotation_angle %= 360
        self.j_moon_1.translation_angle += self.j_moon_1.translation_speed
        self.j_moon_1.translation_angle %= 360
        transformation_j_moon_1 = identity_mat()
        transformation_j_moon_1 = rotate(transformation_j_moon_1, 1.8, "y", False)
        transformation_j_moon_1 = translate(transformation_j_moon_1,
                                            self.jupiter.cal_x(self.jupiter.orbr, self.jupiter.translation_angle),
                                            transformation_jupiter[1][1],
                                            self.jupiter.cal_z(self.jupiter.orbr, self.jupiter.translation_angle))
        transformation_j_moon_1 = rotate(transformation_j_moon_1, self.j_moon_1.rotation_angle, "y")
        transformation_j_moon_1 = scale(transformation_j_moon_1, 0.0018, 0.0018, 0.0018)
        self.j_moon_1.draw(transformation_j_moon_1)

        self.j_moon_2.rotation_angle += self.j_moon_2.rotation_speed
        self.j_moon_2.rotation_angle %= 360
        self.j_moon_2.translation_angle += self.j_moon_2.translation_speed
        self.j_moon_2.translation_angle %= 360
        transformation_j_moon_2 = identity_mat()
        transformation_j_moon_2 = rotate(transformation_j_moon_2, 1.9, "y", False)
        transformation_j_moon_2 = translate(transformation_j_moon_2,
                                            self.jupiter.cal_x(self.jupiter.orbr, self.jupiter.translation_angle),
                                            transformation_jupiter[1][1],
                                            self.jupiter.cal_z(self.jupiter.orbr, self.jupiter.translation_angle))
        transformation_j_moon_2 = rotate(transformation_j_moon_2, self.j_moon_2.rotation_angle, "y")
        transformation_j_moon_2 = scale(transformation_j_moon_2, 0.0013, 0.0013, 0.0013)
        self.j_moon_2.draw(transformation_j_moon_2)

        self.j_moon_3.rotation_angle += self.j_moon_3.rotation_speed
        self.j_moon_3.rotation_angle %= 360
        self.j_moon_3.translation_angle += self.j_moon_3.translation_speed
        self.j_moon_3.translation_angle %= 360
        transformation_j_moon_3 = identity_mat()
        transformation_j_moon_3 = rotate(transformation_j_moon_3, 2, "y", False)
        transformation_j_moon_3 = translate(transformation_j_moon_3,
                                            self.jupiter.cal_x(self.jupiter.orbr, self.jupiter.translation_angle),
                                            transformation_jupiter[1][1],
                                            self.jupiter.cal_z(self.jupiter.orbr, self.jupiter.translation_angle))
        transformation_j_moon_3 = rotate(transformation_j_moon_3, self.j_moon_3.rotation_angle, "y")
        transformation_j_moon_3 = scale(transformation_j_moon_3, 0.0013, 0.0013, 0.0013)
        self.j_moon_3.draw(transformation_j_moon_3)

        # jupiter y lunas__________________________________________________________

        # saturno y lunas__________________________________________________________
        self.saturn.rotation_angle += self.saturn.rotation_speed
        self.saturn.rotation_angle %= 360
        self.saturn.translation_angle += self.saturn.translation_speed
        self.saturn.translation_angle %= 360
        transformation_saturn = identity_mat()
        transformation_saturn = translate(transformation_saturn,
                                          self.saturn.cal_x(self.saturn.orbr, self.saturn.translation_angle),
                                          0,
                                          self.saturn.cal_z(self.saturn.orbr, self.saturn.translation_angle))
        transformation_saturn = rotate(transformation_saturn, self.saturn.rotation_angle, "y")
        transformation_saturn = scale(transformation_saturn, 0.043, 0.043, 0.043)
        self.saturn.draw(transformation_saturn)

        self.mimas.rotation_angle += self.mimas.rotation_speed
        self.mimas.rotation_angle %= 360
        self.mimas.translation_angle += self.mimas.translation_speed
        self.mimas.translation_angle %= 360
        transformation_mimas = identity_mat()
        transformation_mimas = rotate(transformation_mimas, 1.5, "y", False)
        transformation_mimas = translate(transformation_mimas,
                                         self.saturn.cal_x(self.saturn.orbr, self.saturn.translation_angle),
                                         transformation_saturn[1][1],
                                         self.saturn.cal_z(self.saturn.orbr, self.saturn.translation_angle))
        transformation_mimas = rotate(transformation_mimas, self.mimas.rotation_angle, "y")
        transformation_mimas = scale(transformation_mimas, 0.00046, 0.00046, 0.00046)
        self.mimas.draw(transformation_mimas)

        self.encelado.rotation_angle += self.encelado.rotation_speed
        self.encelado.rotation_angle %= 360
        self.encelado.translation_angle += self.encelado.translation_speed
        self.encelado.translation_angle %= 360
        transformation_encelado = identity_mat()
        transformation_encelado = rotate(transformation_encelado, 1.6, "y", False)
        transformation_encelado = translate(transformation_encelado,
                                            self.saturn.cal_x(self.saturn.orbr, self.saturn.translation_angle),
                                            transformation_saturn[1][1],
                                            self.saturn.cal_z(self.saturn.orbr, self.saturn.translation_angle))
        transformation_encelado = rotate(transformation_encelado, self.encelado.rotation_angle, "y")
        transformation_encelado = scale(transformation_encelado, 0.00046, 0.00046, 0.00046)
        self.encelado.draw(transformation_encelado)

        self.tetis.rotation_angle += self.tetis.rotation_speed
        self.tetis.rotation_angle %= 360
        self.tetis.translation_angle += self.tetis.translation_speed
        self.tetis.translation_angle %= 360
        transformation_tetis = identity_mat()
        transformation_tetis = rotate(transformation_tetis, 1.7, "y", False)
        transformation_tetis = translate(transformation_tetis,
                                         self.saturn.cal_x(self.saturn.orbr, self.saturn.translation_angle),
                                         transformation_saturn[1][1],
                                         self.saturn.cal_z(self.saturn.orbr, self.saturn.translation_angle))
        transformation_tetis = rotate(transformation_tetis, self.tetis.rotation_angle, "y")
        transformation_tetis = scale(transformation_tetis, 0.00036, 0.00036, 0.00036)
        self.tetis.draw(transformation_tetis)

        self.titan.rotation_angle += self.titan.rotation_speed
        self.titan.rotation_angle %= 360
        self.titan.translation_angle += self.titan.translation_speed
        self.titan.translation_angle %= 360
        transformation_titan = identity_mat()
        transformation_titan = rotate(transformation_titan, 1.8, "y", False)
        transformation_titan = translate(transformation_titan,
                                         self.saturn.cal_x(self.saturn.orbr, self.saturn.translation_angle),
                                         transformation_saturn[1][1],
                                         self.saturn.cal_z(self.saturn.orbr, self.saturn.translation_angle))
        transformation_titan = rotate(transformation_titan, self.titan.rotation_angle, "y")
        transformation_titan = scale(transformation_titan, 0.0018, 0.0018, 0.0018)
        self.titan.draw(transformation_titan)

        self.s_moon_1.rotation_angle += self.s_moon_1.rotation_speed
        self.s_moon_1.rotation_angle %= 360
        self.s_moon_1.translation_angle += self.s_moon_1.translation_speed
        self.s_moon_1.translation_angle %= 360
        transformation_s_moon_1 = identity_mat()
        transformation_s_moon_1 = rotate(transformation_s_moon_1, 1.9, "y", False)
        transformation_s_moon_1 = translate(transformation_s_moon_1,
                                            self.saturn.cal_x(self.saturn.orbr, self.saturn.translation_angle),
                                            transformation_saturn[1][1],
                                            self.saturn.cal_z(self.saturn.orbr, self.saturn.translation_angle))
        transformation_s_moon_1 = rotate(transformation_s_moon_1, self.s_moon_1.rotation_angle, "y")
        transformation_s_moon_1 = scale(transformation_s_moon_1, 0.0015, 0.0015, 0.0015)
        self.s_moon_1.draw(transformation_s_moon_1)

        self.s_moon_2.rotation_angle += self.s_moon_2.rotation_speed
        self.s_moon_2.rotation_angle %= 360
        self.s_moon_2.translation_angle += self.s_moon_2.translation_speed
        self.s_moon_2.translation_angle %= 360
        transformation_s_moon_2 = identity_mat()
        transformation_s_moon_2 = rotate(transformation_s_moon_2, 2, "y", False)
        transformation_s_moon_2 = translate(transformation_s_moon_2,
                                            self.saturn.cal_x(self.saturn.orbr, self.saturn.translation_angle),
                                            transformation_saturn[1][1],
                                            self.saturn.cal_z(self.saturn.orbr, self.saturn.translation_angle))
        transformation_s_moon_2 = rotate(transformation_s_moon_2, self.s_moon_2.rotation_angle, "y")
        transformation_s_moon_2 = scale(transformation_s_moon_2, 0.0015, 0.0015, 0.0015)
        self.s_moon_2.draw(transformation_s_moon_2)
        #Gran parte de las lunas tienen un tamaño menor, pero como en marte, no se verian

        # saturno y lunas__________________________________________________________

        # urano y lunas__________________________________________________________
        self.uranus.rotation_angle += self.uranus.rotation_speed
        self.uranus.rotation_angle %= 360
        self.uranus.translation_angle += self.uranus.translation_speed
        self.uranus.translation_angle %= 360
        transformation_uranus = identity_mat()
        transformation_uranus = translate(transformation_uranus,
                                          self.uranus.cal_x(self.uranus.orbr, self.uranus.translation_angle),
                                          0,
                                          self.uranus.cal_z(self.uranus.orbr, self.uranus.translation_angle))
        transformation_uranus = rotate(transformation_uranus, self.uranus.rotation_angle, "y")
        transformation_uranus = scale(transformation_uranus, 0.017, 0.017, 0.017)
        self.uranus.draw(transformation_uranus)

        self.u_moon_1.rotation_angle += self.u_moon_1.rotation_speed
        self.u_moon_1.rotation_angle %= 360
        self.u_moon_1.translation_angle += self.u_moon_1.translation_speed
        self.u_moon_1.translation_angle %= 360
        transformation_u_moon_1 = identity_mat()
        transformation_u_moon_1 = rotate(transformation_u_moon_1, 0.5, "y", False)
        transformation_u_moon_1 = translate(transformation_u_moon_1,
                                            self.uranus.cal_x(self.uranus.orbr, self.uranus.translation_angle),
                                            transformation_uranus[1][1],
                                            self.uranus.cal_z(self.uranus.orbr, self.uranus.translation_angle))
        transformation_u_moon_1 = rotate(transformation_u_moon_1, self.u_moon_1.rotation_angle, "y")
        transformation_u_moon_1 = scale(transformation_u_moon_1, 0.0046, 0.0046, 0.0046)
        self.u_moon_1.draw(transformation_u_moon_1)

        self.u_moon_2.rotation_angle += self.u_moon_2.rotation_speed
        self.u_moon_2.rotation_angle %= 360
        self.u_moon_2.translation_angle += self.u_moon_2.translation_speed
        self.u_moon_2.translation_angle %= 360
        transformation_u_moon_2 = identity_mat()
        transformation_u_moon_2 = rotate(transformation_u_moon_2, 0.6, "y", False)
        transformation_u_moon_2 = translate(transformation_u_moon_2,
                                            self.uranus.cal_x(self.uranus.orbr, self.uranus.translation_angle),
                                            transformation_uranus[1][1],
                                            self.uranus.cal_z(self.uranus.orbr, self.uranus.translation_angle))
        transformation_u_moon_2 = rotate(transformation_u_moon_2, self.u_moon_2.rotation_angle, "y")
        transformation_u_moon_2 = scale(transformation_u_moon_2, 0.002, 0.002, 0.002)
        self.u_moon_2.draw(transformation_u_moon_2)

        self.u_moon_3.rotation_angle += self.u_moon_3.rotation_speed
        self.u_moon_3.rotation_angle %= 360
        self.u_moon_3.translation_angle += self.u_moon_3.translation_speed
        self.u_moon_3.translation_angle %= 360
        transformation_u_moon_3 = identity_mat()
        transformation_u_moon_3 = rotate(transformation_u_moon_3, 0.7, "y", False)
        transformation_u_moon_3 = translate(transformation_u_moon_3,
                                            self.uranus.cal_x(self.uranus.orbr, self.uranus.translation_angle),
                                            transformation_uranus[1][1],
                                            self.uranus.cal_z(self.uranus.orbr, self.uranus.translation_angle))
        transformation_u_moon_3 = rotate(transformation_u_moon_3, self.u_moon_3.rotation_angle, "y")
        transformation_u_moon_3 = scale(transformation_u_moon_3, 0.00046, 0.00046, 0.00046)
        self.u_moon_3.draw(transformation_u_moon_3)

        self.u_moon_4.rotation_angle += self.u_moon_4.rotation_speed
        self.u_moon_4.rotation_angle %= 360
        self.u_moon_4.translation_angle += self.u_moon_4.translation_speed
        self.u_moon_4.translation_angle %= 360
        transformation_u_moon_4 = identity_mat()
        transformation_u_moon_4 = rotate(transformation_u_moon_4, 0.8, "y", False)
        transformation_u_moon_4 = translate(transformation_u_moon_4,
                                            self.uranus.cal_x(self.uranus.orbr, self.uranus.translation_angle),
                                            transformation_uranus[1][1],
                                            self.uranus.cal_z(self.uranus.orbr, self.uranus.translation_angle))
        transformation_u_moon_4 = rotate(transformation_u_moon_4, self.u_moon_4.rotation_angle, "y")
        transformation_u_moon_4 = scale(transformation_u_moon_4, 0.00046, 0.00046, 0.00046)
        self.u_moon_4.draw(transformation_u_moon_4)

        self.u_moon_5.rotation_angle += self.u_moon_5.rotation_speed
        self.u_moon_5.rotation_angle %= 360
        self.u_moon_5.translation_angle += self.u_moon_5.translation_speed
        self.u_moon_5.translation_angle %= 360
        transformation_u_moon_5 = identity_mat()
        transformation_u_moon_5 = rotate(transformation_u_moon_5, 0.9, "y", False)
        transformation_u_moon_5 = translate(transformation_u_moon_5,
                                            self.uranus.cal_x(self.uranus.orbr, self.uranus.translation_angle),
                                            transformation_uranus[1][1],
                                            self.uranus.cal_z(self.uranus.orbr, self.uranus.translation_angle))
        transformation_u_moon_5 = rotate(transformation_u_moon_5, self.u_moon_5.rotation_angle, "y")
        transformation_u_moon_5 = scale(transformation_u_moon_5, 0.002, 0.002, 0.002)
        self.u_moon_5.draw(transformation_u_moon_5)

        self.u_moon_6.rotation_angle += self.u_moon_6.rotation_speed
        self.u_moon_6.rotation_angle %= 360
        self.u_moon_6.translation_angle += self.u_moon_6.translation_speed
        self.u_moon_6.translation_angle %= 360
        transformation_u_moon_6 = identity_mat()
        transformation_u_moon_6 = rotate(transformation_u_moon_6, 1, "y", False)
        transformation_u_moon_6 = translate(transformation_u_moon_6,
                                            self.uranus.cal_x(self.uranus.orbr, self.uranus.translation_angle),
                                            transformation_uranus[1][1],
                                            self.uranus.cal_z(self.uranus.orbr, self.uranus.translation_angle))
        transformation_u_moon_6 = rotate(transformation_u_moon_6, self.u_moon_6.rotation_angle, "y")
        transformation_u_moon_6 = scale(transformation_u_moon_6, 0.002, 0.002, 0.002)
        self.u_moon_6.draw(transformation_u_moon_6)

        # urano y lunas__________________________________________________________

        # neptuno y lunas__________________________________________________________
        self.neptune.rotation_angle += self.neptune.rotation_speed
        self.neptune.rotation_angle %= 360
        self.neptune.translation_angle += self.neptune.translation_speed
        self.neptune.translation_angle %= 360
        transformation_neptune = identity_mat()
        transformation_neptune = translate(transformation_neptune,
                                           self.neptune.cal_x(self.neptune.orbr, self.neptune.translation_angle),
                                           0,
                                           self.neptune.cal_z(self.neptune.orbr, self.neptune.translation_angle))
        transformation_neptune = rotate(transformation_neptune, self.neptune.rotation_angle, "y")
        transformation_neptune = scale(transformation_neptune, 0.017, 0.017, 0.017)
        self.neptune.draw(transformation_neptune)

        self.n_moon_1.rotation_angle += self.n_moon_1.rotation_speed
        self.n_moon_1.rotation_angle %= 360
        self.n_moon_1.translation_angle += self.n_moon_1.translation_speed
        self.n_moon_1.translation_angle %= 360
        transformation_n_moon_1 = identity_mat()
        transformation_n_moon_1 = rotate(transformation_n_moon_1, 0.2, "y", False)
        transformation_n_moon_1 = translate(transformation_n_moon_1,
                                            self.neptune.cal_x(self.neptune.orbr, self.neptune.translation_angle),
                                            transformation_neptune[1][1],
                                            self.neptune.cal_z(self.neptune.orbr, self.neptune.translation_angle))
        transformation_n_moon_1 = rotate(transformation_n_moon_1, self.n_moon_1.rotation_angle, "y")
        transformation_n_moon_1 = scale(transformation_n_moon_1, 0.001, 0.001, 0.001)
        self.n_moon_1.draw(transformation_n_moon_1)

        self.n_moon_2.rotation_angle += self.n_moon_2.rotation_speed
        self.n_moon_2.rotation_angle %= 360
        self.n_moon_2.translation_angle += self.n_moon_2.translation_speed
        self.n_moon_2.translation_angle %= 360
        transformation_n_moon_2 = identity_mat()
        transformation_n_moon_2 = rotate(transformation_n_moon_2, 0.2, "y", False)
        transformation_n_moon_2 = translate(transformation_n_moon_2,
                                            self.neptune.cal_x(self.neptune.orbr, self.neptune.translation_angle),
                                            transformation_neptune[1][1],
                                            self.neptune.cal_z(self.neptune.orbr, self.neptune.translation_angle))
        transformation_n_moon_2 = rotate(transformation_n_moon_2, self.n_moon_2.rotation_angle, "y")
        transformation_n_moon_2 = scale(transformation_n_moon_2, 0.001, 0.001, 0.001)
        self.n_moon_2.draw(transformation_n_moon_2)

        self.n_moon_3.rotation_angle += self.n_moon_3.rotation_speed
        self.n_moon_3.rotation_angle %= 360
        self.n_moon_3.translation_angle += self.n_moon_3.translation_speed
        self.n_moon_3.translation_angle %= 360
        transformation_n_moon_3 = identity_mat()
        transformation_n_moon_3 = rotate(transformation_n_moon_3, 0.2, "y", False)
        transformation_n_moon_3 = translate(transformation_n_moon_3,
                                            self.neptune.cal_x(self.neptune.orbr, self.neptune.translation_angle),
                                            transformation_neptune[1][1],
                                            self.neptune.cal_z(self.neptune.orbr, self.neptune.translation_angle))
        transformation_n_moon_3 = rotate(transformation_n_moon_3, self.n_moon_3.rotation_angle, "y")
        transformation_n_moon_3 = scale(transformation_n_moon_3, 0.001, 0.001, 0.001)
        self.n_moon_3.draw(transformation_n_moon_3)

        self.n_moon_4.rotation_angle += self.n_moon_4.rotation_speed
        self.n_moon_4.rotation_angle %= 360
        self.n_moon_4.translation_angle += self.n_moon_4.translation_speed
        self.n_moon_4.translation_angle %= 360
        transformation_n_moon_4 = identity_mat()
        transformation_n_moon_4 = rotate(transformation_n_moon_4, 0.2, "y", False)
        transformation_n_moon_4 = translate(transformation_n_moon_4,
                                            self.neptune.cal_x(self.neptune.orbr, self.neptune.translation_angle),
                                            transformation_neptune[1][1],
                                            self.neptune.cal_z(self.neptune.orbr, self.neptune.translation_angle))
        transformation_n_moon_4 = rotate(transformation_n_moon_4, self.n_moon_4.rotation_angle, "y")
        transformation_n_moon_4 = scale(transformation_n_moon_4, 0.001, 0.001, 0.001)
        self.n_moon_4.draw(transformation_n_moon_4)

        self.n_moon_5.rotation_angle += self.n_moon_5.rotation_speed
        self.n_moon_5.rotation_angle %= 360
        self.n_moon_5.translation_angle += self.n_moon_5.translation_speed
        self.n_moon_5.translation_angle %= 360
        transformation_n_moon_5 = identity_mat()
        transformation_n_moon_5 = rotate(transformation_n_moon_5, 0.2, "y", False)
        transformation_n_moon_5 = translate(transformation_n_moon_5,
                                            self.neptune.cal_x(self.neptune.orbr, self.neptune.translation_angle),
                                            transformation_neptune[1][1],
                                            self.neptune.cal_z(self.neptune.orbr, self.neptune.translation_angle))
        transformation_n_moon_5 = rotate(transformation_n_moon_5, self.n_moon_5.rotation_angle, "y")
        transformation_n_moon_5 = scale(transformation_n_moon_5, 0.001, 0.001, 0.001)
        self.n_moon_5.draw(transformation_n_moon_5)

        self.n_moon_6.rotation_angle += self.n_moon_6.rotation_speed
        self.n_moon_6.rotation_angle %= 360
        self.n_moon_6.translation_angle += self.n_moon_6.translation_speed
        self.n_moon_6.translation_angle %= 360
        transformation_n_moon_6 = identity_mat()
        transformation_n_moon_6 = rotate(transformation_n_moon_6, 0.2, "y", False)
        transformation_n_moon_6 = translate(transformation_n_moon_6,
                                            self.neptune.cal_x(self.neptune.orbr, self.neptune.translation_angle),
                                            transformation_neptune[1][1],
                                            self.neptune.cal_z(self.neptune.orbr, self.neptune.translation_angle))
        transformation_n_moon_6 = rotate(transformation_n_moon_6, self.n_moon_6.rotation_angle, "y")
        transformation_n_moon_6 = scale(transformation_n_moon_6, 0.001, 0.001, 0.001)
        self.n_moon_6.draw(transformation_n_moon_6)

        # neptuno y lunas__________________________________________________________

        # pluto y lunas__________________________________________________________
        self.pluto.rotation_angle += self.pluto.rotation_speed
        self.pluto.rotation_angle %= 360
        self.pluto.translation_angle += self.pluto.translation_speed
        self.pluto.translation_angle %= 360
        transformation_pluto = identity_mat()
        transformation_pluto = translate(transformation_pluto,
                                         self.pluto.cal_x(self.pluto.orbr, self.pluto.translation_angle),
                                         0,
                                         self.pluto.cal_z(self.pluto.orbr, self.pluto.translation_angle))
        transformation_pluto = rotate(transformation_pluto, self.pluto.rotation_angle, "y")
        transformation_pluto = scale(transformation_pluto, 0.0008, 0.0008, 0.0008)
        self.pluto.draw(transformation_pluto)
        # pluto y lunas__________________________________________________________

        # nave__________________________________________________________

        transformation_ship = self.camera.transformation
        transformation_ship = translate(
            transformation_ship, 0.001, -0.03, -0.09
        )
        transformation_ship = rotate(transformation_ship, 180, "y", local=True)
        transformation_ship = scale(transformation_ship, 0.01, 0.01, 0.01)
        # print(f'{transformation_ship[0, 3]} {transformation_ship[1, 3]} {transformation_ship[2, 3]}')
        # print(
            # f'{self.camera.transformation[0, 3]} {self.camera.transformation[1, 3]} {self.camera.transformation[2, 3]}')
        self.ship.draw(transformation_ship)


if __name__ == '__main__':
    VertexShaderCameraDemo().main_loop()
