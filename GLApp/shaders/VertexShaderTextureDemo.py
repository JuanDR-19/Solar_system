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

    @staticmethod
    def apply_moon_transformation(moon, transformation_matrix, scale_factor, planet):
        moon.translation_angle += moon.translation_speed
        moon.translation_angle %= 360

        # Aplicar transformaciones adicionales a la matriz de transformación
        transformation_matrix = translate(transformation_matrix,
                                          planet.cal_x(planet.orbr, planet.translation_angle),
                                          0,
                                          planet.cal_z(planet.orbr, planet.translation_angle))
        transformation_matrix = translate(transformation_matrix,
                                          moon.cal_x(moon.orbr, moon.translation_angle),
                                          0,
                                          moon.cal_z(moon.orbr, moon.translation_angle))
        transformation_matrix = scale(transformation_matrix, scale_factor, scale_factor, scale_factor)
        return transformation_matrix

    @staticmethod
    def apply_transformation(planet, transformation_planet, scale_factor):
        planet.rotation_angle += planet.rotation_speed
        planet.rotation_angle %= 360
        planet.translation_angle += planet.translation_speed
        planet.translation_angle %= 360
        transformation_planet = translate(transformation_planet,
                                          planet.cal_x(planet.orbr, planet.translation_angle),
                                          0,
                                          planet.cal_z(planet.orbr, planet.translation_angle))
        transformation_planet = rotate(transformation_planet, planet.rotation_angle, "y")
        transformation_planet = scale(transformation_planet, scale_factor, scale_factor, scale_factor)
        planet.draw(transformation_planet)

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
            0.3,
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
            0.5,
            0.13
            # 0.13 distancia de la luna a la tierra en la escala manejada
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
            0.5,
            0.00337
        )
        self.deimos = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/deimos.jpg",
            0,
            0.1,
            0,
            0.7,
            0.0085
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
            0.5,
            0.15
        )
        self.europa = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/europa.jpg",
            0,
            0.1,
            0,
            0.7,
            0.24
        )
        self.calisto = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/callisto.jpg",
            0,
            0.1,
            0,
            0.9,
            0.67
        )
        self.j_moon_1 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/io.jpg",
            0,
            0.1,
            0,
            1.1,
            0.3
        )
        self.j_moon_2 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/europa.jpg",
            0,
            0.1,
            0,
            0.3,
            0.4
        )
        self.j_moon_3 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/callisto.jpg",
            0,
            0.1,
            0,
            0.1,
            0.35
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
            0.5,
            0.0667
        )
        self.encelado = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/encelado.jpg",
            0,
            0.1,
            0,
            0.7,
            0.0856
        )
        self.tetis = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/tetis.jpg",
            0,
            0.1,
            0,
            0.9,
            0.106
        )
        self.titan = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            1.1,
            0.434
        )
        self.s_moon_1 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/tetis.jpg",
            0,
            0.1,
            0,
            0.3,
            0.52
        )
        self.s_moon_2 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.1,
            0.135
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
            0.5,
            0.0179
        )
        self.u_moon_2 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.8,
            0.01935
        )
        self.u_moon_3 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.2,
            0.02128
        )
        self.u_moon_4 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.6,
            0.02222
        )
        self.u_moon_5 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.7,
            0.022545
        )
        self.u_moon_6 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.9,
            0.02690
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
            0.5,
            0.0173
        )
        self.n_moon_2 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.7,
            0.01801
        )
        self.n_moon_3 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.6,
            0.18907
        )
        self.n_moon_4 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.9,
            0.02645
        )
        self.n_moon_5 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            0.8,
            0.04231
        )
        self.n_moon_6 = Planet(
            self.program_id,
            "../../assets/models/smooth-sphere.obj",
            "../../assets/textures/titan.jpg",
            0,
            0.1,
            0,
            1,
            0.12744
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
        transformation = identity_mat()
        self.apply_transformation(self.earth, transformation, 0.0046)

        e_moon_transformation = identity_mat()
        # self.apply_transformation(self.e_moon, e_moon_transformation, 0.0012)
        e_moon_transformation = self.apply_moon_transformation(self.e_moon, e_moon_transformation, 0.0012, self.earth)
        self.e_moon.draw(e_moon_transformation)
        # Tierra y lunas__________________________________________________________

        # sol__________________________________________________________
        transformation_sun = identity_mat()
        transformation_sun = translate(transformation_sun, 0, 0, 0)
        transformation_sun = scale(transformation_sun, 0.5, 0.5, 0.5)
        self.sun.draw(transformation_sun)
        # sol _________________________________________________________

        transformation_mercury = identity_mat()
        self.apply_transformation(self.mercury, transformation_mercury, 0.0017)

        transformation_venus = identity_mat()
        self.apply_transformation(self.venus, transformation_venus, 0.0043)

        # marte y lunas__________________________________________________________
        transformation_mars = identity_mat()
        self.apply_transformation(self.mars, transformation_mars, 0.0024)

        transformation_fobos = identity_mat()
        transformation_fobos = self.apply_moon_transformation(self.fobos, transformation_fobos, 0.00036, self.mars)
        self.fobos.draw(transformation_fobos)

        transformation_deimos = identity_mat()
        transformation_deimos = self.apply_moon_transformation(self.deimos, transformation_deimos, 0.00036, self.mars)
        self.deimos.draw(transformation_deimos)
        # marte y lunas__________________________________________________________

        # jupiter y lunas__________________________________________________________
        transformation_jupiter = identity_mat()
        self.apply_transformation(self.jupiter, transformation_jupiter, 0.05)

        transformation_io = identity_mat()
        transformation_io = self.apply_moon_transformation(self.io, transformation_io, 0.0013, self.jupiter)
        self.io.draw(transformation_io)

        transformation_europa = identity_mat()
        transformation_europa = self.apply_moon_transformation(self.europa, transformation_europa, 0.0011, self.jupiter)
        self.europa.draw(transformation_europa)

        transformation_calisto = identity_mat()
        transformation_calisto = self.apply_moon_transformation(self.calisto, transformation_calisto, 0.0017, self.jupiter)
        self.calisto.draw(transformation_calisto)

        transformation_j_moon_1 = identity_mat()
        transformation_j_moon_1 = self.apply_moon_transformation(self.j_moon_1, transformation_j_moon_1, 0.0018, self.jupiter)
        self.j_moon_1.draw(transformation_j_moon_1)

        transformation_j_moon_2 = identity_mat()
        transformation_j_moon_2 = self.apply_moon_transformation(self.j_moon_2, transformation_j_moon_2, 0.0013, self.jupiter)
        self.j_moon_2.draw(transformation_j_moon_2)

        transformation_j_moon_3 = identity_mat()
        transformation_j_moon_3 = self.apply_moon_transformation(self.j_moon_3, transformation_j_moon_3, 0.0013, self.jupiter)
        self.j_moon_3.draw(transformation_j_moon_3)
        # jupiter y lunas__________________________________________________________

        # saturno y lunas__________________________________________________________
        transformation_saturn = identity_mat()
        self.apply_transformation(self.saturn, transformation_saturn, 0.043)

        transformation_mimas = identity_mat()
        transformation_mimas = self.apply_moon_transformation(self.mimas, transformation_mimas, 0.00046, self.saturn)
        self.mimas.draw(transformation_mimas)

        transformation_encelado = identity_mat()
        transformation_encelado = self.apply_moon_transformation(self.encelado, transformation_encelado, 0.00046,
                                                                 self.saturn)
        self.encelado.draw(transformation_encelado)

        transformation_tetis = identity_mat()
        transformation_tetis = self.apply_moon_transformation(self.tetis, transformation_tetis, 0.00036, self.saturn)
        self.tetis.draw(transformation_tetis)

        transformation_titan = identity_mat()
        transformation_titan = self.apply_moon_transformation(self.titan, transformation_titan, 0.0018, self.saturn)
        self.titan.draw(transformation_titan)

        transformation_s_moon_1 = identity_mat()
        transformation_s_moon_1 = self.apply_moon_transformation(self.s_moon_1, transformation_s_moon_1, 0.0015,
                                                                 self.saturn)
        self.s_moon_1.draw(transformation_s_moon_1)

        transformation_s_moon_2 = identity_mat()
        transformation_s_moon_2 = self.apply_moon_transformation(self.s_moon_2, transformation_s_moon_2, 0.0015,
                                                                 self.saturn)
        self.s_moon_2.draw(transformation_s_moon_2)
        # saturno y lunas__________________________________________________________

        # urano y lunas__________________________________________________________
        transformation_uranus = identity_mat()
        self.apply_transformation(self.uranus, transformation_uranus, 0.017)

        transformation_u_moon_1 = identity_mat()
        transformation_u_moon_1 = self.apply_moon_transformation(self.u_moon_1, transformation_u_moon_1, 0.0046,
                                                                 self.uranus)
        self.u_moon_1.draw(transformation_u_moon_1)

        transformation_u_moon_2 = identity_mat()
        transformation_u_moon_2 = self.apply_moon_transformation(self.u_moon_2, transformation_u_moon_2, 0.002,
                                                                 self.uranus)
        self.u_moon_2.draw(transformation_u_moon_2)

        transformation_u_moon_3 = identity_mat()
        transformation_u_moon_3 = self.apply_moon_transformation(self.u_moon_3, transformation_u_moon_3, 0.0046,
                                                                 self.uranus)
        self.u_moon_3.draw(transformation_u_moon_3)

        transformation_u_moon_4 = identity_mat()
        transformation_u_moon_4 = self.apply_moon_transformation(self.u_moon_4, transformation_u_moon_4, 0.0046,
                                                                 self.uranus)
        self.u_moon_4.draw(transformation_u_moon_4)

        transformation_u_moon_5 = identity_mat()
        transformation_u_moon_5 = self.apply_moon_transformation(self.u_moon_5, transformation_u_moon_5, 0.002,
                                                                 self.uranus)
        self.u_moon_5.draw(transformation_u_moon_5)

        transformation_u_moon_6 = identity_mat()
        transformation_u_moon_6 = self.apply_moon_transformation(self.u_moon_6, transformation_u_moon_6, 0.002,
                                                                 self.uranus)
        self.u_moon_6.draw(transformation_u_moon_6)
        # urano y lunas__________________________________________________________

        # neptuno y lunas__________________________________________________________
        transformation_neptune = identity_mat()
        self.apply_transformation(self.neptune, transformation_neptune, 0.017)

        transformation_n_moon_1 = identity_mat()
        transformation_n_moon_1 = self.apply_moon_transformation(self.n_moon_1, transformation_n_moon_1, 0.001,
                                                                 self.neptune)
        self.n_moon_1.draw(transformation_n_moon_1)

        transformation_n_moon_2 = identity_mat()
        transformation_n_moon_2 = self.apply_moon_transformation(self.n_moon_2, transformation_n_moon_2, 0.001,
                                                                 self.neptune)
        self.n_moon_2.draw(transformation_n_moon_2)

        transformation_n_moon_3 = identity_mat()
        transformation_n_moon_3 = self.apply_moon_transformation(self.n_moon_3, transformation_n_moon_3, 0.001,
                                                                 self.neptune)
        self.n_moon_3.draw(transformation_n_moon_3)

        transformation_n_moon_4 = identity_mat()
        transformation_n_moon_4 = self.apply_moon_transformation(self.n_moon_4, transformation_n_moon_4, 0.001,
                                                                 self.neptune)
        self.n_moon_4.draw(transformation_n_moon_4)

        transformation_n_moon_5 = identity_mat()
        transformation_n_moon_5 = self.apply_moon_transformation(self.n_moon_5, transformation_n_moon_5, 0.001,
                                                                 self.neptune)
        self.n_moon_5.draw(transformation_n_moon_5)

        transformation_n_moon_6 = identity_mat()
        transformation_n_moon_6 = self.apply_moon_transformation(self.n_moon_6, transformation_n_moon_6, 0.001,
                                                                 self.neptune)
        self.n_moon_6.draw(transformation_n_moon_6)
        # neptuno y lunas__________________________________________________________

        # pluto y lunas__________________________________________________________
        transformation_pluto = identity_mat()
        self.apply_transformation(self.pluto, transformation_pluto, 0.0008)
        # pluto y lunas__________________________________________________________

        # nave__________________________________________________________
        transformation_ship = self.camera.transformation
        transformation_ship = translate(
            transformation_ship, 0.001, -0.03, -0.09
        )
        transformation_ship = rotate(transformation_ship, 180, "y", local=True)
        transformation_ship = scale(transformation_ship, 0.01, 0.01, 0.01)
        self.ship.draw(transformation_ship)


if __name__ == '__main__':
    VertexShaderCameraDemo().main_loop()
