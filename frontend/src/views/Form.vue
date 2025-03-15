<template>
  <div class="container">
    <header class="header">
      <h1>Cadastro de Formulários</h1>    
      <div class="header-actions">
        <button @click="undo" class="undo-button">
          <img src="@/assets/do-icon.png" alt="Desfazer" />
        </button>              
        <button class="save-button" @click="saveForm">Salvar</button>
      </div>
    </header>

    <div class="form-container">
      <div class="form-title-box">
        <input type="text" class="project-name" placeholder="Nome do projeto" v-model="projectName" />
        <select v-model="sprint" class="sprint-select">
          <option disabled value="">Selecione a sprint</option>
          <option v-for="n in 10" :key="n" :value="n">Sprint {{ n }}</option>
        </select>
        <textarea class="form-description" placeholder="Descrição do formulário" v-model="formDescription"></textarea>
      </div>

      <div v-for="(question, index) in questions" :key="index" class="question-card">
        <div class="question-header">
          <input type="text" placeholder="Pergunta sem título" v-model="question.title" />
          <div class="question-type-buttons">
            <button 
              :class="{ active: question.type === 'linear' }" 
              @click="setQuestionType(index, 'linear')"
            >Escala Linear</button>
            <button 
              :class="{ active: question.type === 'multiple' }" 
              @click="setQuestionType(index, 'multiple')"
            >Múltipla Escolha</button>
          </div>
        </div>

        <textarea class="texarea-box" placeholder="Descrição da pergunta" v-model="question.description"></textarea>
        <div class="question-separator"></div>        
        
        <div v-if="question.type === 'linear'" class="linear-scale">
          <div class="scale-line">
            <label v-for="value in 5" :key="value" class="scale-option">
              <input
                type="radio"
                :name="`question-${index}`"
                :value="value"
                v-model="question.intensity"
              />
              {{ value }}
            </label>
          </div>                       
          <div class="scale-labels">
            <label class="linear-label-left">Intensidade 1</label>
            <label class="linear-label-right">Intensidade 5</label>
          </div>
        </div>

        <div v-if="question.type === 'multiple'" class="multiple-choice">
          <div v-for="(option, optIndex) in question.options" :key="optIndex">
            <input type="radio" :name="`question-${index}`" class="option-radio" />
            <input
              type="text"
              placeholder="Descrição da alternativa"
              v-model="question.options[optIndex]"
              class="option-text"
            />
          </div>
          <button @click="addOption(index)" class="add-option-button">
            <img src="@/assets/icon-plus.png" alt="Adicionar Alternativa" />
          </button>
        </div>        
        <button @click="removeQuestion(index)" class="delete-question">
          <img src="@/assets/icon-trash.png" alt="Deletar Pergunta" />
        </button>
      </div>
      
      <button @click="addQuestion" class="add-question">
        <img src="@/assets/icon-plus.png" alt="Adicionar Pergunta" />
      </button>
    </div>
  </div>
</template>

