"""Smoke tests for package-level attributes and PEP 561 compliance."""


def test_public_api_exports():
    from urdfgenpy import (
        Box,
        Collision,
        Cylinder,
        Inertial,
        InertiaMatrix,
        Joint,
        JointDynamics,
        JointLimit,
        JointMimic,
        Link,
        Material,
        Origin,
        Robot,
        Sphere,
        URDFExporter,
        Visual,
        XacroExporter,
        box_inertia,
        cylinder_inertia,
        sphere_inertia,
    )

    assert all(
        x is not None
        for x in [
            Robot,
            Link,
            Joint,
            JointLimit,
            JointDynamics,
            JointMimic,
            Box,
            Cylinder,
            Sphere,
            Origin,
            Material,
            Visual,
            Collision,
            Inertial,
            InertiaMatrix,
            box_inertia,
            sphere_inertia,
            cylinder_inertia,
            URDFExporter,
            XacroExporter,
        ]
    )
