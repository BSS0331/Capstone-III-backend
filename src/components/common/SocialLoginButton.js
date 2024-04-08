import React from 'react';
import { TouchableOpacity, Image, StyleSheet } from 'react-native';

const SocialLoginButton = ({ iconName, onPress }) => {
  return (
    <TouchableOpacity onPress={onPress} style={styles.button}>
      <Image source={iconName} style={styles.icon} />
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    marginBottom: 10,
  },
  icon: {
    width: 192,
    height: 48,
    resizeMode: 'contain',
  },
});

export default SocialLoginButton;