<script>
  import ApiService from "@/services/api.js";

  export default {
    name: "FormPage",
    props: ["id"],
    data() {
      return {
        projectName: "",
        sprint: "",
        formDescription: "",
        questions: [],
      };
    },
    async created() {
      if (this.id) {
        await this.loadForm();
      }
    },
    methods: {
      async loadForm() {
        try {
          const response = await ApiService.getFormById(this.id);
          // Carrega os novos campos do formulário
          this.projectName = response.data.project_name;
          this.sprint = response.data.sprint;
          this.formDescription = response.data.description;
          this.questions = response.data.questions;
        } catch (error) {
          console.error("Erro ao carregar formulário:", error);
        }
      },
      changeQuestionType(index) {
        if (this.questions[index].type === "multiple") {
          this.questions[index].options = [""];
        } else {
          this.questions[index].options = [];
        }
      },
      addQuestion() {
        this.questions.push({
          title: "",
          description: "",
          type: "linear",
          options: [],
          intensity: 5
        });
      },
      removeQuestion(index) {
        this.questions.splice(index, 1);
      },
      addOption(index) {
        this.questions[index].options.push("");
      },
      async saveForm() {
        try {            
          if (!this.projectName.trim()) {
            alert("O nome do projeto é obrigatório.");
            return;
          }
          if (!this.sprint) {
            alert("A sprint é obrigatória.");
            return;
          }
          if (!this.formDescription.trim()) {
            alert("A descrição do formulário é obrigatória.");
            return;
          }            
          if (this.questions.length === 0) {
            alert("Adicione pelo menos uma pergunta antes de salvar.");
            return;
          }            
          for (const [index, question] of this.questions.entries()) {
            if (!question.title.trim()) {
              alert(`A pergunta ${index + 1} precisa de um título.`);
              return;
            }
            if (!question.type) {
              alert(`A pergunta ${index + 1} precisa de um tipo definido.`);
              return;
            }             
            if (question.type === "multiple") {
              const validOptions = question.options.filter(opt => opt.trim() !== "");
              if (validOptions.length === 0) {
                alert(`A pergunta ${index + 1} de múltipla escolha precisa ter pelo menos uma opção.`);
                return;
              }
            }                
            if (question.type === "linear" && (question.intensity === null || question.intensity <= 0)) {
              alert(`A pergunta ${index + 1} de escala linear precisa ter uma intensidade válida.`);
              return;
            }
          }            
          const formData = {
            project_name: this.projectName.trim(),
            sprint: this.sprint,
            description: this.formDescription.trim(),
            questions: this.questions.map(q => ({
              title: q.title.trim(),
              description: q.description.trim(),
              type: q.type,
              options: q.type === "multiple" ? q.options.filter(opt => opt.trim() !== "") : [],
              intensity: q.type === "linear" ? q.intensity : null
            })),
          };

          console.log("Enviando formulário para API:", formData);
         
          const response = this.id
              ? await ApiService.updateForm(this.id, formData)
              : await ApiService.createForm(formData);

          alert("Formulário salvo com sucesso!");
          console.log("Resposta da API:", response.data);

          this.$router.push("/dashboard");
        } catch (error) {
          console.error("Erro ao salvar formulário:", error);
          console.error("Detalhes do erro:", error.response?.data);
          alert(`Erro ao salvar: ${error.response?.data?.message || "Erro desconhecido"}`);
        }
      },
      undo() {
        this.$router.go(-1);
      },   
      toggleQuestionType(index) {
        this.questions[index].type = this.questions[index].type === "linear" ? "multiple" : "linear";
      },
      setQuestionType(index, type) {
        this.questions[index].type = type;
      },
    }    
  };
</script>

