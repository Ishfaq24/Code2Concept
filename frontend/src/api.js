const BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  "https://code2concept-backend-ecf2.onrender.com"
).replace(/\/+$/, "");

const apiRequest = async (endpoint, options = {}) => {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      data?.message ||
      `Request failed with status ${response.status}`
    );
  }

  return data;
};

export const generateVideo = async (
  topic,
  language = "en",
  generatePdf = false
) => {
  return apiRequest("/generate", {
    method: "POST",
    body: JSON.stringify({
      topic,
      language,
      generate_pdf: generatePdf,
    }),
  });
};

export const getVideoUrl = (videoToken) => {
  const params = new URLSearchParams();

  if (videoToken) {
    params.set("token", videoToken);
  }

  return `${BASE_URL}/video${params.toString() ? `?${params}` : ""}`;
};

export const getPdfUrl = (pdfToken) => {
  const params = new URLSearchParams();

  if (pdfToken) {
    params.set("token", pdfToken);
  }

  return `${BASE_URL}/pdf${params.toString() ? `?${params}` : ""}`;
};

export const regeneratePdf = async (videoToken) => {
  const params = new URLSearchParams();

  if (videoToken) {
    params.set("token", videoToken);
  }

  return apiRequest(
    `/regenerate-pdf${params.toString() ? `?${params}` : ""}`,
    {
      method: "POST",
    }
  );
};
