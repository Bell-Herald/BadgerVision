import { createNativeStackNavigator } from "@react-navigation/native-stack";
import {
  MD3LightTheme as DefaultTheme,
  PaperProvider,
} from "react-native-paper";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { NavigationContainer } from "@react-navigation/native";
import HomeView from "./views/HomeView";
import AppNavigationBar from "./components/AppNavigationBar";
import ScanView from "./views/ScanView";
import theme from "./constants/theme";
import ActionView from "./views/ActionView";
import ManageView from "./views/ManageView";
import IdentifyView from "./views/IdentifyView";
import AddFaceView from "./views/AddFaceView";

export type SessionDetails = {
  zoomSessionName: string;
  zoomJwt: string;
  websocketUrl: string;
};

export type ManagePeopleProps = {
  websocketUrl: string;
};

export type AddFaceProps = {
  websocketUrl: string;
};

export type IdentifyViewProps = {
  zoomSessionName: string;
  zoomJwt: string;
  websocketUrl: string;
};

export type RootStackParamList = {
  Home: undefined;
  "Scan Code": undefined;
  "Choose Action": SessionDetails;
  "Manage People": ManagePeopleProps;
  "Identify People": IdentifyViewProps;
  "Add Face": AddFaceProps;
};

export default function App() {
  const Stack = createNativeStackNavigator<RootStackParamList>();

  return (
    <PaperProvider theme={theme}>
      <SafeAreaProvider>
        <NavigationContainer>
          <Stack.Navigator
            initialRouteName="Home"
            screenOptions={{
              header: (props) => <AppNavigationBar {...props} />,
            }}
          >
            <Stack.Screen name="Home" component={HomeView} />
            <Stack.Screen name="Scan Code" component={ScanView} />
            <Stack.Screen name="Choose Action" component={ActionView} />
            <Stack.Screen name="Manage People" component={ManageView} />
            <Stack.Screen name="Identify People" component={IdentifyView} />
            <Stack.Screen name="Add Face" component={AddFaceView} />
          </Stack.Navigator>
        </NavigationContainer>
      </SafeAreaProvider>
    </PaperProvider>
  );
}
