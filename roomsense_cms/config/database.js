module.exports = ({ env }) => ({
  connection: {
    client: 'mysql',
    connection: {
      host: env('DATABASE_HOST', 'dbhost'),
      port: env.int('DATABASE_PORT', 3036),
      database: env('DATABASE_NAME', 'dbname'),
      user: env('DATABASE_USERNAME', 'username'),
      password: env('DATABASE_PASSWORD', 'password'),
      ssl: env.bool('DATABASE_SSL', false),
    },
  },
});
