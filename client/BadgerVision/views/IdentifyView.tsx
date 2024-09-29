import { EmitterSubscription, View, StyleSheet } from "react-native";
import { Text } from "react-native-paper";
import { RootStackParamList } from "../App";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { useEffect, useRef, useState } from "react";
import WebView from "react-native-webview";

type CallViewProps = {
  zoomSessionName: string;
  zoomJwt: string;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    height: "100%",
    width: "100%",
  },
});

const IdentifyView = ({
  route,
}: NativeStackScreenProps<RootStackParamList, "Identify People">) => {
  const { zoomSessionName, zoomJwt } = route.params;

  const identityPageUrl = `https://badgervision-5a9a2.web.app/?sessionName=${zoomSessionName}&jwt=${zoomJwt}`;

  return <WebView style={styles.container} source={{ uri: identityPageUrl }} />;
};

export default IdentifyView;
