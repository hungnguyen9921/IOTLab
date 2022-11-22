// Import the functions you need from the SDKs you need
import firebase from 'firebase/compat/app';
// import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyC-2dSQ6CMSWyxie0sYE6zcADXWQ8unnmY",
    authDomain: "iotproject-a9462.firebaseapp.com",
    projectId: "iotproject-a9462",
    storageBucket: "iotproject-a9462.appspot.com",
    messagingSenderId: "1043148766075",
    appId: "1:1043148766075:web:499b34ac5f44e507351bde",
    measurementId: "G-8Q3Z5LS498"
};

// Initialize Firebase
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
} else {
    firebase.app(); // if already initialized, use that one
}
// const analytics = getAnalytics(app);

export default firebase;
