import React, { useCallback } from 'react';
import { View, Text } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';

const BarcodeScreen = ({ navigation }) => {
  useFocusEffect(
    useCallback(() => {
      const parent = navigation.getParent(); // 바텀 탭 네비게이터를 가져옵니다.
      parent.setOptions({
        tabBarStyle: { display: 'none' }, // 탭 바 숨기기
        headerShown: false,
      });

      return () => parent.setOptions({
        tabBarStyle: undefined, // 탭 바 다시 표시
      });
    }, [navigation])
  );

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>바코드 입력 화면</Text>
    </View>
  );
};

export default BarcodeScreen;
