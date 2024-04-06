import React from 'react';
import { NavigationContainer } from '@react-navigation/native';

// import HomeScreen from './src/screens/HomeScreen';
// import SettingScreen from './src/screens/SettingScreen';
// import ManualEntryScreen from './src/screens/ManualEntryScreen';
// import ReceiptCaptureScreen from './src/screens/ReceiptCaptureScreen';
// import BarcodeScreen from './src/screens/BarcodeScreen';
import TabNavigator from './src/navigation/TabNavigator';

const App = () => {
  return (
    <NavigationContainer>
      <TabNavigator />
    </NavigationContainer>
  );
};

export default App;
