import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';

const SignUpScreen = () => {
  const [name, setName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [nickname, setNickname] = useState('');

  const validateInput = () => {
    if (!name || !userId || !password || !confirmPassword || !nickname) {
      Alert.alert("Error", "Please fill in all required fields.");
      return false;
    }
    if (/[^a-zA-Z0-9]/.test(password)) {
      Alert.alert("Error", "Password should not contain special characters.");
      return false;
    }
    if (password !== confirmPassword) {
      Alert.alert("Error", "Passwords do not match.");
      return false;
    }
    return true;
  };

  const handleSubmit = () => {
    if (validateInput()) {
      Alert.alert("Success", "Sign up successful!");
      // 회원가입 성공 처리 로직 추가
    }
  };

  return (
    <View style={styles.container}>
      <TextInput 
        placeholder="Name *"
        value={name}
        onChangeText={setName}
        style={styles.input}
      />
      <TextInput 
        placeholder="Phone Number"
        value={phoneNumber}
        onChangeText={setPhoneNumber}
        style={styles.input}
      />
      <TextInput 
        placeholder="ID *"
        value={userId}
        onChangeText={setUserId}
        style={styles.input}
      />
      <TextInput 
        placeholder="Password *"
        value={password}
        onChangeText={setPassword}
        secureTextEntry={true}
        style={styles.input}
      />
      <TextInput 
        placeholder="Confirm Password *"
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry={true}
        style={styles.input}
      />
      <TextInput 
        placeholder="Nickname *"
        value={nickname}
        onChangeText={setNickname}
        style={styles.input}
      />
      <TouchableOpacity onPress={handleSubmit} style={styles.button}>
        <Text>Sign Up</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  input: {
    width: '100%',
    marginVertical: 8,
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    borderRadius: 5,
  },
  button: {
    marginTop: 20,
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 5,
  }
});

export default SignUpScreen;
