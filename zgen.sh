#!/bin/bash

DATA="/daxing/sensitive_data/truncated_data_v2/issue_bot/disengagement/20260116/p7019-091253-1768537551.atomic.zip"

if [ -n "$1" ]; then
  DATA="$1"
fi

./make8-bin/infrastructure/simulation/visualization_main \
    --simple_mode detected_map_test_lsm \
    --always_trigger_upload=true \
    --enable_cloud_map_v2 \
    --enable_upload_live_local_map=true \
    --enable_upload_live_local_map_in_simulation=true \
    --force_init_map_env_lsm_client_in_offline_usage=true \
    --lsm_use_async_request=false \
    --remote_dir $DATA \
    --live_semantic_map_host=https://live-semantic-map-dev.k8s.gz.corp.pony.ai:30443 \
    --use_lsm_prod_env_for_map_online_update=false \
    --static_map_any_version \
    --road_graph_any_version \
    --storage_site guangzhou \

