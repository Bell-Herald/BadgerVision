import { PinataSDK } from "pinata";
import { SessionDetails } from "../../zoom-video-sdk/App";
import { PINATA_GATEWAY, PINATA_JWT } from "./secrets/pinata";

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
