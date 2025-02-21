<template>
  <div class="dashboard-container">
    <header class="header">
      <h1>Dashboard</h1>    
      <div class="header-actions">
      <button @click="undo" class="undo-button">
        <img src="@/assets/do-icon.png" alt="Desfazer" />
      </button>        
      <button @click="redo" class="redo-button">
        <img src="@/assets/do-icon.png" alt="Refazer" />
      </button>        
      <button @click="toggleVisibility" class="toggle-visibility-button">
        <img src="@/assets/icon-toggle.png" alt="Visualizar" />
      </button>
      </div>
    </header>

    <ul>
      <li v-for="form in forms" :key="form.id">
        <strong>{{ form.title }}</strong> - {{ form.description }}
        <button class="edit-button" @click="goToEditForm(form.id)">Editar</button>
        <button class="delete-button" @click="deleteForm(form.id)">Excluir</button>
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
          forms: []
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
        goToEditForm(id) {
          this.$router.push(`/form/${id}`);
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
        },
        redo() {
          this.$router.go(1);
        },
        toggleVisibility() {
          console.log("Alternar visualização");
        },
      }
    };
  </script>
  
  <style scoped> 
  .dashboard-container {
    padding: 20px;
    font-family: Arial, sans-serif;
    background-color: #BBC8C8;
    min-height: 100vh;
    text-align: center;
  }
  
  h1 {
    color: #333;
    
  }
  
  button {
    background-color: #358600;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 20px;
  }
  
  button + button {
    margin-left: 10px;
  }

  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    padding-top: 100px;
  }

  li {
    padding: 10px 0;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #DEE7E7;
    height: 43px;
    width: 100%;
    padding: 10px 20px;
    border-radius: 0;
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
  }

  .header-actions {
    display: flex;
    align-items: center;
    position: absolute;
    right: 148px;
    bottom: 16px;    
  }

  .undo-button,
  .redo-button,
  .toggle-visibility-button{
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 15px;
    transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
    border-radius: 50%;
    width: 5px;
    height: 5px;
  }

  .undo-button img,
  .redo-button img {
    width: 24px;
    height: 24px;
  }

  .toggle-visibility-button img {
    width: 32px;
    height: 32px;
    padding-top: 5px;  
  }

  .undo-button:hover,
  .redo-button:hover, 
  .toggle-visibility-button:hover {
    transform: translateY(-3px) scale(1.1);
    background-color: rgba(#DEE7E7, 67, 67, 0.1);}

  .redo-button img {
    transform: scaleX(-1);
  }

  .delete-button {
    background-color: #358600;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
  }

  .delete-button:hover {
    background-color: #c9302c;
    transform: scale(1.05);
  }

  .edit-button:hover {    
    transform: scale(1.05);
    transition: background-color 0.3s, transform 0.2s;
  }

  .new-form:hover {    
    transform: scale(1.05);
    transition: background-color 0.3s, transform 0.2s;
  }

</style>
  