import http from 'k6/http';
import { check, sleep } from 'k6';

const baseUrl = __ENV.BASE_URL || 'http://localhost:8001';

export const options = {
  scenarios: {
    baseline: {
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
  const payload = JSON.stringify({
    prompt: `baseline prompt ${__VU}-${__ITER}`,
  });

  const response = http.post(`${baseUrl}/generate`, payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(response, {
    'status is 200': (r) => r.status === 200,
    'response marks cache miss or hit': (r) => {
      const body = r.json();
      return typeof body.cached === 'boolean';
    },
  });

  sleep(0.1);
}
