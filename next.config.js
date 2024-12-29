/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    allowMiddlewareResponseBody: true,
  },
  async redirects() {
    return [
      {
        source: '/:path*',
        has: [
          {
            type: 'method',
            value: 'OPTIONS',
          },
        ],
        permanent: false,
        destination: 'https://amiapi.faneagain.ru/:path*',
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Accept, Origin' },
          { key: 'Access-Control-Max-Age', value: '86400' },
        ],
      },
    ];
  },
  async rewrites() {
    return {
      fallback: [
        {
          source: '/api/:path*',
          destination: `https://amiapi.faneagain.ru/:path*`,
        },
      ],
    };
  },
};

module.exports = nextConfig; 