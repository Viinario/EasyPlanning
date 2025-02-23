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
    padding-top: 200px;
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

  .undo-button {
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
    width: 5px;
    height: 8px;
  }

  .home-button {    
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;    
    transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;        
  }

  .undo-button img,
  .home-button img {
    width: 24px;
    height: 24px;
  }
  
  .undo-button:hover,
  .home-button:hover {
    transform: translateY(-3px) scale(1.1);
    background-color: rgba(#DEE7E7, 67, 67, 0.1);
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

  .new-form {    
    transform: scale(1.05);
    transition: background-color 0.3s, transform 0.2s;
    margin-top: 100px;
  }

  .new-form:hover {    
    transform: scale(1.05);
    transition: background-color 0.3s, transform 0.2s;
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
  