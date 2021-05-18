import { StatusBar } from 'expo-status-bar';
import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text style = {styles.text}>READY</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#008450',
    alignItems: 'center',
    justifyContent: 'center',
  },

  text: {
      fontFamily: "Gotham-Black",
      color: "white"
  }
});