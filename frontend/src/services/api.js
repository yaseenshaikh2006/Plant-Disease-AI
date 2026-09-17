/**
 * API Service Client for Plant Disease AI Backend
 */

const API_BASE_URL =
  import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

/**
 * Sends leaf image to backend /api/predict endpoint
 * @param {File} imageFile
 * @param {string|null} cropHint
 * @returns {Promise<Object>}
 */
export async function predictDisease(imageFile, cropHint = null) {
  if (!imageFile) {
    throw new Error('Please select a leaf image.');
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  if (cropHint && cropHint !== 'auto') {
    formData.append('crop', cropHint);
  }

  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: 'POST',
    body: formData,
  });

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error('Invalid response received from backend.');
  }

  if (!response.ok) {
    throw new Error(data.detail || 'Prediction request failed.');
  }

  return data;
}

/**
 * Fetches operational status from /api/health
 */
export async function getHealthStatus() {
  const response = await fetch(`${API_BASE_URL}/api/health`);

  if (!response.ok) {
    throw new Error('Health check failed.');
  }

  return response.json();
}

/**
 * Fetches supported crop taxonomy from /api/crops
 */
export async function getSupportedCrops() {
  const response = await fetch(`${API_BASE_URL}/api/crops`);

  if (!response.ok) {
    throw new Error('Failed to fetch crops.');
  }

  return response.json();
}

/**
 * Fetches disease encyclopedia from /api/diseases
 */
export async function getDiseaseCatalog() {
  const response = await fetch(`${API_BASE_URL}/api/diseases`);

  if (!response.ok) {
    throw new Error('Failed to fetch disease catalog.');
  }

  return response.json();
}

/**
 * Fetches actual academic evaluation results from /api/evaluation
 */
export async function getEvaluationMetrics() {
  const response = await fetch(`${API_BASE_URL}/api/evaluation`);

  if (!response.ok) {
    throw new Error('Failed to fetch evaluation metrics.');
  }

  return response.json();
}