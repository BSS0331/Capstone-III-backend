import React, { useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native'; // 네비게이션 기능을 사용하기 위해 필요
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'; // 하단 탭 네비게이터 생성을 위해 필요
import { Ionicons } from '@expo/vector-icons'; // 아이콘을 사용하기 위해 필요
import { FAB } from 'react-native-paper';  // 플로팅 액션 버튼을 위해 필요

// 홈 화면 컴포넌트 정의
function HomeScreen({ navigation }) {
  const [state, setState] = useState({ open: false });

  const onStateChange = ({ open }) => setState({ open });

  const { open } = state;

  return (
    <View style={styles.container}>
      <Text>메인메뉴 화면</Text>
      <FAB.Group  // 플로팅 액션 버튼
        open={open}
        icon={open ? 'close' : 'plus'}
        actions={[  // 액션 아이콘 정의
          { icon: 'cog', label: '설정', onPress: () => console.log('설정 Pressed'), },
          { icon: 'pencil', label: '수동 입력', onPress: () => console.log('수동 입력 Pressed'), },
          { icon: 'receipt', label: '영수증', onPress: () => console.log('영수증 Pressed'), },
          { icon: 'barcode', label: '바코드', onPress: () => console.log('바코드 Pressed'), },
       ]}
        onStateChange={onStateChange}
        onPress={() => {
          if (open) {
            // FAB를 닫음
          }
        }}
        fabStyle={styles.fab}  // 메인 FAB의 배경색 변경
        color='white'  // 메인 FAB 아이콘 색상 변경
      />
    </View>
  );
}

// 플로팅 액션 버튼 스타일 정의
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: 'skyblue',
    borderRadius: 50,
  },
});

// 레시피 화면 컴포넌트 정의
function RecipesScreen() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>레시피 화면</Text>
    </View>
  );
}

// 냉장고 화면 컴포넌트 정의
function FridgeScreen() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>냉장고 화면</Text>
    </View>
  );
}

const Tab = createBottomTabNavigator(); // 하단 탭 네비게이터 인스턴스 생성

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          // 각 탭에 따라 아이콘 설정
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;

            if (route.name === '메인메뉴') {
              iconName = focused ? 'home' : 'home-outline';
            } else if (route.name === '레시피') {
              iconName = focused ? 'book' : 'book-outline';
            } else if (route.name === '냉장고') {
              iconName = focused ? 'restaurant' : 'restaurant-outline';
            }

            // Ionicons에서 선택한 아이콘을 반환
            return <Ionicons name={iconName} size={size} color={color} />;
          },
        })}
        tabBarOptions={{
          activeTintColor: 'tomato', // 활성 탭의 아이콘 색상
          inactiveTintColor: 'gray', // 비활성 탭의 아이콘 색상
        }}
      >
        {/* 탭 네비게이터에 화면 추가 */}
        <Tab.Screen name="메인메뉴" component={HomeScreen} />
        <Tab.Screen name="레시피" component={RecipesScreen} />
        <Tab.Screen name="냉장고" component={FridgeScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
