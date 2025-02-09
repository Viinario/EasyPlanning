<template>
  <div class="container">
    <header class="header">
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
      <button class="save-button" @click="saveForm">Salvar</button>
      </div>
    </header>

    <div class="form-container">
      <div class="form-title-box">
        <input type="text" class="form-title" placeholder="Formulário sem título" v-model="formTitle" />
        <textarea class="form-description" placeholder="Descrição do formulário" v-model="formDescription"></textarea>
      </div>

      <div v-for="(question, index) in questions" :key="index" class="question-card">
        <div class="question-header">
          <input type="text" placeholder="Pergunta sem título" v-model="question.title" />
          <select v-model="question.type" @change="changeQuestionType(index)">
            <option value="linear">Escala Linear</option>
            <option value="multiple">Múltipla Escolha</option>
          </select>
        </div>

        <textarea placeholder="Descrição da pergunta" v-model="question.description"></textarea>
        <div class="question-separator"></div>
        
        <div v-if="question.type === 'linear'" class="linear-scale">                      
          <div class="scale-line">
            <input type="radio" :name="`question-${index}`" value="1" v-model="question.selectedOption" />
            <input type="radio" :name="`question-${index}`" value="2" v-model="question.selectedOption" />
            <input type="radio" :name="`question-${index}`" value="3" v-model="question.selectedOption" />
            <input type="radio" :name="`question-${index}`" value="4" v-model="question.selectedOption" />
            <input type="radio" :name="`question-${index}`" value="5" v-model="question.selectedOption" />
          </div>                        
          <label class="linear-label-left">Intensidade 1</label>
          <label class="linear-label-right">Intensidade 5</label>
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
        <button @click="removeQuestion" class="delete-question">
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
export default {
  name: 'FormPage',
  data() {
    return {
      formTitle: '',
      formDescription: '',
      questions: [
        {
          title: '',
          description: '',
          type: 'linear',
          options: ['']
        }
      ]
    };
  },
  methods: {
    addQuestion() {
      this.questions.push({
        title: '',
        description: '',
        type: 'linear',
        options: ['']
      });
    },
    removeQuestion(index) {
      this.questions.splice(index, 1);
    },
    addOption(index) {
      this.questions[index].options.push('');
    },
    changeQuestionType(index) {
      if (this.questions[index].type === 'multiple') {
        this.questions[index].options = [''];
      }
    },
    undo() {
      console.log('Desfazer ação');
    },
    redo() {
      console.log('Refazer ação');
    },
    toggleVisibility() {
      console.log('Alternar visualização');
    },
    saveForm() {
      console.log('Formulário salvo:', this.formTitle, this.questions);
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Istok+Web&display=swap');

.container {
  background-color: #BBC8C8;
  min-height: 100vh;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  justify-content: flex-end;
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.icon-button:hover {
  transform: scale(1.1);
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
  margin-right: 50px;
}

.save-button:hover {
  background-color: rgb(150, 206, 153);
}

.form-container {
  /*background: #fff;*/
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

.form-title-box input {
  width: 73%; 
}

.form-title-box textarea {
  resize: none;
  overflow-y: auto;
  max-height: 150px; 
  font-family: 'Istok Web', sans-serif;
  padding: 10px;
  border: none;
  background-color: #DEE7E7;
  height: 22px;
  width: 70%; 
}

.form-title-box input::placeholder {
  color: black;
}

.form-title-box textarea::placeholder {
  color: black;
}

.form-title-box input {
  padding: 0px 10px;
  border: none;
  background-color: #DEE7E7;    
}

.form-title {
  font-size: 40px;
  font-weight: 400;
  color: black;
}

.form-description {
  font-size: 14px;
  margin-left: 30px;
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

.question-card input {
  background-color: #DEE7E7;  
  border: none;  
  font-family: 'Istok Web', sans-serif;
  width: 70% 
}

.question-card textarea {
  background-color: #DEE7E7;  
  border: none;
  flex: 0.7;
  resize: none;
  overflow-y: auto;
  width: 70% 
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
  bottom: 50px;
  text-align: left;
}

.linear-label-right {
  right: 115px;
  bottom: 50px;
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
  padding: 20px 0;
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
  transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
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
  margin-left: 30px;
  width: 100%;
}


@media (max-width: 600px) {
  .option-radio {
    left: -215px;
  }  
}

</style>