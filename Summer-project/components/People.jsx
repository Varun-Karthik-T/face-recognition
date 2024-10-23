import React, { useState, useContext } from "react";
import { View, StyleSheet } from "react-native";
import {
  Card,
  Text,
  Divider,
  FAB,
  Avatar,
  Button,
  IconButton,
} from "react-native-paper";
import { deletePerson } from "@/api/api";
import { router } from "expo-router";
import { DataContext } from "@/contexts/DataContext";

export default function People() {
  const { people, fetchPeople } = useContext(DataContext);
  const [deleteMode, setDeleteMode] = useState(false);

  const handleDeletePerson = async (personId) => {
    console.log("Deleting person with ID:", personId);
    try {
      await deletePerson(personId);
      fetchPeople();
    } catch (error) {
      console.error("Failed to delete person:", error);
    }
  };

  return (
    <>
      <View style={styles.container}>
        <Card style={styles.peopleContainer}>
          {people.map((person, index) => (
            <View key={person.id}>
              <View style={styles.peopleRow}>
                <Avatar.Text size={40} label={person.name[0]} />
                <View style={styles.peopleRowTextContent}>
                  <Text style={styles.peopleName}>{person.name}</Text>
                  <Text style={styles.peopleRelation}>{person.relation}</Text>
                </View>
                {deleteMode && (
                  <IconButton
                    icon="close"
                    onPress={() => handleDeletePerson(person.id)}
                  />
                )}
              </View>
              {!(people.length - 1 === index) && (
                <Divider bold={true} theme={{ colors: { primary: "black" } }} />
              )}
            </View>
          ))}
        </Card>
        <FAB
          icon={"plus"}
          onPress={() => router.push("AddPerson")}
          style={styles.fabAdd}
        />
        <FAB
          icon={"trash-can"}
          onPress={() => setDeleteMode(!deleteMode)}
          style={styles.fabRemove}
        />
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 15,
    gap: 10,
  },
  peopleRow: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    gap: 28,
    paddingVertical: 10,
  },
  peopleRowTextContent: {
    display: "flex",
    flexDirection: "column",
    flex: 1,
  },
  peopleContainer: {
    display: "flex",
    flexDirection: "column",
    padding: 10,
  },
  fabAdd: {
    position: "absolute",
    right: 16,
    bottom: 86,
  },
  fabRemove: {
    position: "absolute",
    right: 16,
    bottom: 16,
  },
  peopleName: {
    fontSize: 17,
    fontWeight: "semibold",
  },
  peopleRelation: {
    fontSize: 14,
    fontWeight: "light",
  },
});
