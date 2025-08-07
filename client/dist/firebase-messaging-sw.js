importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyA2vAljG4L6b2ZK_7utT2y20j258mvXFiE",
  authDomain: "antonella-d1744.firebaseapp.com",
  projectId: "antonella-d1744",
  storageBucket: "antonella-d1744.firebasestorage.app",
  messagingSenderId: "631746154431",
  appId: "1:631746154431:web:dd04cf49a20a8085705b0a",
  measurementId: "G-CTLPZ5B6PY"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});