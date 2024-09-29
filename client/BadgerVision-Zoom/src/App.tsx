import { Center, Text } from "@mantine/core";
import VideoCall from "./VideoCall";
import { StringParam, useQueryParam } from "use-query-params";

function App() {
  const [sessionName] = useQueryParam("sessionName", StringParam);
  const [jwt] = useQueryParam("jwt", StringParam);

  return (
    <Center h="100%">
      {sessionName && jwt ? (
        <VideoCall zoomSessionName={sessionName} zoomJwt={jwt} />
      ) : (
        <Text>Session Name, JWT query params missing.</Text>
      )}
    </Center>
  );
}

export default App;
