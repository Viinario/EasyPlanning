<template>
  <div class="container">
    <header class="header">
      <div class="header-content">
        <h1>{{ projectName }}</h1>
        <h3 class="sprint-text">Sprint: {{ sprint }}</h3>
      </div>
      <div class="header-actions">
        <button @click="$router.push('/')" class="home-button">
          <img src="@/assets/home-icon.png" alt="Home" />
        </button>
        <button @click="undo" class="undo-button">
          <img src="@/assets/do-icon.png" alt="Desfazer" />
        </button>
      </div>
    </header>   
    
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
        <div class="scale-label">Intensidade</div>     
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
      projectName: "",
      sprint: "",
      formDescription: "",
      questions: [],
      answers: [],
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
        this.projectName = response.data.project_name;
        this.sprint = response.data.sprint;
        this.formDescription = response.data.description;
        this.questions = response.data.questions;
        this.answers = new Array(this.questions.length).fill(null);
      } catch (error) {
        console.error("Erro ao carregar formulário:", error);
      }
    },
    getScaleRange(max) {
      return Array.from({ length: max }, (_, i) => i + 1);
    },
    async submitAnswers() {
      try {
        const formId = this.$route.params.id;
        const payload = this.questions.map((question, index) => ({
          form: formId,
          question: question.id,
          answer: this.answers[index],
        }));
  
        await ApiService.submitAnswers(payload);
        alert("Respostas enviadas com sucesso!");
        this.$router.push("/respond");
      } catch (error) {
        console.error("Erro ao enviar respostas:", error);
      }
    },
    undo() {
      this.$router.go(-1);
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
  padding-top: 120px; /* espaço para o header */
}

.question-card {
  background-color: #DEE7E7;
  padding: 15px;
  border-radius: 10px;
  margin: 20px auto;
  text-align: left;
  width: 60%;
  max-width: 800px;
  box-shadow: -5px 5px 4px rgba(0, 0, 0, 0.2);
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

.scale-label {
  text-align: center;
  font-size: 14px;
  margin-top: 10px;
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
  background-color: #358600;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.button-submit:hover {
  transform: translateY(-3px) scale(1.1);    
  transition: background-color 0.3s, transform 0.2s;
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
  transform: translateY(-3px) scale(1.1);    
  transition: background-color 0.3s, transform 0.2s;
}

/* Header atualizado */
.header {
  background-color: #DEE7E7;
  width: 100%;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.header h1 {
  font-size: 24px;
  margin: 0;
  font-family: 'Istok Web', sans-serif;
}

.sprint-text {
  font-size: 18px;
  margin: 5px 0 0 0;
}

.header-actions {
  position: absolute;
  right: 20px;
  top: 50%;
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
