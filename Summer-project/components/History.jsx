import { useState, useEffect, useContext } from "react";
import { View, StyleSheet, Image, ScrollView } from "react-native";
import { Text, Card, Button,ActivityIndicator } from "react-native-paper";
import { getHistory } from "@/api/api";
import { router } from "expo-router";
import Loader from "@/components/Loader";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    
    fetchHisotry();
  }, []);

  const fetchHisotry = () => {
    setLoading(true);
    getHistory().then((response) => {
      setHistory(response.data);
    }).catch((error) => {
      console.error("Error fetching history", error);
    }).finally(() => {
      setLoading(false);
    });
  };



  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator animating={loading} size="large" />
        <Text>Fetching History</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
        <Button icon="refresh" onPress={fetchHisotry}>
          {" "}
          Refresh{" "}
        </Button>
        <Button icon="history" onPress={() => router.push("FullHistory")}>
          View Full History
        </Button>
      </View>

      {history
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .slice(0, 2)
        .map((item) => (
          <View key={item.date} style={styles.historyItem}>
            <Text style={styles.dateText}>
              {new Date(item.date).toDateString()}
            </Text>
            <Card style={styles.card}>
              {item.entries
                .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
                .map((entry, index) => (
                  <View key={entry.id} style={styles.entryContainer}>
                    <View style={styles.entryTextContainer}>
                      <Text style={styles.entryText}>{entry.name}</Text>
                      <Text style={styles.timestampText}>
                        {new Date(entry.timestamp).toLocaleTimeString()}
                      </Text>
                    </View>
                    {entry.image && (
                      <Image
                        source={{
                          uri: `data:image/jpeg;base64,${entry.image}`,
                        }}
                        style={styles.entryImage}
                      />
                    )}
                  </View>
                ))}
            </Card>
          </View>
        ))}
    </ScrollView>
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
