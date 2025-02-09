<template>
    <div class="dashboard-container">
      <h1>Dashboard</h1>
      <p>Formulários salvos.</p>
      <button @click="$router.push('/')">Voltar para o Início</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DashboardPage'
  };
  </script>
  
  <style scoped>
  .dashboard-container {
    padding: 20px;
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    min-height: 100vh;
    text-align: center;
  }
  
  h1 {
    color: #333;
  }
  
  button {
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 20px;
  }
  
  button:hover {
    background-color: #388e3c;
  }
  </style>
  