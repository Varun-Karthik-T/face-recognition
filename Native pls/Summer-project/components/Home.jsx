import { View, StyleSheet, TouchableOpacity, Modal } from "react-native";
import { Text, Avatar, Card, Button } from "react-native-paper";
import { SafeAreaView } from "react-native-safe-area-context";
import { getProfiles, getActiveprofile, getPeople, switchProfile } from "@/api/api";
import { useEffect, useState, useContext } from "react";
import { router } from "expo-router";
import { DataContext } from "@/contexts/DataContext";

function Home() {
  const { setLoading } = useContext(DataContext);
  const [profiles, setProfiles] = useState([]);  // For listing profiles
  const [currentProfile, setCurrentProfile] = useState({});  // Initialize as empty object to avoid undefined issues
  const [modalVisible, setModalVisible] = useState(false);  // For modal visibility
  const [selectedProfile, setSelectedProfile] = useState(null);  // For selected profile change

  useEffect(() => {
    setLoading(true);
    
    // Fetch profiles and active profile
    const fetchData = async () => {
      try {
        const profileRes = await getProfiles();
        setProfiles(profileRes.data.profiles); // Set profiles array from API response

        const activeProfileRes = await getActiveprofile();
        setCurrentProfile(activeProfileRes.data); // Set active profile data

        setLoading(false);
      } catch (error) {
        console.error("Error fetching profiles or active profile", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Handle profile change logic
  const handleProfileChange = (profileId) => {
    setSelectedProfile(profileId);
    setModalVisible(true);
  };

  // Confirm profile change after modal confirmation
  const confirmProfileChange = async () => {
    try {
      await switchProfile(selectedProfile);  // Switch the profile
      const response = await getActiveprofile();  // Fetch the new active profile
      setCurrentProfile(response.data);  // Update active profile state
      setModalVisible(false);  // Hide modal
    } catch (error) {
      console.error("Failed to switch profile", error);
    }
  };

  return (
    <>
      {/* Suspicious Activity Card */}
      <Card style={styles.susContainer}>
        <Card.Content style={styles.susCard}>
          <Avatar.Icon size={50} icon="alert" />
          <SafeAreaView style={styles.susText}>
            <Text style={{ fontSize: 20, fontWeight: "bold" }}>
              Suspicious Activity
            </Text>
            <Text>There is suspicious activity detected in your house</Text>
          </SafeAreaView>
        </Card.Content>
      </Card>

      {/* Current Active Profile */}
      <Card>
        <Card.Content>
          <Text style={{ fontSize: 20, fontWeight: "bold" }}>
            Current profile - {currentProfile?.active_profile_id ?? "No active profile"} {/* Safe access with fallback */}
          </Text>
        </Card.Content>
      </Card>

      {/* Profile List */}
      <Card style={styles.container}>
        <Card.Content>
          <View style={styles.profileRow}>
            {/* Display first 3 profiles */}
            {profiles.slice(0, 3).map((profile) => (
              <TouchableOpacity
                key={profile.id}
                style={styles.profileContainer}
                onPress={() => handleProfileChange(profile.id)}
              >
                <Avatar.Text size={54} label={profile.profile_name[0]} />
                <Text>{profile.profile_name}</Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Display next 2 profiles and Edit button */}
          <View style={styles.profileRow}>
            {profiles.slice(3, 5).map((profile) => (
              <TouchableOpacity
                key={profile.id}
                style={styles.profileContainer}
                onPress={() => handleProfileChange(profile.id)}
              >
                <Avatar.Text size={54} label={profile.profile_name[0]} />
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

      {/* Profile Switching Modal */}
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
    </>
  );
}

export default Home;

const styles = StyleSheet.create({
  container: {
    margin: 10,
    height: "auto",
  },
  susContainer: {
    margin: 10,
  },
  susCard: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  susText: {
    padding: 10,
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
