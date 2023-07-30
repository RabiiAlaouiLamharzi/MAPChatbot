import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDKjo4DHpEUbaeTHDWTsZSIahAdVz2SfZA",
  authDomain: "chatbotmap-7cabf.firebaseapp.com",
  projectId: "chatbotmap-7cabf",
  storageBucket: "chatbotmap-7cabf.appspot.com",
  messagingSenderId: "510141607732",
  appId: "1:510141607732:web:98cac683ef9ad4d7783f61"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app)