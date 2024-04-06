import React, { useLayoutEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';

const SettingScreen = ({ navigation }) => {
    useLayoutEffect(() => {
        navigation.setOptions({
          
        });
      }, [navigation]);

    return (
    <View style={styles.container}>
      <Text>설정 화면</Text>
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

export default SettingScreen;
