import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { Appbar, Button, PaperProvider } from "react-native-paper";
import { SafeAreaProvider } from "react-native-safe-area-context";

export default function App() {
  return (
    <PaperProvider>
      <SafeAreaProvider>
        <View>
          <Appbar.Header>
            <Appbar.Content title="Badger Vision" />
          </Appbar.Header>
          <Button mode="contained-tonal">Hi</Button>
          <Text>Open up App.tsx to st art working on your app!</Text>
        </View>
      </SafeAreaProvider>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});
