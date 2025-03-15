<template>
  <div class="container">
    <header class="header">
      <h1>Escolha um formulário para responder</h1>
      <div class="header-actions">
        <button @click="$router.push('/')" class="home-button">
          <img src="@/assets/home-icon.png" alt="Home" />
        </button>
        <button @click="undo" class="undo-button">
          <img src="@/assets/do-icon.png" alt="Desfazer" />
        </button>              
      </div>
    </header>
    <ul>
      <li v-for="form in forms" :key="form.id">
        <div class="form-info">
          <strong>{{ form.project_name }}</strong> - Sprint: {{ form.sprint }} - {{ form.description }}
        </div>
        <div class="responder-section">
          <a :href="generateAccessLink(form)" target="_blank" class="access-link">
            Acessar formulário
          </a>
          <button @click="goToAnswerForm(form.id)">Responder</button>
        </div>
      </li>
    </ul>       
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
    generateAccessLink(form) {
      // Gera um link completo com base no domínio atual e no ID do formulário.
      return window.location.origin + `/answer/${form.id}`;
    },
    goToAnswerForm(id) {
      this.$router.push(`/answer/${id}`);
    },
    undo() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #BBC8C8;
  min-height: 100vh;
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  padding-top: 200px;
}

li {
  margin-bottom: 20px;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.form-info {
  margin-bottom: 10px;
}

.responder-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.access-link {
  font-weight: bold;
  color: #358600;
  text-decoration: none;
  background-color: #f1f1f1;
  padding: 5px 8px;
  border-radius: 5px;
  font-size: 14px;
}

button {
  background-color: #358600;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

button:hover {
  transform: scale(1.05);
  transition: background-color 0.3s, transform 0.2s;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #DEE7E7;
  height: 43px;
  width: 100%;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header h1 {
  flex-grow: 1;
  text-align: center;
  margin: 0;
  font-size: 24px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Istok Web', sans-serif;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 96%;
  padding: 0 20px;
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
}

.home-button,
.undo-button {
  background: none;
  border: none;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s;
}

.home-button img,
.undo-button img {
  width: 24px;
  height: 24px;
}

.undo-button:hover,
.home-button:hover {
  transform: translateY(-3px) scale(1.1);
  background-color: rgba(222, 231, 231, 0.1);
}
</style>
