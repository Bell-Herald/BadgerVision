import { PinataSDK } from "pinata";
import { SessionDetails } from "./App";
import { PINATA_GATEWAY, PINATA_JWT } from "./secrets/pinata";
import { io } from "socket.io-client";

const getPinataClient = () => {
  return new PinataSDK({
    pinataJwt: PINATA_JWT,
    pinataGateway: PINATA_GATEWAY,
  });
};

export const getSessionDetails = async (
  sessionId: string
): Promise<SessionDetails> => {
  const pinata = getPinataClient();

  const { data } = (await pinata.gateways.get(sessionId)) as { data: string };
  return JSON.parse(data);
};

const getWebsocketClient = (serverUrl: string) => {
  return io(serverUrl);
};

export type Face = {
  id: string;
  name: string;
  url: string;
};

export const facesUpdatedListener = (
  serverUrl: string,
  listener: (faces: Face) => void
) => {
  const socket = getWebsocketClient(serverUrl);

  socket.on("faces-updated", listener);
};

export const addFace = (serverUrl: string) => {};
