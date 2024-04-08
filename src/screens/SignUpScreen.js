import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';

const SignUpScreen = () => {
  // 상태 관리 Hooks를 사용하여 입력 필드의 값 저장
  const [name, setName] = useState('');
  const [userId, setUserId] = useState(''); // 사용자 이메일 주소
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // 입력 값 검증 함수
  const validateInput = () => {
    // 모든 필드가 채워졌는지 확인
    if (!name || !userId || !password || !confirmPassword) {
      Alert.alert("오류", "모든 필수 필드를 입력하세요.");
      return false;
    }
    // 이메일 형식 검증
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userId)) {
      Alert.alert("오류", "올바른 이메일 형식을 입력하세요.");
      return false;
    }
    // 비밀번호에 특수 문자 포함 여부 검증
    if (/[^a-zA-Z0-9]/.test(password)) {
      Alert.alert("오류", "비밀번호에 특수 문자를 포함할 수 없습니다.");
      return false;
    }
    // 비밀번호 일치 여부 검증
    if (password !== confirmPassword) {
      Alert.alert("오류", "비밀번호가 일치하지 않습니다.");
      return false;
    }
    // 모든 검증 통과시 true 반환
    return true;
  };

  // '가입하기' 버튼 클릭 시 실행되는 함수
  const handleSubmit = () => {
    if (validateInput()) {
      Alert.alert("성공", "회원가입에 성공했습니다!");
      // 여기에 회원가입 성공 처리 로직을 추가하면 됩니다. 예를 들어, DB에 사용자 정보를 저장하는 API 호출 등
    }
  };

  return (
    <View style={styles.container}>
      <TextInput 
        placeholder="닉네임"
        value={name}
        onChangeText={setName}
        style={styles.input}
      />
      <TextInput 
        placeholder="이메일"
        value={userId}
        onChangeText={setUserId}
        style={styles.input}
      />
      <TextInput 
        placeholder="비밀번호"
        value={password}
        onChangeText={setPassword}
        secureTextEntry={true}
        style={styles.input}
      />
      <TextInput 
        placeholder="비밀번호 확인"
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry={true}
        style={styles.input}
      />
      <TouchableOpacity onPress={handleSubmit} style={styles.button}>
        <Text style={styles.buttonText}>가입하기</Text>
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
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
  }
});

export default SignUpScreen;
