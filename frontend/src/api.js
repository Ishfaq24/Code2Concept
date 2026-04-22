const BASE_URL = "http://127.0.0.1:8000";

export const generateVideo = async (topic, language = "en") => {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ topic, language }),
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