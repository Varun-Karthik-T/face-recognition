// registerForPushNotificationsAsync.js

import * as Notifications from 'expo-notifications';

const registerForPushNotificationsAsync = async () => {
  // Request permissions for notifications
  const { status: existingStatus } = await Notifications.getPermissionsAsync();

  // Only ask if permissions have not already been granted
  let finalStatus = existingStatus;
  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  // If permissions are not granted, return null
  if (finalStatus !== 'granted') {
    alert('Notification permissions are not granted!');
    return null;
  }

  // Get the push token
  const token = (await Notifications.getExpoPushTokenAsync()).data;
  console.log(token); // You can log the token or send it to your server
  return token;
};

export default registerForPushNotificationsAsync;
