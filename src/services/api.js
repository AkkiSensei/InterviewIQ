// Base API configurations and utilities for InterviewIQ

export const API_BASE_URL = 'http://localhost:8000/api'; // Reserved for future FastAPI integration

/**
 * Simulates network latency.
 * @param {number} ms - The millisecond delay duration.
 * @returns {Promise<void>}
 */
export const simulateDelay = (ms = 1000) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};
