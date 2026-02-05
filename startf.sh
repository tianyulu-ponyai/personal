cp zproxy.config.js common/webapps/live_semantic_map/web/webpack.config.js
(sleep 10 && cp zorigin.config.js common/webapps/live_semantic_map/web/webpack.config.js) &

cd common/webapps/live_semantic_map/web
export NODE_OPTIONS=--max-old-space-size=8192
npm run start
cd -
