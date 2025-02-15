<template>
    <div class="container">
      <h1>{{ formTitle }}</h1>
      <p>{{ formDescription }}</p>
  
      <div v-for="(question, index) in questions" :key="index" class="question-card">
        <h3>{{ question.title }}</h3>
        <p>{{ question.description }}</p>
  
        <!-- Resposta de Escala Linear -->
        <div v-if="question.type === 'linear'" class="linear-scale">
          <div class="scale-line">
            <label v-for="value in getScaleRange(question.intensity)" :key="value" class="scale-option">
              <input
                type="radio"
                :name="`question-${index}`"
                :value="value"
                v-model="answers[index]"
              />
              {{ value }}
            </label>
          </div>         
        </div>
  
        <!-- Resposta de Múltipla Escolha -->
        <div v-if="question.type === 'multiple'" class="multiple-choice">
          <div v-for="(option, optIndex) in question.options" :key="optIndex">
            <input
              type="radio"
              :name="`question-${index}`"
              :value="option"
              v-model="answers[index]"
            />
            <label>{{ option }}</label>
          </div>
        </div>
      </div>
  
      <div class="buttons-container">
        <button class="button-submit" @click="submitAnswers">Enviar Respostas</button>
        <button class="button-cancel" @click="$router.push('/respond')">Cancelar</button>
      </div>
    </div>
  </template>
  
  <script>
  import ApiService from "@/services/api.js";
  
  export default {
    name: "AnswerForm",
    data() {
      return {
        formTitle: "",
        formDescription: "",
        questions: [],
        answers: [], // Armazena as respostas do usuário
      };
    },
    async created() {
      const formId = this.$route.params.id;
      if (formId) {
        await this.loadForm(formId);
      }
    },
    methods: {
      async loadForm(id) {
        try {
          const response = await ApiService.getFormById(id);
          this.formTitle = response.data.title;
          this.formDescription = response.data.description;
          this.questions = response.data.questions;
          this.answers = new Array(this.questions.length).fill(null);
        } catch (error) {
          console.error("Erro ao carregar formulário:", error);
        }
      },
      getScaleRange(max) {
        return Array.from({ length: max + 1 }, (_, i) => i);
      },
      async submitAnswers() {
        try {
          const responseData = this.questions.map((q, index) => ({
            question_id: q.id,
            answer: this.answers[index],
            correct: q.type === "multiple" ? q.correct_answer === this.answers[index] : null,
          }));
  
          await ApiService.submitAnswers(responseData);
          alert("Respostas enviadas com sucesso!");
          this.$router.push("/respond");
        } catch (error) {
          console.error("Erro ao enviar respostas:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    background-color: #BBC8C8;
    min-height: 100vh;
    padding: 20px;
    font-family: Arial, sans-serif;
    text-align: center;
  }
  
  .question-card {
    background-color: #DEE7E7;
    padding: 15px;
    border-radius: 10px;
    margin-top: 20px;
    text-align: left;
  }
  
  .linear-scale {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .scale-line {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 10px;
  }
  
  .scale-option {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .scale-labels {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 5px;
  }
  
  .multiple-choice {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .buttons-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
  }
  
  .button-submit {
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .button-submit:hover {
    background-color: #388e3c;
  }
  
  .button-cancel {
    background-color: #d9534f;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .button-cancel:hover {
    background-color: #c9302c;
  }
  </style>
  