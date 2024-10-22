import { View, StyleSheet, Alert, Image, TouchableOpacity } from "react-native";
import { Text, TextInput, Button, HelperText } from "react-native-paper";
import { useState, useContext } from "react";
import * as ImagePicker from "expo-image-picker";
import { addPerson } from "@/api/api";
import { DataContext } from "@/contexts/DataContext";

function AddPerson() {
  const [name, setName] = useState("");
  const [relation, setRelation] = useState("");
  const [images, setImages] = useState([]);

  const { setLoading, userName,fetchPeople } = useContext(DataContext);

  const pickImages = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsMultipleSelection: true,
        selectionLimit: 5,
        quality: 1,
      });

      if (!result.canceled) {
        const selectedImages = result.assets.slice(0, 5);
        setImages(selectedImages);
      }
    } catch (error) {
      console.error(error);
      Alert.alert("Error", "An error occurred while picking images");
    }
  };

  const removeImage = (index) => {
    setImages((prevImages) => prevImages.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("name", name);
    formData.append("username", userName);
    formData.append("relation", relation);
    images.forEach((image, index) => {
      formData.append("images", {
        uri: image.uri,
        name: `photo_${index}.jpg`,
        type: "image/jpeg",
      });
    });

    try {
      const response = await addPerson(formData);
      setLoading(false);
      console.log(response.data);
      if (response.data.success) {
        Alert.alert("Success", response.data.message);
        fetchPeople();
      } else {
        const errorMessages = response.data.error.join("\n");
        Alert.alert("Error", errorMessages);
      }
    } catch (error) {
      setLoading(false);
      console.error(error);
      Alert.alert("Error", "An error occurred while adding the person");
    }
  };

  return (
    <>
      <View style={styles.container}>
        <Text variant="headlineLarge">Add a new Person</Text>
        <TextInput label="Name" value={name} onChangeText={setName} />
        <TextInput
          label="Relation"
          value={relation}
          onChangeText={setRelation}
        />
        <Button mode="contained" onPress={pickImages}>
          Pick Images
        </Button>
        {images.length > 0 && (
          <>
            <HelperText type="info">Tap on an image to remove it</HelperText>
            <View style={styles.imageGrid}>
              {images.map((image, index) => (
                <TouchableOpacity
                  key={index}
                  onPress={() => removeImage(index)}
                >
                  <Image source={{ uri: image.uri }} style={styles.image} />
                </TouchableOpacity>
              ))}
            </View>
          </>
        )}
        <Button
          mode="contained"
          disabled={!(name && relation && images.length === 5)}
          onPress={handleSubmit}
          style={styles.addButton}
        >
          Add
        </Button>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    gap: 20,
  },
  imageGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
    marginTop: 10,
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: 10,
  },
  addButton: {
    marginTop: 20,
  },
});

export default AddPerson;
