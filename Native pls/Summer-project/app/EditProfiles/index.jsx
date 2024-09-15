import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  FlatList,
  TouchableOpacity,
  Modal,
  StyleSheet,
} from "react-native";
import { Avatar, Button, Card, List, Checkbox } from "react-native-paper";
import { getProfiles } from "@/api/api";

function EditProfiles() {
  const [profilesToEdit, setProfilesToEdit] = useState([]);
  const [editModalVisible, setEditModalVisible] = useState(false);
  const [addPersonModalVisible, setAddPersonModalVisible] = useState(false);
  const [selectedProfileIndex, setSelectedProfileIndex] = useState(null);
  const [newProfileName, setNewProfileName] = useState("");
  const [expandedProfileId, setExpandedProfileId] = useState(null); // For expanding the profile
  const [selectedPeople, setSelectedPeople] = useState({}); // To track selected people for each profile

  useEffect(() => {
    getProfiles().then((response) => {
      const profiles = response.data.profiles;
      setProfilesToEdit(profiles);
      const initialSelection = profiles.reduce((acc, profile) => {
        acc[profile.id] = [];
        return acc;
      }, {});
      setSelectedPeople(initialSelection);
    });
  }, []);

  // const handleEditPress = (index) => {
  //   setSelectedProfileIndex(index);
  //   setNewProfileName(profilesToEdit[index].profile_name);
  //   setEditModalVisible(true);
  // };

  const handleSaveProfile = () => {
    const updatedProfiles = [...profilesToEdit];
    updatedProfiles[selectedProfileIndex].profile_name = newProfileName;
    setProfilesToEdit(updatedProfiles);
    setEditModalVisible(false);
  };

  const handleAddPerson = (index) => {
    setAddPersonModalVisible(true);
  };

  const toggleExpandProfile = (id) => {
    setExpandedProfileId(expandedProfileId === id ? null : id); // Toggle expansion
  };

  const toggleSelectPerson = (profileId, personId) => {
    setSelectedPeople((prevSelected) => {
      const updatedSelection = [...prevSelected[profileId]];
      if (updatedSelection.includes(personId)) {
        return {
          ...prevSelected,
          [profileId]: updatedSelection.filter((id) => id !== personId),
        };
      } else {
        return {
          ...prevSelected,
          [profileId]: [...updatedSelection, personId],
        };
      }
    });
  };

  const handleDeleteSelected = (profileId) => {
    const updatedProfiles = profilesToEdit.map((profile) => {
      if (profile.id === profileId) {
        return {
          ...profile,
          allowed_people: profile.allowed_people.filter(
            (person) => !selectedPeople[profileId].includes(person.id)
          ),
        };
      }
      return profile;
    });
    setProfilesToEdit(updatedProfiles);
    setSelectedPeople((prevSelected) => ({
      ...prevSelected,
      [profileId]: [],
    }));
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Edit Profiles</Text>
      <FlatList
        data={profilesToEdit}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item, index }) => (
          <Card style={styles.card}>
            <View style={styles.profileRow}>
              {/* <Avatar.Text size={54} label={item.profile_name[0]} /> */}
              <Text style={styles.profileName}>{item.profile_name}</Text>
              {/* <TouchableOpacity onPress={() => handleEditPress(index)}>
                <Avatar.Icon size={35} icon="pencil" />
              </TouchableOpacity> */}
              <TouchableOpacity onPress={() => handleAddPerson(index)}>
                <Avatar.Icon size={35} icon="plus" />
              </TouchableOpacity>
              <TouchableOpacity onPress={() => toggleExpandProfile(item.id)}>
                <Avatar.Icon
                  size={35}
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
                        <Checkbox
                          status={
                            selectedPeople[item.id]?.includes(person.id)
                              ? "checked"
                              : "unchecked"
                          }
                          onPress={() => toggleSelectPerson(item.id, person.id)}
                        />
                        <List.Item
                          title={person.name}
                          description={person.relation}
                          left={(props) => (
                            <List.Icon {...props} icon="account" />
                          )}
                        />
                      </View>
                    ))}
                    <Button
                      mode="contained"
                      onPress={() => handleDeleteSelected(item.id)}
                      disabled={selectedPeople[item.id].length === 0}
                    >
                      Delete Selected
                    </Button>
                  </>
                ) : (
                  <Text style={styles.noMembersText}>No members available</Text>
                )}
              </View>
            )}
          </Card>
        )}
      />
    </View>
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
    marginBottom: 12,
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
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  modalContent: {
    width: 300,
    padding: 16,
    backgroundColor: "white",
    borderRadius: 10,
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
});