<style scoped>
  /* (Mantém os estilos já existentes – opcionalmente pode-se ajustar o estilo do .sprint-select) */
  @import url('https://fonts.googleapis.com/css2?family=Istok+Web&display=swap');

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
    align-items: center;
    position: absolute;
    right: 70px;
    bottom: 16px;    
  }

  .save-button {
    background-color: #358600;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s;
    white-space: nowrap;
    margin-left: 20px;    
  }

  .save-button:hover {
      transform: scale(1.05);
      transition: background-color 0.3s, transform 0.2s;
    }

  .form-container {
    border-radius: 10px;
    margin-top: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .form-title-box {
    background: #DEE7E7;
    padding: 5px;
    border-radius: 10px;
    box-shadow: -5px 5px 4px 0px rgba(0, 0, 0, 0.2);
    width: 100%;
    max-width: 1000px;
    display: flex;
    flex-direction: column;
    gap: 2px;  
    font-family: 'Istok Web', sans-serif;
  }

  .project-name, .sprint-select {
    width: 73%; 
    padding: 0px 10px;
    border: none;
    background-color: #DEE7E7;    
  }

  .form-description {
    font-size: 14px;
    margin-left: 30px;
  }

  .form-title-box input::placeholder,
  .form-title-box textarea::placeholder {
    color: black;
  }

  .question-card {
    background-color: #DEE7E7;
    padding: 15px;
    border-radius: 10px;
    margin-top: 40px;
    width: 100%;
    max-width: 850px;
    box-shadow: -5px 5px 4px 0px rgba(0, 0, 0, 0.2);  
    position: relative;  
  }

  .question-card input,
  .question-card textarea {
    background-color: #DEE7E7;  
    border: none;
    font-family: 'Istok Web', sans-serif;
    width: 70%;
  }

  .question-card input::placeholder {
    color: black;
    font-family: 'Istok Web', sans-serif;
    font-size: 17px;
  }

  .question-card textarea::placeholder {
    color: black;
    font-family: 'Istok Web', sans-serif;
    font-size: 13px;
  }

  .question-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;    
  }

  .question-header select {
    background: #D9D9D9;  
  }

  .question-separator {
    height: 3px;                  
    background-color: #BBC8C8;
    width: 100%;               
  }

  .linear-scale {
    align-items: center;
    justify-content: space-between;
    margin: 30px 0;
  }

  .linear-label-left,
  .linear-label-right {
    position: absolute;  
    transform: translateY(5px);
    font-size: 12px;
    font-family: 'Istok Web', sans-serif;
    color: black;
    white-space: nowrap;
  }

  .linear-label-left {
    left: 115px;
    bottom: 30px;
    text-align: left;
  }

  .linear-label-right {
    right: 115px;
    bottom: 30px;
    text-align: right;
  }

  @media (max-width: 600px) {
    .linear-label-left {
      left: 70px;
    }
    .linear-label-right {
      right: 65px;
    }
  }

  .scale-line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    width: 70%;
    padding: 0px 0;
    margin: 0 auto;  
  }

  .scale-line::before {
    content: "";  
    position: absolute;
    top: 48%;
    left: 0%;
    right: 0%;
    height: 2.5px;
    background-color: #BBC8C8;  
    z-index: 0;  
  }

  .scale-line input[type="radio"] {  
    appearance: none;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #5E4AE3;
    cursor: pointer;
    position: relative;  
    z-index: 1;
    margin: 0;
    transition: all 0.3s ease;
    flex-shrink: 0;
  }

  .scale-line input[type="radio"]:checked {
    background-color: black;
    transform: scale(1.2);
  }
  
  .scale-option {
    font-size: 0;
  }

  .multiple-choice {
    margin-top: 10px;
  }

  .delete-question {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 8px 12px;
    margin-top: 10px;
    cursor: pointer;
    border-radius: 5px;
    transition: background 0.3s;
  }

  .add-option-button,
  .add-question {
    background-color: #4caf50;
    border: none;
    padding: 8px;
    margin-top: 10px;
    cursor: pointer;
    border-radius: 50%;
    transition: background 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 25px;
    height: 25px;  
  }

  .add-option-button {
    background-color: #DEE7E7;  
    width: 5px;
    height: 5px;
    padding-top: 30px;  
  }

  .add-question img {
    width: 25px;
    height: 25px;
    box-shadow: 5px 5px 4px 0px rgba(0, 0, 0, 0.3);  
    border-radius: 100%;
  }

  .add-option-button img {
    width: 20px;
    height: 20px;
    box-shadow: 5px 5px 4px 0px rgba(0, 0, 0, 0.2);  
    border-radius: 50%;  
  }

  .add-option-button:hover,
  .add-question:hover {
    transform: translateY(-3px) scale(1.1);
    transition: background-color 0.3s, transform 0.2s;
  }

  .delete-question {
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 60%;
    padding: 8px;
    position: absolute;
    bottom: 5px;
    right: 5px;
  }

  .delete-question img {
    width: 20px;
    height: 22px;
  }

  .delete-question:hover {
    background-color: #f09e9e;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    transform: translateY(-3px) scale(1.1);
  }

  .undo-button {
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

  .undo-button img {
    width: 24px;
    height: 24px;
  }

  .undo-button:hover {
    transform: translateY(-3px) scale(1.1);
    background-color: rgba(#DEE7E7, 67, 67, 0.1);
  }

  .multiple-choice {
    flex-direction: column;
    align-items: flex-start;
    margin-top: 10px;
  }

  .option-radio {
    cursor: pointer;
    position: absolute;
    left: -290px;
    margin-right: 10px;
  }

  .option-text {
    border: none;
    background-color: #DEE7E7;
    font-family: 'Istok Web', sans-serif;  
    margin-left: -200px;
    width: 100%;
  }

  .texarea-box{    
    font-family: 'Istok Web', sans-serif;    
    margin-right: 250px;
    width: 100%;  
    min-height: 5px;         
    max-height: 20px;        
  }

  .question-type-buttons {
    display: flex;
    gap: 10px;
  }

  .question-type-buttons button {
    padding: 8px 12px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background: #ddd;
    font-weight: bold;
    transition: background 0.3s;
  }

  .question-type-buttons button.active {
    background: #358600;
    color: white;
  }

  .question-type-buttons button:hover {
    background: #2d6b00;
    color: white;
  }
</style>
