import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

import HomeStack from './HomeStack';
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
          if (route.name === 'Home') {  // '메인메뉴'
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Recipes') {  // '레시피'
            iconName = focused ? 'book' : 'book-outline';
          } else if (route.name === 'Fridge') {  // 냉장고'
            iconName = focused ? 'restaurant' : 'restaurant-outline';
          }
          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: 'tomato', // 활성 탭의 아이콘 색상
        tabBarInactiveTintColor: 'gray', // 비활성 탭의 아이콘 색상
        tabBarStyle: [ // 탭 바 스타일
          {
            display: 'flex'
          },
          null
        ]
      })}
    >
      <Tab.Screen name="Home" component={HomeStack} options={{ title: '메인메뉴' }}/>
      <Tab.Screen name="Recipes" component={RecipesScreen} options={{ title: '레시피' }}/>
      <Tab.Screen name="Fridge" component={FridgeScreen} options={{ title: '냉장고' }}/>
    </Tab.Navigator>
  );
};

export default TabNavigator;
