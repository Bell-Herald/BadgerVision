import { useEffect, useState } from "react";
import { StyleSheet, View } from "react-native";
import { Button, FAB, List } from "react-native-paper";
import { RootStackParamList } from "../App";
import {
  NativeStackNavigationProp,
  NativeStackScreenProps,
} from "@react-navigation/native-stack";
import {
  Face,
  facesUpdatedListener,
  refreshFaces,
  removeFace,
} from "../server";
import { useNavigation } from "@react-navigation/native";

type ManageViewNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  "Manage People"
>;

const styles = StyleSheet.create({
  fab: {
    position: "absolute",
    margin: 30,
    right: 0,
    bottom: 0,
  },
  container: {
    height: "100%",
  },
});

const ManageView = ({
  route,
}: NativeStackScreenProps<RootStackParamList, "Manage People">) => {
  const { websocketUrl } = route.params;
  const navigation = useNavigation<ManageViewNavigationProp>();
  const [faces, setFaces] = useState<Face[]>();

  useEffect(() => {
    refreshFaces(websocketUrl);

    const remove = facesUpdatedListener(websocketUrl, (_faces) => {
      setFaces(_faces);
    });

    return () => {
      remove();
    };
  }, []);

  const ManageFace = ({ faceId }: { faceId: string }) => {
    const handleRemoveFace = () => {
      removeFace(websocketUrl, faceId);
    };

    return <Button onPress={handleRemoveFace}>Delete Face</Button>;
  };

  return (
    <View style={styles.container}>
      <List.Section title="Identified Faces">
        {faces?.map((face) => (
          <List.Item
            key={face.id}
            title={face.name}
            right={() => <ManageFace faceId={face.id} />}
          />
        ))}
      </List.Section>
      <FAB
        icon="plus"
        style={styles.fab}
        onPress={() => navigation.navigate("Add Face", { websocketUrl })}
      />
    </View>
  );
};

export default ManageView;
