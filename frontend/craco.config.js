module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      // Change the hash algorithm to SHA-256
      webpackConfig.output.hashFunction = 'sha256';
      return webpackConfig;
    },
  },
};