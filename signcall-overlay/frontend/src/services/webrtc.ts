export async function getLocalStream(): Promise<MediaStream> {
  return navigator.mediaDevices.getUserMedia({ video: true, audio: false });
}
