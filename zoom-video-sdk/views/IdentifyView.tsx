import {
  EventType,
  useZoom,
  ZoomVideoSdkProvider,
  ZoomVideoSdkUser,
} from "@zoom/react-native-videosdk";
import { EmitterSubscription, View } from "react-native";
import { Text } from "react-native-paper";
import { RootStackParamList } from "../App";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { useEffect, useRef, useState } from "react";

type CallViewProps = {
  zoomSessionName: string;
  zoomJwt: string;
};

const CallView = ({ zoomSessionName, zoomJwt }: CallViewProps) => {
  const zoom = useZoom();
  const listeners = useRef<EmitterSubscription[]>([]);
  const [isInSession, setIsInSession] = useState(false);

  useEffect(() => {
    const connect = async () => {
      const sessionJoin = zoom.addListener(
        EventType.onSessionJoin,
        async () => {
          setIsInSession(true);
        }
      );
      listeners.current.push(sessionJoin);

      await zoom.joinSession({
        sessionName: zoomSessionName,
        token: zoomJwt,
        userName: "Client",
        audioOptions: {
          connect: true,
          mute: true,
          autoAdjustSpeakerVolume: false,
        },
        videoOptions: { localVideoOn: true },
        sessionIdleTimeoutMins: 30,
      });
    };
    connect();

    return () => {
      zoom.leaveSession();
      setIsInSession(false);
    };
  }, [zoomJwt]);

  return <Text>Connected?: {isInSession ? "true" : "false"}</Text>;
};

const IdentifyView = ({
  route,
}: NativeStackScreenProps<RootStackParamList, "Identify People">) => {
  const { zoomSessionName, zoomJwt } = route.params;

  return (
    <View>
      <Text>Identify View</Text>

      <ZoomVideoSdkProvider config={{ domain: "zoom.us", enableLog: true }}>
        <CallView zoomSessionName={zoomSessionName} zoomJwt={zoomJwt} />
      </ZoomVideoSdkProvider>
    </View>
  );
};

export default IdentifyView;
