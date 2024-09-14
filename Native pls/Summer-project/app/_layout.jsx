import AppBar from "@/components/AppBar";
import { Stack } from "expo-router";
import { PaperProvider } from "react-native-paper";
import { DataProvider } from "@/contexts/DataContext";
import Loader from "@/components/Loader";

const theme = {
  colors: {
    primary: "rgb(0, 101, 142)",
    onPrimary: "rgb(255, 255, 255)",
    primaryContainer: "rgb(199, 231, 255)",
    onPrimaryContainer: "rgb(0, 30, 46)",
    secondary: "rgb(0, 103, 129)",
    onSecondary: "rgb(255, 255, 255)",
    secondaryContainer: "rgb(185, 234, 255)",
    onSecondaryContainer: "rgb(0, 31, 41)",
    tertiary: "rgb(0, 102, 132)",
    onTertiary: "rgb(255, 255, 255)",
    tertiaryContainer: "rgb(189, 233, 255)",
    onTertiaryContainer: "rgb(0, 31, 42)",
    error: "rgb(186, 26, 26)",
    onError: "rgb(255, 255, 255)",
    errorContainer: "rgb(255, 218, 214)",
    onErrorContainer: "rgb(65, 0, 2)",
    background: "rgb(252, 252, 255)",
    onBackground: "rgb(25, 28, 30)",
    surface: "rgb(252, 252, 255)",
    onSurface: "rgb(25, 28, 30)",
    surfaceVariant: "rgb(221, 227, 234)",
    onSurfaceVariant: "rgb(65, 72, 77)",
    outline: "rgb(113, 120, 126)",
    outlineVariant: "rgb(193, 199, 206)",
    shadow: "rgb(0, 0, 0)",
    scrim: "rgb(0, 0, 0)",
    inverseSurface: "rgb(46, 49, 51)",
    inverseOnSurface: "rgb(240, 241, 243)",
    inversePrimary: "rgb(132, 207, 255)",
    elevation: {
      level0: "transparent",
      level1: "rgb(239, 244, 249)",
      level2: "rgb(232, 240, 246)",
      level3: "rgb(224, 235, 243)",
      level4: "rgb(222, 234, 241)",
      level5: "rgb(217, 231, 239)",
    },
    surfaceDisabled: "rgba(25, 28, 30, 0.12)",
    onSurfaceDisabled: "rgba(25, 28, 30, 0.38)",
    backdrop: "rgba(43, 49, 54, 0.4)",
  },
};

function RootLayout() {
  return (
    <>
      <DataProvider>
        <PaperProvider theme={theme}>
          <AppBar />
          <Stack screenOptions={{ headerShown: false }} />
          <Loader />
        </PaperProvider>
      </DataProvider>
    </>
  );
}

export default RootLayout;
