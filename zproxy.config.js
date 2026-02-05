const path = require("path");

const apiMocker = require("mocker-api");
const webpack = require("webpack");
const HtmlWebPackPlugin = require("html-webpack-plugin");
const WebpackShellPlugin = require("webpack-shell-plugin");

const matchCss = /\.css$/;

const isDev = process.env.NODE_ENV === "development";
const standalone =
  process.env.NODE_ENV === "development" &&
  process.env.NODE_MODE === "frontend_standalone";
const plugins = [
  new HtmlWebPackPlugin({
    template: "./src/index.ejs",
    filename: "./index.html",
  }),
  // In local pc develop, we do not us nginx, we need remove the following comments. So please do not remove the follow code
  new webpack.DefinePlugin({
    __ENV__: {
      LSM_API_HOST: JSON.stringify(
        process.env.LSM_API_HOST || "http://localhost:9000"
      ),
      AUTH_API_HOST: JSON.stringify(
        process.env.AUTH_API_HOST || "http://localhost:9000"
      ),
      LSM_WEB_HOST: JSON.stringify(
        process.env.LSM_WEB_HOST || "http://localhost:9000"
      ),
      GAODE_MAP_API_KEY: JSON.stringify(
        process.env.GAODE_MAP_API_KEY || "07d566570056a6f518173c5e0e2fa0cf"
      ),
      GAODE_MAP_API_SECRET: JSON.stringify(
        process.env.GAODE_MAP_API_SECRET || ""
      ),
    },
  }),
];

console.log("!!!!! " + process.env.LSM_API_HOST);
console.log("isDev: " + isDev);

module.exports = [
  {
    context: __dirname,
    entry: "entry.tsx",
    output: {
      path: path.resolve("./dist/"),
      filename: isDev ? "LsmWeb.[hash].js" : "LsmWeb.[contenthash].js",
    },
    module: {
      rules: [
        {
          enforce: "pre",
          test: /\.(tsx?)$/,
          loader: "eslint-loader",
          exclude: /node_modules/,
        },
        {
          test: /\.(jsx?|tsx?)$/,
          exclude: /node_modules/,
          use: [
            {
              loader: "awesome-typescript-loader",
              options: {
                useCache: true,
                useBabel: true,
                babelCore: "@babel/core",
              },
            },
          ],
        },
        {
          test: /\.css$/,
          use: ["style-loader", "css-loader"],
        },
        {
          test: /\.scss$/,
          use: [
            {
              loader: "file-loader",
              options: {
                name: "bundle.css",
              },
            },
            { loader: "extract-loader" },
            { loader: "css-loader" },
            {
              loader: "sass-loader",
              options: {
                importer: (url) => {
                  if (url.indexOf("@material") === 0) {
                    const filePath = url.split("@material")[1];
                    const nodeModulePath = `./node_modules/@material/${filePath}`;
                    return { file: path.resolve(nodeModulePath) };
                  }

                  if (url.indexOf("~") === 0) {
                    const filePath = url.split("~")[1];
                    const nodeModulePath = `./node_modules/${filePath}`;
                    return {
                      file: path.resolve(nodeModulePath).replace(matchCss, ""),
                    };
                  }

                  return { file: url.replace(matchCss, "") };
                },
              },
            },
          ],
        },
        {
          test: /\.(jpe?g|png|gif|svg|eot|woff|ttf|svg|woff2)$/,
          use: [
            {
              loader: "file-loader",
              options: {
                name: "[name].[ext]",
                outputPath: "assets/",
                publicPath: "assets/",
              },
            },
          ],
        },
      ],
    },

    resolve: {
      extensions: [".ts", ".tsx", ".js", ".jsx"],
      modules: [
        path.resolve(__dirname, "src"),
        path.resolve(__dirname, "static"),
        "./node_modules",
      ],
    },

    plugins,
    devtool: "source-map",
    devServer: {
      contentBase: "./dist",
      historyApiFallback: true,
      port: 9000,
      disableHostCheck: true,
      before(app) {
        if (standalone) {
          apiMocker(app, path.resolve("mocker/index.js"));
        }
      },
      // add local to staging proxy
      proxy: {
        // 处理所有 /auth 开头的请求
        "/auth": {
          // target: 'https://live-semantic-map.srv.corp.pony.ai', // prod
          // target: 'https://staging-live-semantic-map.srv.corp.pony.ai', // staging
          target: "https://live-semantic-map-dev.k8s.gz.corp.pony.ai:30443 ", // dev
          changeOrigin: true,
          secure: false,
          cookieDomainRewrite: {
            "staging-live-semantic-map.srv.corp.pony.ai": "localhost",
            ".srv.corp.pony.ai": "localhost",
            "*": "localhost",
          },
          cookiePathRewrite: {
            "*": "/",
          },
          headers: {
            Accept: "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,zh;q=0.8",
          },
          onProxyRes(proxyRes, req, res) {
            // 处理响应中的 Set-Cookie
            if (proxyRes.headers["set-cookie"]) {
              proxyRes.headers["set-cookie"] = proxyRes.headers[
                "set-cookie"
              ].map((cookie) => {
                return cookie
                  .replace(/Domain=.*?;/gi, "Domain=localhost;")
                  .replace(/Secure;?/gi, "")
                  .replace(/SameSite=None;?/gi, "SameSite=Lax;");
              });
            }
          },
        },
        // 处理所有 /lsm 开头的请求
        "/lsm": {
          // target: 'https://live-semantic-map.srv.corp.pony.ai', // prod
          // target: 'https://staging-live-semantic-map.srv.corp.pony.ai', // staging
          target: "https://live-semantic-map-dev.k8s.gz.corp.pony.ai:30443 ", // dev
          changeOrigin: true,
          secure: false,
          cookieDomainRewrite: {
            "staging-live-semantic-map.srv.corp.pony.ai": "localhost",
            ".srv.corp.pony.ai": "localhost",
            "*": "localhost",
          },
          cookiePathRewrite: {
            "*": "/",
          },
          headers: {
            Accept: "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,zh;q=0.8",
          },
          onProxyRes(proxyRes, req, res) {
            // 处理响应中的 Set-Cookie
            if (proxyRes.headers["set-cookie"]) {
              proxyRes.headers["set-cookie"] = proxyRes.headers[
                "set-cookie"
              ].map((cookie) => {
                return cookie
                  .replace(/Domain=.*?;/gi, "Domain=localhost;")
                  .replace(/Secure;?/gi, "")
                  .replace(/SameSite=None;?/gi, "SameSite=Lax;");
              });
            }
          },
        },
      },
    },
  },
];
