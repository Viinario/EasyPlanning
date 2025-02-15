<template>
    <div class="dashboard-container">
      <h1>Escolha um Formulário para Responder</h1>
  
      <ul>
        <li v-for="form in forms" :key="form.id">
          <strong>{{ form.title }}</strong> - {{ form.description }}
          <button @click="goToAnswerForm(form.id)">Responder</button>
        </li>
      </ul>
  
      <button @click="$router.push('/')">Voltar</button>
    </div>
  </template>
  
  <script>
  import ApiService from "@/services/api.js";
  
  export default {
    name: "RespondForm",
    data() {
      return {
        forms: [],
      };
    },
    async created() {
      await this.fetchForms();
    },
    methods: {
      async fetchForms() {
        try {
          const response = await ApiService.getForms();
          this.forms = response.data;
        } catch (error) {
          console.error("Erro ao buscar formulários:", error);
        }
      },
      goToAnswerForm(id) {
        this.$router.push(`/answer/${id}`);
      },
    },
  };
  </script>
  
  <style scoped>
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    margin-bottom: 10px;
  }
  button {
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-left: 10px;
  }
  button:hover {
    background-color: #388e3c;
  }
  </style>
  