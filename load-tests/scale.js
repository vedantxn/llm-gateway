import http from 'k6/http';
import { check, sleep } from 'k6';

const baseUrl = __ENV.BASE_URL || 'http://localhost:8000';

export const options = {
  scenarios: {
    scale_out: {
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
    prompt: `scaled prompt ${__VU}-${__ITER}`,
  });

  const response = http.post(`${baseUrl}/generate`, payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(response, {
    'status is 200': (r) => r.status === 200,
    'response marks cache miss or hit': (r) => typeof r.json().cached === 'boolean',
    'served by instance': (r) => Boolean(r.headers['X-Served-By']),
  });

  sleep(0.1);
}
