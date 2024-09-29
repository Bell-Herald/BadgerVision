import { Button, Center, Stack, Text } from "@mantine/core";
import VideoCall from "./VideoCall";
import { StringParam, useQueryParam } from "use-query-params";
// import { playToneListener } from "./server";
import { useEffect, useState } from "react";
import { generateReducedJingle } from "./util/toneGenerator.ts";
import { playNameListener, playToneListener } from "./server.ts";

function App() {
  const [isInteracted, setIsInteracted] = useState(false);
  const [sessionName] = useQueryParam("sessionName", StringParam);
  const [jwt] = useQueryParam("jwt", StringParam);

  const handleAudioStart = () => setIsInteracted(true);

  useEffect(() => {
    if (!isInteracted) return;

    // console.log("hi");
    // const tone = Array.from({ length: 128 }, () => Math.random());
    // generateReducedJingle(tone);

    const url = "162.243.166.134:3000";

    playToneListener(url, (res) => {
      console.log("Playing tone", res);
      generateReducedJingle(res.face_encoding);
    });

    playNameListener(url, (res) => {
      console.log("Playing name", res);
      const msg = new SpeechSynthesisUtterance();
      msg.text = res.name;
      window.speechSynthesis.speak(msg);
    });
  }, [isInteracted]);

  return (
    <Center h="100%">
      {sessionName && jwt ? (
        <Stack>
          {!isInteracted && (
            <Button onClick={handleAudioStart}>Init Audio</Button>
          )}
          <VideoCall zoomSessionName={sessionName} zoomJwt={jwt} />
        </Stack>
      ) : (
        <Text>Session Name, JWT query params missing.</Text>
      )}
    </Center>
  );
}

export default App;
