import { io } from "socket.io-client";

const getWebsocketClient = (serverUrl: string) => {
  return io(serverUrl);
};

export const playToneListener = (
  serverUrl: string,
  listener: (res: { sid: string; face_encoding: number[] }) => void
) => {
  const socket = getWebsocketClient(serverUrl);

  socket.on("play_tone", listener);

  return () => socket.removeListener("play_tone");
};

export const playNameListener = (
  serverUrl: string,
  listener: (res: { sid: string; name: string }) => void
) => {
  const socket = getWebsocketClient(serverUrl);

  socket.on("play_name", listener);

  return () => socket.removeListener("play_tone");
};

export const playEmotionListener = (
  serverUrl: string,
  listener: (res: { sid: string; emotion: string }) => void
) => {
  const socket = getWebsocketClient(serverUrl);

  socket.on("play_emotion", listener);

  return () => socket.removeListener("play_tone");
};
