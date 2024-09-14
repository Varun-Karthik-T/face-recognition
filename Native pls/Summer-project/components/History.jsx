import { View, StyleSheet } from "react-native";
import { Text, Card, Divider,Appbar } from "react-native-paper";
import { getHistory } from "@/api/api";
import { useEffect, useState } from "react";

function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    getHistory().then((response) => {
      setHistory(response.data);
    });
  }, []);

  return (
    <>
    <View style={styles.container}>
      {history.map((item) => (
        <View key={item.date} style={styles.historyItem}>
          <Text style={styles.dateText}>{new Date(item.date).toDateString()}</Text>
          <Card style={styles.card}>
            {item.entries.map((entry, index) => (
              <View key={entry.id}>
                <Text style={styles.entryText}>{entry.name}</Text>
                <Text style={styles.timestampText}>{new Date(entry.timestamp).toLocaleTimeString()}</Text>
              </View>
            ))}
          </Card>
        </View>
      ))}
    </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    paddingTop:10,
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
  entryText: {
    fontSize: 16,
    marginBottom: 4,
  },
  timestampText: {
    fontSize: 12,
    color: "gray",
  },
});

export default History;
