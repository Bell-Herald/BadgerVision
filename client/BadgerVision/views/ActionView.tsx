import {
  NativeStackNavigationProp,
  NativeStackScreenProps,
} from "@react-navigation/native-stack";
import { StyleSheet, View, Image } from "react-native";
import { RootStackParamList } from "../App";
import { Button, Text } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";

type ActionViewNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  "Choose Action"
>;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "column",
    gap: 30,
    padding: 30,
    paddingTop: 50,
  },
});

const ActionView = ({
  route,
}: NativeStackScreenProps<RootStackParamList, "Choose Action">) => {
  const navigation = useNavigation<ActionViewNavigationProp>();
  const { zoomSessionName, zoomJwt, websocketUrl } = route.params;

  return (
    <View style={styles.container}>
      <Button
        mode="contained-tonal"
        onPress={() => navigation.navigate("Manage People")}
      >
        Manage People
      </Button>
      <Button
        mode="contained-tonal"
        onPress={() =>
          navigation.navigate("Identify People", { zoomSessionName, zoomJwt })
        }
      >
        Run Identification
      </Button>
      <Text>
        Zoom Session Name: {zoomSessionName}, Zoom JWT: {zoomJwt}, WS URL:{" "}
        {websocketUrl}
      </Text>
    </View>
  );
};

export default ActionView;
