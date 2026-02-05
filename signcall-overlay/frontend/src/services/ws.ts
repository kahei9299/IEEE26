import type { WsIn, WsOut } from "../types/messages";

export type WsHandlers = {
  onMessage: (msg: WsIn) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (e: Event) => void;
};

export function createWs(url: string, handlers: WsHandlers) {
  const ws = new WebSocket(url);

  ws.onopen = () => handlers.onOpen?.();
  ws.onclose = () => handlers.onClose?.();
  ws.onerror = (e) => handlers.onError?.(e);
  ws.onmessage = (ev) => {
    try {
      const msg = JSON.parse(ev.data) as WsIn;
      handlers.onMessage(msg);
    } catch {
      // ignore
    }
  };

  const send = (data: WsOut) => {
    if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(data));
  };

  return { ws, send };
}
