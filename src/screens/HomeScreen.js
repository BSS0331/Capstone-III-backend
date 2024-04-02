import React, { useState } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { FAB } from 'react-native-paper';

// Home 화면
const HomeScreen = () => {
  const [isFabOpen, setIsFabOpen] = useState(false);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>메인메뉴 화면</Text>
      <FAB.Group  // FAB 그룹 (설정, 수동 입력, 영수증, 바코드 버튼)
        open={isFabOpen}
        icon={isFabOpen ? 'close' : 'plus'}
        color= '#4E348B'
        actions={[
          { icon: 'cog', label: '설정', onPress: () => console.log('설정 Pressed'), small: false },
          { icon: 'pencil', label: '수동 입력', onPress: () => console.log('수동 입력 Pressed'), small: false },
          { icon: 'receipt', label: '영수증', onPress: () => console.log('영수증 Pressed'), small: false },
          { icon: 'barcode', label: '바코드', onPress: () => console.log('바코드 Pressed'), small: false },
        ]}
        onStateChange={({ open }) => setIsFabOpen(open)}
        onPress={() => {
          setIsFabOpen(!isFabOpen);
        }}
        fabStyle={styles.fab} // FAB 스타일을 적용
      />
    </View>
  );
};

// FAB 스타일
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  text: {
    fontSize: 18,
    marginBottom: 20,
  },
  fab: {
    backgroundColor: '#EEE8F4',
    borderRadius: 28,
  },
});

export default HomeScreen;
