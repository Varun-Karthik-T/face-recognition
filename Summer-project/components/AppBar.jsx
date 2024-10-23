import { usePathname, router } from "expo-router";
import { Appbar } from "react-native-paper";

function AppBar() {
  const currentRoute = usePathname();

  return (
    <Appbar.Header elevated mode="center-aligned">
      {currentRoute !== "/" && (
        <Appbar.BackAction
          onPress={() => {
            router.back();
          }}
        />
      )}
      <Appbar.Content title="VigilEye" />
    </Appbar.Header>
  );
}

export default AppBar;
