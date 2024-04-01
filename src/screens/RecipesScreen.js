import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const RecipesScreen = () => {
  return (
    <View style={styles.container}>
      <Text>레시피 화면</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default RecipesScreen;