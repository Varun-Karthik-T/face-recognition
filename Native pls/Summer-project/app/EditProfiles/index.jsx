import { useState, useEffect, useContext } from "react";
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import {
  Avatar,
  Button,
  Card,
  List,
  Checkbox,
  TextInput,
  Portal,
  Modal,
} from "react-native-paper";
import { getProfiles, editProfile } from "@/api/api";
import { DataContext } from "@/contexts/DataContext";

function EditProfiles() {
  const [profilesToEdit, setProfilesToEdit] = useState([]);
  const [editModalVisible, setEditModalVisible] = useState(false);
  const [selectedData, setSelectedData] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [newProfileName, setNewProfileName] = useState("");
  const [expandedProfileId, setExpandedProfileId] = useState(null);

  const { people, setLoading, fetchProfiles, profiles } =
    useContext(DataContext);

  useEffect(() => {
    getProfiles().then((response) => {
      const profiles = response.data.profiles;
      setProfilesToEdit(profiles);
    });
  }, [profiles]);

  const toggleExpandProfile = (id) => {
    setExpandedProfileId(expandedProfileId === id ? null : id);
  };

  const handleEdit = (index) => {
    console.log("Editing profile:", profilesToEdit[index]);
    setNewProfileName(profilesToEdit[index].profile_name);
    setSelectedData(profilesToEdit[index]);
    setSelectedId(profilesToEdit[index].id);
    setEditModalVisible(true);
  };

  const handleSave = async () => {
    setLoading(true);
    const modifiedData = {
      ...selectedData,
      profile_name: newProfileName,
    };
    try {
      const response = await editProfile(selectedId, modifiedData);
      fetchProfiles();
    } catch (e) {
      console.log("Error: " + e);
    } finally {
      setLoading(false);
      setEditModalVisible(false);
    }
  };

  const handleCheckboxChange = (personId) => {
    setSelectedData((prevSelectedData) => {
      const isSelected = prevSelectedData.allowed_people.some(
        (person) => person.id === personId
      );
      if (isSelected) {
        return {
          ...prevSelectedData,
          allowed_people: prevSelectedData.allowed_people.filter(
            (person) => person.id !== personId
          ),
        };
      } else {
        return {
          ...prevSelectedData,
          allowed_people: [
            ...prevSelectedData.allowed_people,
            {
              id: personId,
              name: people.find((p) => p.id === personId).name,
            },
          ],
        };
      }
    });
  };

  return (
    <>
      <View style={styles.container}>
        <Text style={styles.header}>Edit Profiles</Text>
        <FlatList
          data={profilesToEdit}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item, index }) => (
            <Card style={styles.card}>
              <View style={styles.profileRow}>
                <Text style={styles.profileName}>{item.profile_name}</Text>
                <TouchableOpacity onPress={() => handleEdit(index)}>
                  <Avatar.Icon size={40} icon="pencil" />
                </TouchableOpacity>
                <TouchableOpacity onPress={() => toggleExpandProfile(item.id)}>
                  <Avatar.Icon
                    size={40}
                    icon={
                      expandedProfileId === item.id
                        ? "chevron-up"
                        : "chevron-down"
                    }
                  />
                </TouchableOpacity>
              </View>

              {expandedProfileId === item.id && (
                <View style={styles.membersList}>
                  {item.allowed_people.length > 0 ? (
                    <>
                      {item.allowed_people.map((person) => (
                        <View key={person.id} style={styles.memberItem}>
                          <List.Item
                            title={person.name}
                            description={person.relation}
                            left={(props) => (
                              <List.Icon {...props} icon="account" />
                            )}
                          />
                        </View>
                      ))}
                    </>
                  ) : (
                    <Text style={styles.noMembersText}>
                      No members available
                    </Text>
                  )}
                </View>
              )}
            </Card>
          )}
        />
        {editModalVisible && (
          <Portal>
            <Modal
              visible={editModalVisible}
              onDismiss={() => setEditModalVisible(false)}
            >
              <View style={styles.modalContent}>
                <Text style={styles.modalTitle}>Edit Profile</Text>
                <TextInput
                  label="Profile Name"
                  value={newProfileName}
                  onChangeText={(newProfileName) =>
                    setNewProfileName(newProfileName)
                  }
                  style={styles.input}
                />
                <FlatList
                  data={people}
                  keyExtractor={(item) => item.id.toString()}
                  renderItem={({ item }) => (
                    <View style={styles.checkboxContainer}>
                      <Checkbox
                        status={
                          selectedData.allowed_people.some(
                            (person) => person.id === item.id
                          )
                            ? "checked"
                            : "unchecked"
                        }
                        onPress={() => handleCheckboxChange(item.id)}
                      />
                      <Text style={styles.checkboxLabel}>{item.name}</Text>
                    </View>
                  )}
                />
                <Button mode="contained" onPress={handleSave}>
                  Save
                </Button>
              </View>
            </Modal>
          </Portal>
        )}
      </View>
    </>
  );
}

export default EditProfiles;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  header: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 16,
  },
  card: {
    margin: 8,
  },
  profileRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    padding: 12,
    gap: 6,
  },
  profileName: {
    fontSize: 18,
    flex: 1,
    marginLeft: 12,
  },
  membersList: {
    paddingLeft: 16,
    paddingBottom: 16,
  },
  memberItem: {
    flexDirection: "row",
    alignItems: "center",
  },
  noMembersText: {
    paddingLeft: 16,
    paddingBottom: 16,
    color: "gray",
  },
  modalContainer: {
    display: "flex",
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  modalContent: {
    width: 300,
    padding: 16,
    backgroundColor: "white",
    borderRadius: 10,
    alignSelf: "center",
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 12,
  },
  input: {
    borderBottomWidth: 1,
    marginBottom: 12,
    fontSize: 16,
    padding: 8,
  },
  checkboxContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  checkboxLabel: {
    marginLeft: 8,
    fontSize: 16,
  },
});
