import pytest

from urdfgenpy import Joint, Link, Material, Robot


def _make_robot():
    """Minimal two-link robot for use in tests."""
    robot = Robot("test_bot")

    base = Link("base_link")
    arm = Link("arm_link")
    robot.add_link(base)
    robot.add_link(arm)

    joint = Joint(name="base_arm", joint_type="revolute", parent="base_link", child="arm_link")
    robot.add_joint(joint)
    return robot


class TestRobotBuilding:
    def test_add_link(self):
        r = Robot("r")
        r.add_link(Link("a"))
        assert len(r.links) == 1

    def test_add_duplicate_link_raises(self):
        r = Robot("r")
        r.add_link(Link("a"))
        with pytest.raises(ValueError, match="already exists"):
            r.add_link(Link("a"))

    def test_add_joint_missing_parent_raises(self):
        r = Robot("r")
        r.add_link(Link("child"))
        with pytest.raises(ValueError, match="Parent link"):
            r.add_joint(Joint("j", "fixed", parent="missing", child="child"))

    def test_add_joint_missing_child_raises(self):
        r = Robot("r")
        r.add_link(Link("parent"))
        with pytest.raises(ValueError, match="Child link"):
            r.add_joint(Joint("j", "fixed", parent="parent", child="missing"))

    def test_add_duplicate_joint_raises(self):
        r = _make_robot()
        with pytest.raises(ValueError, match="already exists"):
            r.add_joint(Joint("base_arm", "fixed", parent="base_link", child="arm_link"))

    def test_get_link(self):
        r = _make_robot()
        assert r.get_link("base_link").name == "base_link"

    def test_get_link_missing_raises(self):
        r = _make_robot()
        with pytest.raises(KeyError):
            r.get_link("no_such_link")

    def test_get_joint(self):
        r = _make_robot()
        assert r.get_joint("base_arm").joint_type == "revolute"

    def test_get_joint_missing_raises(self):
        r = _make_robot()
        with pytest.raises(KeyError):
            r.get_joint("no_such")

    def test_add_material(self):
        r = Robot("r")
        r.add_material(Material("blue", rgba=(0, 0, 1, 1)))
        assert len(r.materials) == 1


class TestURDFExport:
    def test_header(self):
        xml = _make_robot().to_urdf()
        assert '<?xml version="1.0"?>' in xml

    def test_robot_name(self):
        xml = _make_robot().to_urdf()
        assert 'name="test_bot"' in xml

    def test_contains_links(self):
        xml = _make_robot().to_urdf()
        assert 'name="base_link"' in xml
        assert 'name="arm_link"' in xml

    def test_contains_joint(self):
        xml = _make_robot().to_urdf()
        assert 'name="base_arm"' in xml

    def test_write_file(self, tmp_path):
        out = tmp_path / "robot.urdf"
        _make_robot().to_urdf(str(out))
        assert out.exists()
        content = out.read_text()
        assert "<robot" in content

    def test_save_urdf(self, tmp_path):
        out = tmp_path / "robot.urdf"
        _make_robot().save(str(out))
        assert "<?xml" in out.read_text()


class TestXacroExport:
    def test_xacro_header(self):
        xml = _make_robot().to_xacro()
        assert "xacro" in xml.lower()

    def test_write_file(self, tmp_path):
        out = tmp_path / "robot.xacro"
        _make_robot().to_xacro(str(out))
        assert out.exists()

    def test_save_xacro(self, tmp_path):
        out = tmp_path / "robot.xacro"
        _make_robot().save(str(out))
        assert out.exists()


class TestTreeString:
    def test_tree_contains_robot_name(self):
        tree = _make_robot().tree_string()
        assert "test_bot" in tree

    def test_tree_contains_links(self):
        tree = _make_robot().tree_string()
        assert "base_link" in tree
        assert "arm_link" in tree

    def test_tree_contains_joint(self):
        tree = _make_robot().tree_string()
        assert "base_arm" in tree

    def test_save_tree(self, tmp_path):
        out = tmp_path / "tree.txt"
        _make_robot().save_tree(str(out))
        assert "test_bot" in out.read_text()
