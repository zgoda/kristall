/* eslint-disable no-unused-vars */
export default (config, env, helpers) => {
  let { rule } = helpers.getLoadersByName(config, 'babel-loader')[0];
  let babelConfig = rule.options;
  babelConfig.plugins.push(require.resolve('@babel/plugin-transform-react-jsx-source'));

  if (config.devServer) {
    const target = 'http://127.0.0.1:5000';
    config.devServer.proxy = [
      {
        path: '/api/**',
        target,
        changeOrigin: true,
        changeHost: true,
        pathRewrite: function pathRewrite(path, _request) {
          const newPath = path.replace(/^\/[^/]+\//, '');
          return `/${newPath}`;
        },
        onProxyReq: (proxyReq) => {
          if (proxyReq.getHeader('origin')) {
            proxyReq.setHeader('origin', target);
          }
        }
      },
    ];
  }
};
