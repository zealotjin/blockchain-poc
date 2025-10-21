const webpack = require("webpack");

module.exports = function override(config) {
  const fallback = config.resolve.fallback || {};
  Object.assign(fallback, {
    fs: false,
    path: require.resolve("path-browserify"),
    os: require.resolve("os-browserify/browser"),
    crypto: require.resolve("crypto-browserify"),
    stream: require.resolve("stream-browserify"),
    vm: require.resolve("vm-browserify"),
    buffer: require.resolve("buffer"),
    process: require.resolve("process/browser.js"),
    http: require.resolve("stream-http"),
    https: require.resolve("https-browserify"),
    url: require.resolve("url/"),
    assert: require.resolve("assert/")
  });

  config.resolve.fallback = fallback;

  // Add aliases for module resolution
  config.resolve.alias = {
    ...config.resolve.alias,
    "process/browser": require.resolve("process/browser.js"),
    "openapi-fetch": require.resolve("openapi-fetch/dist/index.mjs"),
  };

  // Configure module rules to handle ESM modules properly
  config.module.rules.push({
    test: /\.m?js$/,
    resolve: {
      fullySpecified: false, // disable the behaviour
    },
  });

  config.plugins = (config.plugins || []).concat([
    new webpack.ProvidePlugin({
      process: "process/browser.js",
      Buffer: ["buffer", "Buffer"],
    }),
  ]);

  // Ignore warnings about missing modules that are intentionally excluded
  config.ignoreWarnings = [
    /Failed to parse source map/,
    /Module not found: Error: Can't resolve '@react-native-async-storage/,
    /Connection interrupted while trying to subscribe/,
  ];

  return config;
};