import http from 'k6/http';
import { check, sleep } from 'k6';

const baseUrl = __ENV.BASE_URL || 'http://localhost:8000';
const prompt = __ENV.PROMPT || 'repeat this prompt for cache verification';

export const options = {
  scenarios: {
    cached: {
      executor: 'constant-vus',
      vus: Number(__ENV.VUS || 50),
      duration: __ENV.DURATION || '30s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<3000'],
  },
};

export default function () {
  const response = http.post(
    `${baseUrl}/generate`,
    JSON.stringify({ prompt }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(response, {
    'status is 200': (r) => r.status === 200,
    'cache header is present': (r) => Boolean(r.headers['X-Cache']),
  });

  sleep(0.1);
}
