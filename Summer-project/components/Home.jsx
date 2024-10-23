import {
  View,
  StyleSheet,
  TouchableOpacity,
  Modal,
  Image,
  ScrollView,
} from "react-native";
import {
  Text,
  Avatar,
  Card,
  Button,
  useTheme,
  ActivityIndicator,
  Divider,
} from "react-native-paper";
import { SafeAreaView } from "react-native-safe-area-context";
import {
  getProfiles,
  getActiveprofile,
  getPeople,
  switchProfile,
  getNotifications,
  getPermissions,
  changePermission,
} from "@/api/api";
import { useEffect, useState, useContext } from "react";
import { router } from "expo-router";
import Notify from "@/api/notify";
import Loader from "./Loader";

function Home() {
  const [profiles, setProfiles] = useState([]);
  const [currentProfile, setCurrentProfile] = useState({});
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [permissions, setPermissions] = useState([]);

  const theme = useTheme();

  useEffect(() => {
    setLoading(true);

    const fetchData = async () => {
      try {
        const profileRes = await getProfiles();
        setProfiles(profileRes.data.profiles);

        const activeProfileRes = await getActiveprofile();
        setCurrentProfile(activeProfileRes.data);

        const notifyRes = await getNotifications();
        setNotifications(notifyRes.data.suspicious_activity);

        const permissionsRes = await getPermissions();
        setPermissions(permissionsRes.data.entries);

        setLoading(false);
      } catch (error) {
        console.error("Error fetching profiles or active profile", error);
        setLoading(false);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleProfileChange = (profileId) => {
    setSelectedProfile(profileId);
    setModalVisible(true);
  };

  const confirmProfileChange = async () => {
    try {
      await switchProfile(selectedProfile);
      const response = await getActiveprofile();
      setCurrentProfile(response.data);
      setModalVisible(false);
    } catch (error) {
      console.error("Failed to switch profile", error);
    }
  };

  const handlePermissionChange = async (permissionId, allow) => {
    try {
      await changePermission(permissionId, allow);
      const permissionsRes = await getPermissions();
      setPermissions(permissionsRes.data.entries);
    } catch (error) {
      console.error("Failed to change permission", error);
    }
  };

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator animating={loading} size="large" />
        <Text>Fetching Profiles</Text>
      </View>
    );
  }

  return (
    <>
      {/* Suspicious Activity Card */}
      <ScrollView>
        <Card style={styles.susContainer}>
          <Card.Content style={styles.susCard}>
            <Avatar.Icon size={50} icon="alert" />
            <SafeAreaView style={styles.susText}>
              {notifications.length > 0 ? (
                notifications.slice(0, 2).map((activity, index) => (
                  <View key={index}>
                    <Text style={{ fontSize: 15, fontWeight: "bold" }}>
                      {activity.classification} at {"\n"}
                      {new Date(activity.timestamp).toLocaleString()}
                      {"\n"}
                    </Text>
                    {index === 0 && <Divider />}
                  </View>
                ))
              ) : (
                <Text>No recent suspicious activity detected</Text>
              )}
            </SafeAreaView>
          </Card.Content>
        </Card>

        <Card style={{ marginVertical: 10 }}>
          <Card.Content>
            <Text style={{ fontSize: 20, fontWeight: "bold" }}>
              Permissions
            </Text>
            {permissions.map((permission, index) => (
              <View
                key={index}
                style={{ flexDirection: "row", alignItems: "center" }}
              >
                <Image
                  source={{ uri: `data:image/jpeg;base64,${permission.image}` }}
                  style={{ width: 100, height: 100, marginRight: 10 }}
                />
                <View style={{ flexDirection: "column", gap: 20 }}>
                  <Text style={{ fontWeight: "bold" ,fontSize:17}}>
                    {permission.name} is at the door
                  </Text>
                  <Text>{permission.reason}</Text>
                  <View
                    style={{
                      display: "flex",
                      flexDirection: "row",
                      justifyContent: "space-evenly",
                      gap: 20,
                    }}
                  >
                    <Button
                      mode="contained"
                      onPress={() => handlePermissionChange(index, true)}
                    >
                      Open door
                    </Button>
                    <Button
                      mode="outlined"
                      onPress={() => handlePermissionChange(index, false)}
                    >
                      Deny
                    </Button>
                  </View>
                </View>
              </View>
            ))}
          </Card.Content>
        </Card>

        <Card>
          <Card.Content>
            <Text style={{ fontSize: 20, fontWeight: "bold" }}>
              Current profile -{" "}
              {currentProfile?.active_profile_id ?? "No active profile"}
            </Text>
          </Card.Content>
        </Card>

        <Card style={styles.container}>
          <Card.Content>
            <View style={styles.profileRow}>
              {profiles.slice(0, 3).map((profile) => (
                <TouchableOpacity
                  key={profile.id}
                  style={styles.profileContainer}
                  onPress={() => handleProfileChange(profile.id)}
                >
                  <Avatar.Text
                    size={54}
                    label={profile.profile_name[0]}
                    style={{
                      backgroundColor:
                        profile.id === currentProfile.active_profile_id
                          ? "green"
                          : theme.colors.primary,
                    }}
                  />
                  <Text>{profile.profile_name}</Text>
                </TouchableOpacity>
              ))}
            </View>

            <View style={styles.profileRow}>
              {profiles.slice(3, 5).map((profile) => (
                <TouchableOpacity
                  key={profile.id}
                  style={styles.profileContainer}
                  onPress={() => handleProfileChange(profile.id)}
                >
                  <Avatar.Text
                    size={54}
                    label={profile.profile_name[0]}
                    style={{
                      backgroundColor:
                        profile.id === currentProfile.active_profile_id
                          ? "green"
                          : theme.colors.primary,
                    }}
                  />
                  <Text>{profile.profile_name}</Text>
                </TouchableOpacity>
              ))}

              <TouchableOpacity
                style={styles.profileContainer}
                onPress={() => router.push("EditProfiles")}
              >
                <Avatar.Icon size={54} icon="pencil" />
                <Text>Edit</Text>
              </TouchableOpacity>
            </View>
          </Card.Content>
        </Card>

        <Modal
          transparent={true}
          visible={modalVisible}
          animationType="slide"
          onRequestClose={() => setModalVisible(false)}
        >
          <View style={styles.modalContainer}>
            <View style={styles.modalContent}>
              <Text style={styles.modalText}>Switch to this profile?</Text>
              <Button mode="contained" onPress={confirmProfileChange}>
                Confirm
              </Button>
              <Button onPress={() => setModalVisible(false)}>Cancel</Button>
            </View>
          </View>
        </Modal>
      </ScrollView>
    </>
  );
}

export default Home;

const styles = StyleSheet.create({
  container: {
    margin: 10,
  },
  susContainer: {
    height: "auto",
  },
  susCard: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-evenly",
    alignItems: "center",
  },
  susText: {
    fontSize: 20,
    fontWeight: "bold",
  },
  profileRow: {
    flexDirection: "row",
    justifyContent: "space-around",
    marginVertical: 12,
    flexWrap: "wrap",
  },
  profileContainer: {
    alignItems: "center",
    marginHorizontal: 10,
    paddingVertical: 10,
  },
  modalContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0,0,0,0.3)",
  },
  modalContent: {
    width: 300,
    padding: 20,
    backgroundColor: "white",
    borderRadius: 10,
    alignItems: "center",
  },
  modalText: {
    fontSize: 18,
    marginBottom: 20,
  },
});
