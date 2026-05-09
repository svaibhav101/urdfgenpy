# --- std
import math

# --- usr
from urdfgenpy import Box, Collision, Cylinder, Inertial, Material, Origin, Sphere, Visual


class TestOrigin:
    def test_default(self):
        o = Origin()
        xml = o.to_xml()
        assert 'xyz="0.0 0.0 0.0"' in xml
        assert 'rpy="0.0 0.0 0.0"' in xml

    def test_explicit(self):
        o = Origin(xyz=(1.0, 2.0, 3.0), rpy=(0.1, 0.2, 0.3))
        xml = o.to_xml()
        assert 'xyz="1.0 2.0 3.0"' in xml
        assert 'rpy="0.1 0.2 0.3"' in xml

    def test_above_box(self):
        b = Box(0.2, 0.2, 0.1)
        o = Origin.above(b)
        assert math.isclose(o.xyz[2], 0.05)

    def test_above_cylinder(self):
        c = Cylinder(radius=0.05, length=0.2)
        o = Origin.above(c)
        assert math.isclose(o.xyz[2], 0.1)

    def test_above_sphere(self):
        s = Sphere(radius=0.3)
        o = Origin.above(s)
        assert math.isclose(o.xyz[2], 0.3)

    
    def test_wheel(self):
        o = Origin.wheel()
        assert math.isclose(o.rpy[0], -math.pi / 2.0)
        assert o.rpy[1] == 0.0
        assert o.rpy[2] == 0.0

    def test_above_xy_offset(self):
        b = Box(0.1, 0.1, 0.2)
        o = Origin.above(b, xy=(1.0, 2.0))
        assert o.xyz[0] == 1.0
        assert o.xyz[1] == 2.0


class TestMaterial:
    def test_with_rgba(self):
        m = Material("red", rgba=(1.0, 0.0, 0.0, 1.0))
        xml = m.to_xml()
        assert 'name="red"' in xml
        assert 'rgba="1.0 0.0 0.0 1.0"' in xml

    def test_with_texture(self):
        m = Material("wood", texture="wood.png")
        xml = m.to_xml()
        assert 'filename="wood.png"' in xml

    def test_name_only(self):
        m = Material("plain")
        xml = m.to_xml()
        assert '<material name="plain">' in xml


class TestVisual:
    def test_basic(self):
        b = Box(0.1, 0.1, 0.1)
        v = Visual(geometry=b)
        xml = v.to_xml()
        assert "<visual>" in xml
        assert "<geometry>" in xml
        assert "<box" in xml

    def test_with_material(self):
        b = Box(0.1, 0.1, 0.1)
        mat = Material("blue", rgba=(0, 0, 1, 1))
        v = Visual(geometry=b, material=mat)
        xml = v.to_xml()
        assert 'name="blue"' in xml

    def test_named_visual(self):
        v = Visual(geometry=Sphere(0.1), name="tip")
        assert 'name="tip"' in v.to_xml()


class TestCollision:
    def test_basic(self):
        xml = Collision(geometry=Box(1, 1, 1)).to_xml()
        assert "<collision>" in xml
        assert "<box" in xml



class TestInertial:
    def test_from_box(self):
        inert = Inertial.from_box(1.0, 0.2, 0.2, 0.1)
        assert inert.mass == 1.0
        xml = inert.to_xml()
        assert "<inertial>" in xml
        assert "<mass" in xml
        assert "<inertia" in xml

    def test_from_sphere(self):
        inert = Inertial.from_sphere(0.5, 0.1)
        assert math.isclose(inert.matrix.ixx, inert.matrix.izz)

    def test_from_cylinder(self):
        inert = Inertial.from_cylinder(1.0, 0.05, 0.2)
        assert inert.mass == 1.0

    def test_from_geometry_box(self):
        b = Box(0.1, 0.1, 0.1)
        inert = Inertial.from_geometry(1.0, b)
        assert inert.mass == 1.0

    def test_from_geometry_sphere(self):
        s = Sphere(0.1)
        inert = Inertial.from_geometry(0.5, s)
        assert math.isclose(inert.matrix.ixx, inert.matrix.iyy)

    def test_from_geometry_cylinder(self):
        c = Cylinder(0.05, 0.2)
        inert = Inertial.from_geometry(1.0, c)
        assert inert.mass == 1.0

   

