// HomeStack.js
import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from '../screens/HomeScreen';
import SettingScreen from '../screens/SettingScreen';
import ManualEntryScreen from '../screens/ManualEntryScreen';
import BarcodeScreen from '../screens/BarcodeScreen';
import ReceiptCaptureScreen from '../screens/ReceiptCaptureScreen';

const Stack = createStackNavigator();

const HomeStack = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: true }}>
      <Stack.Screen name="Home"
      component={HomeScreen}
      options={{ headerShown: false }} />
      <Stack.Screen name="Setting"
      component={SettingScreen}
      options={{ title: '설정' }} />
      <Stack.Screen name="ManualEntry"
      component={ManualEntryScreen}
      options={{ title: '수동 입력' }} />
      <Stack.Screen name="Barcode"
      component={BarcodeScreen}
      options={{ title: '바코드' }} />
      <Stack.Screen name="ReceiptCapture"
      component={ReceiptCaptureScreen}
      options={{ title: '영수증' }} />
    </Stack.Navigator>
  );
};

export default HomeStack;