export default function CaptionOverlay(props: { caption: string; confidence: number; mode: string }) {
  const { caption, confidence, mode } = props;
  return (
    <div className="overlay">
      <span>{caption || "—"}</span>
      <span className="badge">{Math.round(confidence * 100)}%</span>
      <span className="badge">{mode}</span>
    </div>
  );
}
