require('dotenv').config();

const URL = "https://testes.codefolio.com.br";
const FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]";
const FIREBASE_VALUE = `
{
  "apiKey": "AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg",
  "appName": "[DEFAULT]",
  "createdAt": "1761527447694",
  "displayName": "Sidnei Correia Junior",
  "email": "sidneicorreia.aluno@unipampa.edu.br",
  "emailVerified": true,
  "isAnonymous": false,
  "lastLoginAt": "1761529757560",
  "phoneNumber": null,
  "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocJFqkk-GXYNmv4ROq0dK1kNqLtmN5PVzPjtCHMOyhLRxmJGKCE=s96-c",
  "providerData": [
    {
      "providerId": "google.com",
      "uid": "114168160847001878634",
      "displayName": "Sidnei Correia Junior",
      "email": "sidneicorreia.aluno@unipampa.edu.br",
      "phoneNumber": null,
      "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocJFqkk-GXYNmv4ROq0dK1kNqLtmN5PVzPjtCHMOyhLRxmJGKCE=s96-c"
    }
  ],
  "stsTokenManager": {
    "accessToken": "${process.env.accessTokentoken}",
    "expirationTime": ${process.env.expirationTime},
    "refreshToken": "${process.env.refreshToken}",
    "tenantId": null
  },
  "uid": "oSo4dFAJfoPU5JuUJwqNkaZGYRn1",
  "_redirectEventId": null
}

`;


module.exports = {URL, FIREBASE_KEY, FIREBASE_VALUE};