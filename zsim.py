#!/usr/bin/env python3
from absl import app, flags
from typing import List, Dict
import subprocess
import os

GEOMETRY_BASED_NEIGHBOR_CALCULATION_RELATED_ISSUE_REMOTE_DIRS: List[str] = [
    # https://jira.corp.pony.ai/browse/RTI-41772295
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260107/k9043-112624-1767763796.atomic.zip',
    # https://jira.corp.pony.ai/browse/RTI-41565329
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260102/k9043-102255-1767324907.atomic.zip',
    # https://jira.corp.pony.ai/browse/RTI-41861988
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260109/k9011-144638-1767941609.atomic.zip',
    # https://jira.corp.pony.ai/browse/RTI-41564778
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260102/k9042-094931-1767324699.atomic.zip',
    # https://jira.corp.pony.ai/browse/RTI-42778510
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260129/k9216-100455-1769655966.atomic.zip',
    # jenkins latency-diff 20251103_k8101_192331_1762169901__1762170588-traffic-flow
    '/guangzhou/truncated_data_v2/manual/guangzhou/20250926/k8106-074958-1758847477__1758847974.atomic.zip',
]

LANE_CONFIDENCE_RELATED_ISSUE_REMOTE_DIRS: List[str] = [
    # https://jira.corp.pony.ai/browse/RTI-41364507
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20251228/p7050-084545-1766897859.atomic.zip',
    # https://jira.corp.pony.ai/browse/RTI-40669561
    '/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20251214/p7052-093153-1765683083.atomic.zip',
]

ISSUE_REMOTE_DIRS: Dict[str, List[str]] = {
    'common': GEOMETRY_BASED_NEIGHBOR_CALCULATION_RELATED_ISSUE_REMOTE_DIRS,
    'geometry_neighbor': GEOMETRY_BASED_NEIGHBOR_CALCULATION_RELATED_ISSUE_REMOTE_DIRS,
    'lane_confidence': LANE_CONFIDENCE_RELATED_ISSUE_REMOTE_DIRS
}

FLAGS = flags.FLAGS

TARGETS = {
    'olive': 'olive_main',
    'simulation': 'simulation_main',
    'geometry_neighbor_test': 'multi_frame_lane_info_generator_unit_test',
}

BINARY_PATHS = {
    'olive': './make8-bin/common/tools/olive/olive_main',
    'simulation': './make8-bin/infrastructure/simulation/simulation_main',
    'profile': './make8-bin/common/utils/profiler/profile_helper/profile_helper_cli_package',
    'geometry_neighbor_test': './make8-bin/map/pom/detected_map/online_map/multi_frame_lane_info_generator_unit_test',
}


def define_flags():
    flags.DEFINE_bool(
        'build',
        False,
        'Whether to build before running binary',
    )

    flags.DEFINE_enum(
        'mode',
        'olive',
        ['olive', 'profile'],
        'Running mode',
    )

    flags.DEFINE_bool(
        'geo',
        True,
        'Whether to enable geometry-based neighbor calculation',
    )

    flags.DEFINE_string(
        'dir',
        '',
        'The remote directory for record',
    )

    flags.DEFINE_bool(
        'upload',
        False,
        'Whether to upload CPU flame graph onto web',
    )

    flags.DEFINE_integer(
        'buffer_size',
        256,
        'The size of simulation buffer',
    )

    flags.DEFINE_integer(
        'index',
        0,
        'The index of the remote directory in the List that should be used',
    )


def common(argv):
    if len(FLAGS.dir) == 0:
        FLAGS.dir = ISSUE_REMOTE_DIRS['common'][FLAGS.index]

    olive_target = 'olive_main'
    if FLAGS.build:
        subprocess.run(['make8', 'build', olive_target], check=True)

    olive_args = [
        '--simple-mode=detected_map',
        f'--remote-dir={FLAGS.dir}',
        '--static_map_any_version',
        '--road_graph_any_version',
        f'--simulation_data_buffer_size={FLAGS.buffer_size}',
    ]

    subprocess.run([BINARY_PATHS['olive']] + olive_args, check=True)


def geometry_neighbor(argv):
    if len(FLAGS.dir) == 0:
        FLAGS.dir = ISSUE_REMOTE_DIRS['geometry_neighbor'][FLAGS.index]

    if FLAGS.build:
        if FLAGS.mode == 'olive':
            subprocess.run(['make8', 'build', TARGETS['olive']], check=True)
        elif FLAGS.mode == 'profile':
            subprocess.run(['make8', 'build', TARGETS['simulation']], check=True)

    olive_args = [
        '--simple-mode=detected_map',
        f'--remote-dir={FLAGS.dir}',
        '--static_map_any_version',
        '--road_graph_any_version',
        f'--simulation_data_buffer_size={FLAGS.buffer_size}',
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
        subprocess.run([BINARY_PATHS['olive']] + olive_args, check=True)
    elif FLAGS.mode == 'profile':
        subprocess.run([BINARY_PATHS['profile']] + profiler_args, check=True)
        if FLAGS.upload:
            subprocess.run([BINARY_PATHS['profile'], 'upload'], check=True)


def geometry_neighbor_test(argv):
    if FLAGS.build:
        subprocess.run(['make8', 'build', TARGETS['geometry_neighbor_test']], check=True)
    subprocess.run(BINARY_PATHS['geometry_neighbor_test'], check=True)


def lane_confidence(argv):
    if len(FLAGS.dir) == 0:
        FLAGS.dir = ISSUE_REMOTE_DIRS['lane_confidence'][FLAGS.index]
    pass


if __name__ == '__main__':
    os.chdir('/home/tianyulu/work/ponyai/.sub-repos')
    define_flags()

    # app.run(common)
    # app.run(geometry_neighbor)
    # app.run(geometry_neighbor_test)
    app.run(lane_confidence)
