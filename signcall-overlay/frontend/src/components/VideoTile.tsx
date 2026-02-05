import { useEffect, useRef } from "react";
import CaptionOverlay from "./CaptionOverlay";

export default function VideoTile(props: {
  title: string;
  stream: MediaStream | null;
  caption: string;
  confidence: number;
  mode: string;
  videoRef?: React.RefObject<HTMLVideoElement>;
}) {
  const internalRef = useRef<HTMLVideoElement>(null);
  const ref = props.videoRef ?? internalRef;

  useEffect(() => {
    if (ref.current && props.stream) {
      ref.current.srcObject = props.stream;
      ref.current.play().catch(() => {});
    }
  }, [props.stream]);

  return (
    <div>
      <div style={{ marginBottom: 6 }}>{props.title}</div>
      <div className="tile">
        <video className="video" ref={ref} muted playsInline />
        <CaptionOverlay caption={props.caption} confidence={props.confidence} mode={props.mode} />
      </div>
    </div>
  );
}
