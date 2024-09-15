import { View, StyleSheet, TouchableOpacity } from "react-native";
import { Text, Surface, Avatar, Button } from "react-native-paper";
import { getProfiles } from "@/app/api/api";
import { useEffect, useState } from "react";
import { useNavigation } from '@react-navigation/native'; // Assuming you are using React Navigation

function Home() {
  const [profiles, setProfiles] = useState([]);
  const navigation = useNavigation();

  useEffect(() => {
    getProfiles().then((response) => {
      setProfiles(response.data.profiles);
      console.log(response.data);
    });
  }, []);

  const handleEditPress = () => {
    navigation.navigate('EditProfiles'); // Navigate to EditProfiles screen
  };

  return (
    <>
      <Surface style={styles.container}>
        <View style={styles.profileRow}>
          {profiles.slice(0, 3).map((profile) => (
            <View key={profile.id} style={styles.profileContainer}>
              <Avatar.Text size={48} label={profile.profile_name[0]} />
              <Text>{profile.profile_name}</Text>
            </View>
          ))}
        </View>
        <View style={styles.profileRow}>
          {profiles.slice(3, 5).map((profile) => (
            <View key={profile.id} style={styles.profileContainer}>
              <Avatar.Text size={48} label={profile.profile_name[0]} />
              <Text>{profile.profile_name}</Text>
            </View>
          ))}
          {/* Edit button as the sixth item */}
          <TouchableOpacity style={styles.profileContainer} onPress={handleEditPress}>
            <Avatar.Icon size={48} icon="pencil" />
            <Text>Edit</Text>
          </TouchableOpacity>
        </View>
      </Surface>
    </>
  );
}

export default Home;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 10,
  },
  profileRow: {
    flexDirection: "row",
    justifyContent: "space-around",
    marginVertical: 10,
  },
  profileContainer: {
    alignItems: "center",
    marginHorizontal: 10,
  },
});
