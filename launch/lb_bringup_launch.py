# lb_bringup_launch.py

import launch
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    package_dir = get_package_share_directory('lb_bringup')

    lb_control_launch_file = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('lb_control')
                             ,'launch/lb_control_launch.py')
            )
    )

    teleop_twist_joy_launch_file = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('teleop_twist_joy')
                             ,'launch/teleop-launch.py')
            ),
            launch_arguments = {
                'publish_stamped_twist': 'True',
                'joy_vel': '/lb_base_controller/cmd_vel',
                'joy_config': 'f710'
            }.items(),
    )

    ros_realsense2_launch_file = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                  os.path.join(get_package_share_directory('realsense2_camera')
                               ,'launch/rs_launch.py')
            ),
    )


    LD = LaunchDescription([
        Node(
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent_serial',
            output='screen',
            arguments=['serial', '--dev', '/dev/ttyACM0'],
        )
    ])

    LD.add_action(lb_control_launch_file)
    LD.add_action(teleop_twist_joy_launch_file)
    LD.add_action(ros_realsense2_launch_file)

    return LD