import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'gazebo_tutorial'  # (package name)
    pkg_share = get_package_share_directory(package_name)

    # Turn the xacro file into plain URDF text
    xacro_file = os.path.join(pkg_share, 'urdf', 'teslabot.urdf.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    # 1. Launch Gazebo (reuses gazebo_ros's own launch file)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        )
    )

    # 2. Robot State Publisher: publishes the robot model and link positions
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

    # 3. Spawn the robot into Gazebo, using the model published on /robot_description
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'teslabot'],
        output='screen',
    )

    # 4. Joint State Broadcaster: publishes the joints' current positions
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
    )

    # 5. Joint Trajectory Controller: receives target trajectories and moves the joints
    joint_trajectory_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller'],
        output='screen',
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        # Start the controllers only after the robot exists, one after another
        RegisterEventHandler(OnProcessExit(target_action=spawn_robot, on_exit=[joint_state_broadcaster])),
        RegisterEventHandler(OnProcessExit(target_action=joint_state_broadcaster, on_exit=[joint_trajectory_controller])),
    ])