#!/usr/bin/env python3

from urdfgenpy import Box, Cylinder, Sphere


class TestBox:
    def test_xml(self):
        b = Box(1.0, 2.0, 3.0)
        assert b.to_xml() == '<box size="1.0 2.0 3.0"/>'

    def test_shape(self):
        assert Box(1, 1, 1).shape == "box"


class TestCylinder:
    def test_xml(self):
        c = Cylinder(radius=0.5, length=1.0)
        assert 'radius="0.5"' in c.to_xml()
        assert 'length="1.0"' in c.to_xml()

    def test_shape(self):
        assert Cylinder(0.1, 0.2).shape == "cylinder"


class TestSphere:
    def test_xml(self):
        s = Sphere(radius=0.25)
        assert s.to_xml() == '<sphere radius="0.25"/>'

    def test_shape(self):
        assert Sphere(1.0).shape == "sphere"
