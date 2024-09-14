import React, { useState, useEffect } from "react";
import { View, StyleSheet } from "react-native";
import {
  Card,
  Text,
  Divider,
  FAB,
  Avatar,
  Button,
} from "react-native-paper";
import { getPeople } from "@/api/api";
import { router } from "expo-router";

export default function People() {
  const [people, setPeople] = useState([]);

  useEffect(() => {
    fetchPeople();
  }, []);

  const fetchPeople = () => {
    getPeople().then((response) => {
      setPeople(response.data);
    });
  }

  return (
    <>
      <View style={styles.container}>
        <Button onPress={fetchPeople} icon="refresh"> Refresh </Button>
        <Card style={styles.peopleContainer}>
          {people.map((person, Index) => (
            <View key={person.id}>
              <View style={styles.peopleRow}>
                <Avatar.Text size={40} label={person.name[0]} />
                <View style={styles.peopleRowTextContent}>
                  <Text style={styles.peopleName}>{person.name}</Text>
                  <Text style={styles.peopleRelation}>{person.relation}</Text>
                </View>
              </View>
              {!(people.length - 1 == Index) && (
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
    gap: 28,
    paddingVertical: 10,
  },
  peopleRowTextContent: {
    display: "flex",
    flexDirection: "column",
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
