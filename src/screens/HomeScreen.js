import React, { useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { FAB } from 'react-native-paper';

const HomeScreen = ({ navigation }) => {
  const [state, setState] = useState({ open: false });

  const onStateChange = ({ open }) => setState({ open });
  const { open } = state;

  return (
    <View style={styles.container}>
      <Text>메인메뉴 화면</Text>
      <FAB.Group
        open={open}
        icon={open ? 'close' : 'plus'}
        actions={[
          { icon: 'cog', label: '설정', onPress: () => console.log('설정 Pressed') },
          { icon: 'pencil', label: '수동 입력', onPress: () => console.log('수동 입력 Pressed') },
          { icon: 'receipt', label: '영수증', onPress: () => console.log('영수증 Pressed') },
          { icon: 'barcode', label: '바코드', onPress: () => console.log('바코드 Pressed') },
        ]}
        onStateChange={onStateChange}
        onPress={() => {
          if (open) {
            // FAB를 닫음
          }
        }}
        fabStyle={styles.fab}
        color="white"
      />
    </View>
  );
};

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

export default HomeScreen;