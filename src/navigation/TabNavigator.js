import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';  // 하단 탭 네비게이터 생성 함수를 불러옴
import { Ionicons } from '@expo/vector-icons';  // Expo 아이콘 라이브러리를 불러옴

import HomeStack from './HomeStack';                   // 로컬 HomeStack 컴포넌트를 불러옴
import RecipesScreen from '../screens/RecipesScreen';  // 로컬 RecipesScreen 컴포넌트를 불러옴
import FridgeScreen from '../screens/FridgeScreen';    // 로컬 FridgeScreen 컴포넌트를 불러옴

const Tab = createBottomTabNavigator();  // 하단 탭 네비게이터를 생성

// 하단 네비게이터
const TabNavigator = () => {  // TabNavigator 컴포넌트를 함수형 컴포넌트로 정의
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({  // 각 탭 화면에 대한 옵션을 정의
        tabBarIcon: ({ focused, color, size }) => {  // Expo Icon 설정
          let iconName;
          if (route.name === 'Home') {             // '메인메뉴' 탭인 경우
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Recipes') {   // '레시피' 탭인 경우
            iconName = focused ? 'book' : 'book-outline';
          } else if (route.name === 'Fridge') {    // 냉장고' 탭인 경우
            iconName = focused ? 'restaurant' : 'restaurant-outline';
          }
          return <Ionicons name={iconName} size={size} color={color} />;  // 아이콘 컴포넌트 렌더링
        },
        tabBarActiveTintColor: 'tomato', // 활성 탭의 아이콘 색상
        tabBarInactiveTintColor: 'gray', // 비활성 탭의 아이콘 색상
        tabBarStyle: [ // 탭 바 스타일 설정
          {
            display: 'flex'
          },
          null
        ]
      })}
    >
      <Tab.Screen name="Home" component={HomeStack} options={{ title: '메인메뉴', headerShown: false }}/>
      <Tab.Screen name="Recipes" component={RecipesScreen} options={{ title: '레시피' }}/>
      <Tab.Screen name="Fridge" component={FridgeScreen} options={{ title: '냉장고' }}/>
    </Tab.Navigator>
  );
};

export default TabNavigator;
