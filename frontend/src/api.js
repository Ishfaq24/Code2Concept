const BASE_URL = "http://127.0.0.1:8000";

export const generateVideo = async (topic, language = "en", generatePdf = false) => {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ topic, language, generate_pdf: generatePdf }),
  });

  return res.json();
};

export const getVideoUrl = (videoToken) => {
  const params = new URLSearchParams();
  if (videoToken) {
    params.set("token", videoToken);
  }

  const query = params.toString();
  return `${BASE_URL}/video${query ? `?${query}` : ""}`;
};

export const getPdfUrl = (pdfToken) => {
  const params = new URLSearchParams();
  if (pdfToken) {
    params.set("token", pdfToken);
  }

  const query = params.toString();
  return `${BASE_URL}/pdf${query ? `?${query}` : ""}`;
};

export const regeneratePdf = async (videoToken) => {
  const params = new URLSearchParams();
  if (videoToken) {
    params.set("token", videoToken);
  }

  const query = params.toString();
  const res = await fetch(`${BASE_URL}/regenerate-pdf${query ? `?${query}` : ""}`, {
    method: "POST",
  });

  return res.json();
};