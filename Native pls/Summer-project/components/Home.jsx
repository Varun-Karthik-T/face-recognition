import { View, StyleSheet, TouchableOpacity } from "react-native";
import { Text, Avatar, Card } from "react-native-paper";
import { getProfiles } from "@/api/api";
import { useEffect, useState } from "react";
import { Route } from "expo-router/build/Route";
import { router } from "expo-router";

function Home() {
  const [profiles, setProfiles] = useState([]);

  useEffect(() => {
    getProfiles().then((response) => {
      setProfiles(response.data.profiles);
   
    });
  }, []);



  return (
    <>
      <Card>
        <Card.Content style={styles.susCard}>
          <Avatar.Icon size={50} icon="alert" />
          <View style={styles.susText}>
            <Text style={{ fontSize: 20, fontWeight: "bold" }}>
              Suspicious Activity
            </Text>
            <Text>There is a suspicious activity detected in your house</Text>
          </View>
        </Card.Content>
      </Card>
      <Card style={styles.container}>
        <Card.Content>
          <View style={styles.profileRow}>
            {profiles.slice(0, 3).map((profile) => (
              <View key={profile.id} style={styles.profileContainer}>
                <Avatar.Text size={54} label={profile.profile_name[0]} />
                <Text>{profile.profile_name}</Text>
              </View>
            ))}
          </View>
          <View style={styles.profileRow}>
            {profiles.slice(3, 5).map((profile) => (
              <View key={profile.id} style={styles.profileContainer}>
                <Avatar.Text size={54} label={profile.profile_name[0]} />
                <Text>{profile.profile_name}</Text>
              </View>
            ))}

            <TouchableOpacity
              style={styles.profileContainer}
              onPress={(pro)=>router.push("EditProfiles")}
            >
              <Avatar.Icon size={54} icon="pencil" />
              <Text>Edit</Text>
            </TouchableOpacity>
          </View>
        </Card.Content>
      </Card>
    </>
  );
}

export default Home;

const styles = StyleSheet.create({
  container: {
   
    margin: 10,
    height: 'auto', 

  },
  susCard: {
    margin: 10,
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 10,
    margin: 10,
  },
  susText: {
    fontSize: 20,
    fontWeight: "bold",
    paddingRight: 30,
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
});
