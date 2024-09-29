import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../App";
import { StyleSheet, Text, View } from "react-native";
import { Button, IconButton, MD3Colors, TextInput } from "react-native-paper";
import { useRef, useState } from "react";
import { CameraView } from "expo-camera";

const styles = StyleSheet.create({
  container: {
    flex: 1,
    gap: 30,
    alignItems: "stretch",
    padding: 30,
  },
  camera: {
    aspectRatio: 1,
    width: "100%",
    borderRadius: 10,
  },
  buttonContainer: {
    display: "flex",
    flexDirection: "column",
    flexWrap: "nowrap",
    justifyContent: "space-between",
  },
});

const AddFaceView = ({
  route,
}: NativeStackScreenProps<RootStackParamList, "Add Face">) => {
  const { websocketUrl } = route.params;
  const [name, setName] = useState("");
  const [image, setImage] = useState("");

  const ref = useRef<CameraView | null>(null);

  const handleCaptureImage = async () => {
    if (!ref.current) return;

    const photo = await ref.current.takePictureAsync();
    setImage(photo?.base64 as string);
  };

  const handleScanCode = () => {};

  return (
    <View style={styles.container}>
      <TextInput
        label="Name"
        value={name}
        onChangeText={(text) => setName(text)}
      />
      <CameraView facing={"back"} style={styles.camera} ref={ref} />
      <View style={styles.buttonContainer}>
        <IconButton
          icon="camera"
          iconColor={MD3Colors.primary0}
          mode="contained-tonal"
          size={30}
          onPress={handleCaptureImage}
        />
        <Button
          mode="contained-tonal"
          onPress={handleScanCode}
          disabled={!name || !image}
        >
          Add Face
        </Button>
      </View>
      <Text></Text>
    </View>
  );
};

export default AddFaceView;
