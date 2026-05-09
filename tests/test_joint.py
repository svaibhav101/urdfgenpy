from urdfgenpy import Joint, JointDynamics, JointLimit, JointMimic


class TestJointLimit:
    def test_xml(self):
        lim = JointLimit(lower=-1.0, upper=1.0, effort=10.0, velocity=1.5)
        xml = lim.to_xml()
        assert 'lower="-1.0"' in xml
        assert 'upper="1.0"' in xml
        assert 'effort="10.0"' in xml
        assert 'velocity="1.5"' in xml


class TestJointDynamics:
    def test_xml(self):
        dyn = JointDynamics(damping=0.5, friction=0.01)
        xml = dyn.to_xml()
        assert 'damping="0.5"' in xml
        assert 'friction="0.01"' in xml


class TestJointMimic:
    def test_xml(self):
        m = JointMimic(joint="other_joint", multiplier=2.0, offset=0.1)
        xml = m.to_xml()
        assert 'joint="other_joint"' in xml
        assert 'multiplier="2.0"' in xml
        assert 'offset="0.1"' in xml


class TestJoint:
    def _make_joint(self, joint_type="revolute"):
        return Joint(
            name="test_joint",
            joint_type=joint_type,
            parent="base",
            child="arm",
        )

    def test_fixed_joint_xml(self):
        j = self._make_joint("fixed")
        xml = j.to_xml()
        assert 'type="fixed"' in xml
        assert "<axis" not in xml

    def test_revolute_has_axis(self):
        j = self._make_joint("revolute")
        xml = j.to_xml()
        assert "<axis" in xml

    def test_prismatic_has_axis(self):
        j = self._make_joint("prismatic")
        assert "<axis" in j.to_xml()

    def test_floating_no_axis(self):
        j = self._make_joint("floating")
        assert "<axis" not in j.to_xml()

    def test_with_limit(self):
        j = Joint(
            name="j", joint_type="revolute", parent="a", child="b",
            limit=JointLimit(lower=-1.0, upper=1.0, effort=5.0, velocity=1.0),
        )
        assert "<limit" in j.to_xml()

    def test_with_dynamics(self):
        j = Joint(
            name="j", joint_type="revolute", parent="a", child="b",
            dynamics=JointDynamics(damping=1.0, friction=0.1),
        )
        assert "<dynamics" in j.to_xml()

    def test_with_mimic(self):
        j = Joint(
            name="j", joint_type="revolute", parent="a", child="b",
            mimic=JointMimic(joint="other"),
        )
        assert "<mimic" in j.to_xml()

    def test_parent_child_in_xml(self):
        j = self._make_joint()
        xml = j.to_xml()
        assert 'link="base"' in xml
        assert 'link="arm"' in xml
