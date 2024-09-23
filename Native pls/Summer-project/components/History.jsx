import { useState, useEffect, useContext } from "react";
import { View, StyleSheet, Image } from "react-native";
import { Text, Card, Button } from "react-native-paper";
import { getHistory } from "@/api/api";
import { DataContext } from "@/contexts/DataContext";

function History() {
  const [history, setHistory] = useState([]);
  const { setLoading } = useContext(DataContext);

  useEffect(() => {
    fetchHisotry();
  }, []);

  const fetchHisotry = () => {
    setLoading(true);
    getHistory().then((response) => {
      setHistory(response.data);
    });
    setLoading(false);
  };
  return (
    <View style={styles.container}>
      <Button icon="refresh" onPress={fetchHisotry}>
        {" "}
        Refresh{" "}
      </Button>
      {history.map((item) => (
        <View key={item.date} style={styles.historyItem}>
          <Text style={styles.dateText}>
            {new Date(item.date).toDateString()}
          </Text>
          <Card style={styles.card}>
            {item.entries.map((entry, index) => (
              <View key={entry.id} style={styles.entryContainer}>
                <View style={styles.entryTextContainer}>
                  <Text style={styles.entryText}>{entry.name}</Text>
                  <Text style={styles.timestampText}>
                    {new Date(entry.timestamp).toLocaleTimeString()}
                  </Text>
                </View>
                {entry.image && (
                  <Image
                    source={{ uri: `data:image/jpeg;base64,${entry.image}` }}
                    style={styles.entryImage}
                  />
                )}
              </View>
            ))}
          </Card>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    paddingTop: 10,
  },
  historyItem: {
    marginBottom: 20,
  },
  dateText: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 8,
  },
  card: {
    padding: 16,
  },
  entryContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 10,
  },
  entryTextContainer: {
    flex: 1,
  },
  entryText: {
    fontSize: 16,
    marginBottom: 4,
  },
  timestampText: {
    fontSize: 12,
    color: "gray",
  },
  entryImage: {
    width: 100,
    height: 100,
    borderRadius: 10,
    marginLeft: 10,
  },
});

export default History;
