#!/usr/bin/zsh

set -e

MODE="no_build"
if [ -n "$1" ]; then
  MODE=$1
fi

#shisho render ./common/config/latency_evaluation/nansha/detected_map/


#DATA=/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260109/k9011-144638-1767941609.atomic.zip
#DATA=/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260102/k9043-102255-1767324907.atomic.zip
#DATA=/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260107/k9043-112624-1767763796.atomic.zip
#DATA=/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260102/k9042-094931-1767324699.atomic.zip
#DATA=/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260129/k9216-100455-1769655966.atomic.zip # https://jira.corp.pony.ai/browse/RTI-42778510
#DATA=/guangzhou/truncated_data_v2/manual/guangzhou/20250926/k8106-074958-1758847477__1758847974.atomic.zip # 长距离

if [ -n "$2" ]; then
  DATA=$2
fi
#
#
#if [ "$MODE" = "build" ]; then
#  make8 build olive_main
#fi
#
#
#./make8-bin/common/tools/olive/olive_main \
#  --simple-mode detected_map \
#  --remote-dir "$DATA" \
#  --static_map_any_version \
#  --road_graph_any_version \
#  --simulation_data_buffer_size=512 \
#  --enable_geometry_based_neighbor_calculation=false \
#   > test_geometry.log 2>&1


#./make8-bin/common/tools/olive/olive_main \
#  --simple-mode detected_map \
#  --remote-dir $DATA \
#  --static_map_any_version \
#  --road_graph_any_version \
#  --simulation_data_buffer_size=256 \
#  --storage_site=daxing \
#  --enable_get_lane_type_from_model \
#  --enable_geometry_based_neighbor_calculation=false \
#  > test_no_geometry.log 2>&1


if [ "$MODE" = "build" ]; then
  make8 build simulation_main
fi

#./make8-bin/infrastructure/simulation/simulation_main \
#  --simple-mode detected_map \
#  --remote-dir "$DATA" \
#  --static_map_any_version \
#  --road_graph_any_version


./make8-bin/common/utils/profiler/profile_helper/profile_helper_cli_package profile \
  --mode=cpu \
  --binary="$PWD/make8-bin/infrastructure/simulation/simulation_main" \
  --cwd="$PWD" \
  --args="--simple-mode detected_map \
        --remote-dir $DATA \
        --static_map_any_version \
        --road_graph_any_version"

#./make8-bin/common/utils/profiler/profile_helper/profile_helper_cli_package upload