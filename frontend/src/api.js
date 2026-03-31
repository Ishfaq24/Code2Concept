const BASE_URL = "http://127.0.0.1:8000";

export const generateVideo = async (topic) => {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ topic }),
  });

  return res.json();
};

export const getVideoUrl = () => {
  return `${BASE_URL}/video`;
};