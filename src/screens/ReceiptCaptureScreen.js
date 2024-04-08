import React, { useCallback } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { useFocusEffect } from '@react-navigation/native';
import RecipesScreen from '../screens/RecipesScreen';
import SearchScreen from '../screens/SearchScreen';

const Stack = createStackNavigator();

const RecipesStack = ({ navigation }) => {
    useFocusEffect(
        useCallback(() => {
            const parent = navigation.getParent(); // 상위 네비게이터를 가져옴

            // parent가 존재하면 탭 바와 헤더를 숨김
            if (parent) {
                parent.setOptions({
                    tabBarStyle: { display: 'none' },
                    headerShown: false,
                });

                // 화면에서 벗어날 때 탭 바와 헤더를 다시 표시
                return () => parent.setOptions({
                    tabBarStyle: undefined,
                    headerShown: true,
                });
            }
        }, [navigation])
    );

    return (
        <Stack.Navigator>
            <Stack.Screen name="Recipes" component={RecipesScreen} />
            <Stack.Screen name="SearchScreen" component={SearchScreen} options={{ title: '검색' }} />
        </Stack.Navigator>
    );
};

export default RecipesStack;