from urdfgenpy import Box, Collision, Cylinder, Inertial, Link, Visual


def make_link(name="link1"):
    b = Box(0.1, 0.1, 0.1)
    link = Link(name)
    link.add_visual(Visual(geometry=b))
    link.add_collision(Collision(geometry=b))
    link.set_inertial(Inertial.from_box(1.0, 0.1, 0.1, 0.1))
    return link


class TestLink:
    def test_empty_link_xml(self):
        xml = Link("empty").to_xml()
        assert '<link name="empty">' in xml
        assert "</link>" in xml

    def test_has_visual(self):
        xml = make_link().to_xml()
        assert "<visual>" in xml

    def test_has_collision(self):
        xml = make_link().to_xml()
        assert "<collision>" in xml

    def test_has_inertial(self):
        xml = make_link().to_xml()
        assert "<inertial>" in xml

    def test_multiple_visuals(self):
        link = Link("multi")
        link.add_visual(Visual(geometry=Box(0.1, 0.1, 0.1)))
        link.add_visual(Visual(geometry=Cylinder(0.05, 0.1)))
        assert link.to_xml().count("<visual>") == 2

    def test_chaining(self):
        b = Box(0.1, 0.1, 0.1)
        link = Link("chain").add_visual(Visual(geometry=b)).add_collision(Collision(geometry=b))
        assert len(link.visuals) == 1
        assert len(link.collisions) == 1
