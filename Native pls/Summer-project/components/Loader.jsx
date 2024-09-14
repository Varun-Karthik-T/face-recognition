import { ActivityIndicator } from "react-native-paper";
import { DataContext } from "@/contexts/DataContext";
import { useContext } from "react";
import { View, StyleSheet } from "react-native";

function Loader() {
  const { loading } = useContext(DataContext);

  if (!loading) return null;

  return (
    <>
      <View style={styles.overlay}>
        <View style={styles.loaderContainer}>
          <ActivityIndicator animating={loading} size="large" />
        </View>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  overlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    justifyContent: "center",
    alignItems: "center",
  },
  loaderContainer: {
    justifyContent: "center",
    alignItems: "center",
  },
});

export default Loader;