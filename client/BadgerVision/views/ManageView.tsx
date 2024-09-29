import { View } from "react-native";
import { Button, List } from "react-native-paper";

const ManageView = () => {
  const ManageFace = () => {
    return <Button>Delete Face</Button>;
  };

  return (
    <View>
      <List.Section title="Identified Faces">
        <List.Item title="First item" right={() => <ManageFace />} />
        <List.Item title="Second item" />
      </List.Section>
    </View>
  );
};

export default ManageView;
