module.exports = {
  apps : [
    {
      name: "datachecker",
      script: "./bin/www",
      interpreter_args: "--max-old-space-size=16000",
      instances: 1,
      // merge_logs: true,
      // exec_mode: "cluster",
      env: {
        // PORT: 3030,
        NODE_ENV: "production"
      },
      env_dev: {
        PORT: 8080,
        NODE_ENV: "development"
      }
    }
  ]
};
