import { BarcodeScanningResult, CameraView } from "expo-camera";
import { StyleSheet, View, Alert } from "react-native";
import _ from "lodash";
import { getSessionDetails } from "../server";
import { useNavigation } from "@react-navigation/native";
import { RootStackParamList } from "../App";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";

const styles = StyleSheet.create({
  container: {
    flex: 1,
    gap: 30,
    justifyContent: "center",
    alignItems: "center",
    padding: 30,
  },
  camera: {
    aspectRatio: 1,
    width: "100%",
    borderRadius: 10,
  },
});

type ScanViewNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  "Home"
>;

const ScanView = () => {
  const navigation = useNavigation<ScanViewNavigationProp>();

  const handleBarcodeScanned = _.debounce(
    async (barcode: BarcodeScanningResult) => {
      try {
        const sessionDetails = await getSessionDetails(barcode.data);

        navigation.navigate("Choose Action", sessionDetails);
      } catch (e) {
        Alert.alert("Invalid QR Scanned", JSON.stringify(e), [
          { text: "OK", onPress: () => {} },
        ]);
      }
    },
    500
  );

  return (
    <View style={styles.container}>
      <CameraView
        facing={"back"}
        style={styles.camera}
        barcodeScannerSettings={{
          barcodeTypes: ["qr"],
        }}
        onBarcodeScanned={handleBarcodeScanned}
      />
    </View>
  );
};

export default ScanView;
