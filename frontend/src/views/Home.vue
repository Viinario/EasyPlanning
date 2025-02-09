<template>
    <div class="home-container">
      <h1>EasyPlanning</h1>
      <div class="buttons">
        <button @click="goToForm">Acessar Formulário</button>
        <button @click="goToDashboard">Visualizar Dashboard</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage',
    methods: {
      goToForm() {
        this.$router.push('/form');
      },
      goToDashboard() {
        this.$router.push('/dashboard');
      }
    }
  };
  </script>
  
  <style scoped>
  .home-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #DEE7E7;
    font-family: Arial, sans-serif;
  }
  
  h1 {
    font-size: 48px;
    color: #2c3e50;
    margin-bottom: 30px;
  }
  
  .buttons button {
    background-color: #4caf50;
    color: white;
    padding: 15px 30px;
    margin: 10px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
  }
  
  .buttons button:hover {
    background-color: #388e3c;
  }
  </style>
  