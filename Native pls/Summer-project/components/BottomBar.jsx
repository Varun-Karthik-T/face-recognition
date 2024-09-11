import { useState } from 'react';
import { BottomNavigation, Text } from 'react-native-paper';
import Home from './Home';
import History from './History';
import People from './People';

const HomeRoute = () => <Home />;

const HistoryRoute = () => <History />;

const PeopleRoute = () => <People />;

const BottomNavBar = () => {
  const [index, setIndex] = useState(0);
  const [routes] = useState([
    { key: 'home', title: 'Favorites', focusedIcon: 'heart', unfocusedIcon: 'heart-outline'},
    { key: 'history', title: 'Albums', focusedIcon: 'album' },
    { key: 'people', title: 'Recents', focusedIcon: 'history' },
  ]);

  const renderScene = BottomNavigation.SceneMap({
    home: HomeRoute,
    history: HistoryRoute,
    people: PeopleRoute,
  });

  return (
    <BottomNavigation
      navigationState={{ index, routes }}
      onIndexChange={setIndex}
      renderScene={renderScene}
    />
  );
};

export default BottomNavBar;