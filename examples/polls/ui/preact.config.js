export default (config, env, helpers) => {

  if (config.devServer) {
    config.devServer.proxy = [
      {
        path: "/api/**",
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
        changeHost: true,
        pathRewrite: function(path, request) {
          return '/' + path.replace(/^\/[^\/]+\//, '');
        }
      }
    ];
  }

};
