import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { StyleSheet, View, Image } from "react-native";
import { Button } from "react-native-paper";
import { RootStackParamList } from "../App";
import { useCameraPermissions } from "expo-camera";

type HomeViewNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  "Home"
>;

const styles = StyleSheet.create({
  logo: {
    height: 150,
    width: "100%",
    objectFit: "contain",
  },
  container: {
    flex: 1,
    gap: 30,
    alignItems: "center",
    padding: 30,
    paddingTop: 150,
  },
});

const HomeView = () => {
  const [_, requestPermission] = useCameraPermissions();
  const navigation = useNavigation<HomeViewNavigationProp>();

  const handleScanCode = () => {
    requestPermission();
    navigation.navigate("Scan Code");
  };

  return (
    <View style={styles.container}>
      <Image style={styles.logo} source={require("./../assets/big-logo.png")} />
      <Button mode="contained-tonal" icon="camera" onPress={handleScanCode}>
        Scan Code
      </Button>
    </View>
  );
};

export default HomeView;
