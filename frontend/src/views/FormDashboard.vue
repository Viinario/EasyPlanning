<template>
  <div class="container">
    <header class="header">
      <h1>Dashboard dos formulários</h1>
      <div class="header-actions">
        <button @click="$router.push('/')" class="home-button">
          <img src="@/assets/home-icon.png" alt="Home" />
        </button>
        <button @click="undo" class="undo-button">
          <img src="@/assets/do-icon.png" alt="Desfazer" />
        </button>
      </div>
    </header>
    
    <!-- Área de Filtros -->
    <div class="filter-container">
      <input
        type="text"
        v-model="projectQuery"
        placeholder="Buscar por nome do projeto"
        class="filter-input"
      />
      
      <select v-model="sprintQuery" class="filter-input">
        <option value="">Todas as sprints</option>
        <option v-for="n in 10" :key="n" :value="n">Sprint {{ n }}</option>
      </select>
      
      <div class="date-range">
        <label>
          Data Inicial:
          <input type="date" v-model="startDate" class="filter-input" />
        </label>
        <label>
          Data Final:
          <input type="date" v-model="endDate" class="filter-input" />
        </label>
      </div>
    </div>

    <ul>
      <li v-for="form in filteredForms" :key="form.id">
        <strong>
          {{ form.project_name }} - Sprint: {{ form.sprint }} - {{ formatDate(form.created_at) }}
        </strong>
        <br />
        {{ form.description }}
        <div class="buttons-group">
          <button class="edit-button" @click="goToEditForm(form.id)">Editar</button>
          <button class="delete-button" @click="deleteForm(form.id)">Excluir</button>
          <button class="edit-button" @click="goToAnswers(form.id)">Visualizar Respostas</button>
        </div>
      </li>
    </ul>

    <button class="new-form" @click="$router.push('/form')">Criar Novo Formulário</button>
  </div>
</template>

<script>
import ApiService from "@/services/api.js";

export default {
  name: "DashboardPage",
  data() {
    return {
      forms: [],
      projectQuery: "",
      sprintQuery: "",
      startDate: "",
      endDate: "",
    };
  },
  async created() {
    await this.fetchForms();
  },
  computed: {
    filteredForms() {
      return this.forms.filter(form => {
        const createdDate = new Date(form.created_at);
        let matchesProject = true;
        let matchesSprint = true;
        let matchesDate = true;

        // Filtro por nome do projeto
        if (this.projectQuery) {
          matchesProject = form.project_name
            .toLowerCase()
            .includes(this.projectQuery.toLowerCase());
        }
        // Filtro por sprint
        if (this.sprintQuery) {
          matchesSprint = String(form.sprint) === String(this.sprintQuery);
        }
        // Filtro por data: se definido, verifica se a data de criação está no intervalo
        if (this.startDate) {
          const start = new Date(this.startDate);
          matchesDate = createdDate >= start;
        }
        if (matchesDate && this.endDate) {
          const end = new Date(this.endDate);
          matchesDate = createdDate <= end;
        }
        return matchesProject && matchesSprint && matchesDate;
      });
    }
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
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString();
    },
    goToEditForm(id) {
      this.$router.push(`/form/${id}`);
    },
    goToAnswers(id) {
      this.$router.push(`/formAnswers/${id}`);
    },
    async deleteForm(id) {
      if (confirm("Tem certeza que deseja excluir este formulário?")) {
        try {
          await ApiService.deleteForm(id);
          this.fetchForms();
        } catch (error) {
          console.error("Erro ao excluir formulário:", error);
        }
      }
    },
    undo() {
      this.$router.go(-1);
    }
  }
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
  top: 35%;
  left: 0;
  transform: translateY(-50%);
}

.filter-container {
  margin-top: 80px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.filter-input {
  padding: 8px;
  width: 80%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.date-range {
  display: flex;
  gap: 10px;
  align-items: center;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  padding-top: 20px;
}

li {
  padding: 10px 0;
  border-bottom: 1px solid #ccc;
  margin-bottom: 10px;
}

.buttons-group {
  margin-top: 10px;
}

button {
  background-color: #358600;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

button + button {
  margin-left: 10px;
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

.delete-button:hover {
  background-color: #c9302c;
  transform: scale(1.05);
}

.edit-button:hover {
  transform: scale(1.05);
  transition: background-color 0.3s, transform 0.2s;
}

.new-form {
  margin-top: 20px;
  transition: transform 0.2s;
}

.new-form:hover {
  transform: scale(1.05);
}

@media (max-width: 800px) {
  .header-actions {
    width: 85%;
  }
}

@media (max-width: 1000px) {
  .header-actions {
    width: 90%;
  }
}

@media (max-width: 1200px) {
  .header-actions {
    width: 90%;
  }
}

@media (max-width: 1500px) {
  .header-actions {
    width: 90%;
  }
}
</style>
