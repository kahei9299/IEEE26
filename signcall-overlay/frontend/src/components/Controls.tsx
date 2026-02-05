export default function Controls(props: {
  connected: boolean;
  modePref: string;
  setModePref: (v: string) => void;
  sendCorrection: () => void;
}) {
  return (
    <div className="controls">
      <div>WS: {props.connected ? "connected" : "disconnected"}</div>

      <label>
        Caption style:
        <select value={props.modePref} onChange={(e) => props.setModePref(e.target.value)}>
          <option value="concise">concise</option>
          <option value="detailed">detailed</option>
        </select>
      </label>

      <button onClick={props.sendCorrection}>Send sample correction</button>
    </div>
  );
}
