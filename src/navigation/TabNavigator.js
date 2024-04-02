import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import HomeScreen from '../screens/HomeScreen';
import RecipesScreen from '../screens/RecipesScreen';
import FridgeScreen from '../screens/FridgeScreen';

const Tab = createBottomTabNavigator();

// 하단 네비게이터
const TabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {  // Expo Icon
          let iconName;
          if (route.name === '메인메뉴') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === '레시피') {
            iconName = focused ? 'book' : 'book-outline';
          } else if (route.name === '냉장고') {
            iconName = focused ? 'restaurant' : 'restaurant-outline';
          }
          return <Ionicons name={iconName} size={size} color={color} />;
        },
      })}
      tabBarOptions={{
        activeTintColor: 'tomato',
        inactiveTintColor: 'gray',
      }}
    >
      <Tab.Screen name="메인메뉴" component={HomeScreen} />
      <Tab.Screen name="레시피" component={RecipesScreen} />
      <Tab.Screen name="냉장고" component={FridgeScreen} />
    </Tab.Navigator>
  );
};

export default TabNavigator;