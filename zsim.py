#!/usr/bin/env python3
from absl import app, flags
import subprocess
import os

GEOMETRY_BASED_NEIGHBOR_CALCULATION_RELATED_ISSUE_REMOTE_DIRS = [
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260109/k9011-144638-1767941609.atomic.zip',
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260102/k9043-102255-1767324907.atomic.zip',
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260107/k9043-112624-1767763796.atomic.zip',
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260102/k9042-094931-1767324699.atomic.zip',
    # https://jira.corp.pony.ai/browse/RTI-42778510
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260129/k9216-100455-1769655966.atomic.zip',
    # 长距离，latency报告中表现最差的record
    '/guangzhou/truncated_data_v2/manual/guangzhou/20250926/k8106-074958-1758847477__1758847974.atomic.zip',
]
USE_DIR_INDEX = 0

flags.DEFINE_enum(
    'mode',
    'olive',
    ['olive', 'profile'],
    'Running mode',
)

flags.DEFINE_bool(
    'build',
    False,
    'Whether to build before running binary',
)

flags.DEFINE_bool(
    'geo',
    True,
    'Whether to enable geometry-based neighbor calculation',
)

flags.DEFINE_string(
    'dir',
    f'{GEOMETRY_BASED_NEIGHBOR_CALCULATION_RELATED_ISSUE_REMOTE_DIRS[USE_DIR_INDEX]}',
    'The remote directory for record',
)

flags.DEFINE_bool(
    'upload',
    False,
    'Whether to upload flame graph onto web',
)

FLAGS = flags.FLAGS


# flags.alias_flag('g', 'enable_geometry')


def common(argv):
    os.chdir('/home/tianyulu/work/ponyai/.sub-repos')

    if FLAGS.build:
        subprocess.run(['make8', 'build', 'olive_main'], check=True)

    olive_binary_path = './make8-bin/common/tools/olive/olive_main'

    olive_args = [
        '--simple-mode=detected_map',
        f'--remote-dir={FLAGS.dir}',
        '--static_map_any_version',
        '--road_graph_any_version',
        '--simulation_data_buffer_size=512',
    ]

    subprocess.run([olive_binary_path] + olive_args, check=True)


def geometry_neighbor(argv):
    os.chdir('/home/tianyulu/work/ponyai/.sub-repos')

    if FLAGS.build:
        if FLAGS.mode == 'olive':
            subprocess.run(['make8', 'build', 'olive_main'], check=True)
        elif FLAGS.mode == 'profile':
            subprocess.run(['make8', 'build', 'simulation_main'], check=True)

    olive_binary_path = './make8-bin/common/tools/olive/olive_main'
    profiler_binary_path = './make8-bin/common/utils/profiler/profile_helper/profile_helper_cli_package'

    olive_args = [
        '--simple-mode=detected_map',
        f'--remote-dir={FLAGS.dir}',
        '--static_map_any_version',
        '--road_graph_any_version',
        '--simulation_data_buffer_size=512',
        f'--enable_geometry_based_neighbor_calculation={str(FLAGS.geo).lower()}',
    ]

    profiler_args = [
        'profile',
        '--mode=cpu',
        '--binary=./make8-bin/infrastructure/simulation/simulation_main',
        f'--cwd={os.getcwd()}',
        '--args',
        ' '.join(olive_args),
    ]

    if FLAGS.mode == 'olive':
        subprocess.run([olive_binary_path] + olive_args, check=True)
    elif FLAGS.mode == 'profile':
        subprocess.run([profiler_binary_path] + profiler_args, check=True)
        if FLAGS.upload:
            subprocess.run([profiler_binary_path, 'upload'], check=True)


def lane_confidence(argv):
    pass

if __name__ == '__main__':
    # app.run(geometry_neighbor)
    app.run(common)