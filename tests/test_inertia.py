import math

from urdfgenpy.inertia import (
    InertiaMatrix,
    box_inertia,
    cylinder_inertia,
    sphere_inertia,
)


class TestInertiaMatrix:
    def test_to_xml_contains_values(self):
        m = InertiaMatrix(ixx=1.0, ixy=0.0, ixz=0.0, iyy=2.0, iyz=0.0, izz=3.0)
        xml = m.to_xml()
        assert 'ixx="1"' in xml
        assert 'iyy="2"' in xml
        assert 'izz="3"' in xml

    def test_to_xml_zero_off_diagonal(self):
        m = InertiaMatrix(ixx=1.0, ixy=0.0, ixz=0.0, iyy=1.0, iyz=0.0, izz=1.0)
        assert 'ixy="0"' in m.to_xml()


class TestBoxInertia:
    def test_uniform_cube(self):
        # 1 kg cube, side=1 -> each diagonal = 1/6
        m = box_inertia(1.0, 1.0, 1.0, 1.0)
        expected = 1.0 / 6.0
        assert math.isclose(m.ixx, expected, rel_tol=1e-9)
        assert math.isclose(m.iyy, expected, rel_tol=1e-9)
        assert math.isclose(m.izz, expected, rel_tol=1e-9)
        assert m.ixy == 0.0

    def test_non_cube_axis_correctness(self):
        # l=2(x), w=1(y), h=0.5(z), mass=1
        # ixx = (1/12)*(w^2+h^2) = (1+0.25)/12
        # iyy = (1/12)*(l^2+h^2) = (4+0.25)/12
        # izz = (1/12)*(l^2+w^2) = (4+1)/12
        m = box_inertia(1.0, 2.0, 1.0, 0.5)
        assert math.isclose(m.ixx, (1.0 + 0.25) / 12.0, rel_tol=1e-9)
        assert math.isclose(m.iyy, (4.0 + 0.25) / 12.0, rel_tol=1e-9)
        assert math.isclose(m.izz, (4.0 + 1.0) / 12.0, rel_tol=1e-9)

    def test_ixx_depends_on_yw_not_x(self):
        # Changing l (x-dimension) must NOT change ixx.
        m1 = box_inertia(1.0, 1.0, 1.0, 1.0)
        m2 = box_inertia(1.0, 5.0, 1.0, 1.0)
        assert math.isclose(m1.ixx, m2.ixx)

    def test_multiply(self):
        m1 = box_inertia(1.0, 1.0, 1.0, 1.0, inertia_multiply=1.0)
        m2 = box_inertia(1.0, 1.0, 1.0, 1.0, inertia_multiply=2.0)
        assert math.isclose(m2.ixx, 2 * m1.ixx)


class TestSphereInertia:
    def test_formula(self):
        # I = 2/5 * m * r^2
        m = sphere_inertia(2.0, 0.5)
        expected = (2.0 / 5.0) * 2.0 * 0.5**2
        assert math.isclose(m.ixx, expected)
        assert math.isclose(m.iyy, expected)
        assert math.isclose(m.izz, expected)

    def test_off_diagonal_zero(self):
        m = sphere_inertia(1.0, 1.0)
        assert m.ixy == 0.0 and m.ixz == 0.0 and m.iyz == 0.0


class TestCylinderInertia:
    def test_symmetry_ixx_iyy(self):
        m = cylinder_inertia(1.0, 0.1, 0.5)
        assert math.isclose(m.ixx, m.iyy)

    def test_izz_formula(self):
        # izz = 0.5 * m * r^2
        m = cylinder_inertia(2.0, 0.3, 1.0)
        expected_izz = 0.5 * 2.0 * 0.3**2
        assert math.isclose(m.izz, expected_izz)
