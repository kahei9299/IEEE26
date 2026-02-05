export async function captureJpegBase64(videoEl: HTMLVideoElement): Promise<string> {
  const canvas = document.createElement("canvas");
  canvas.width = videoEl.videoWidth || 640;
  canvas.height = videoEl.videoHeight || 360;
  const ctx = canvas.getContext("2d");
  if (!ctx) return "";
  ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL("image/jpeg", 0.7);
  return dataUrl.split(",")[1] || "";
}
