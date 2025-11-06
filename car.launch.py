
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
import os

def generate_launch_description():
    # Package share dir
    pkg_share = FindPackageShare("my_nav2_pkg").find("my_nav2_pkg")

    # URDF/Xacro
    xacro_file = os.path.join(pkg_share, "urdf", "car.xacro")

    # RViz config (make sure you create this .rviz file in config/)
    rviz_config_file = os.path.join(pkg_share, "config", "car_config.rviz")

    # Launch arguments
    declared_arguments = [
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
            description="Use simulation clock if true"
        ),
    ]
    use_sim_time = LaunchConfiguration("use_sim_time")

    # Run xacro to generate robot_description
    robot_description_content = Command([
        FindExecutable(name="xacro"),
        " ",
        xacro_file
    ])
    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    # Robot State Publisher
    rsp_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description, {"use_sim_time": use_sim_time}]
    )

    # Joint State Publisher GUI
    jsp_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        parameters=[{"use_sim_time": use_sim_time}]
    )

    # RViz2
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file]
    )

    return LaunchDescription(declared_arguments + [
        rsp_node,
        jsp_node,
        rviz_node
    ])
