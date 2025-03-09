<template>
  <div class="container">
    <header class="header">
      <div v-if="answers.length">
        <h1>{{ answers[0].form_title }}</h1>
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

    <!-- Aggregated Info Section -->
    <div class="aggregated-info" v-if="aggregatedInfo.length">
      <h2>Informações Agregadas</h2>
      <div v-for="(item) in aggregatedInfo" :key="item.question_id" class="aggregate-item">
        <p><strong>Questão:</strong> {{ item.question_description }}</p>
        <p v-if="item.question_type === 'linear'">
          Média: {{ item.mean }}
        </p>
        <p v-else-if="item.question_type === 'multiple'">
          Opção mais escolhida: {{ item.mostChosen }}
        </p>
      </div>
    </div>

    <div>
      <ul>
        <li v-for="(answer, index) in answers" :key="answer.id">
          <p><strong>Questão:</strong> {{ answer.question_description }}</p>
          
          <div v-if="answer.question_type === 'linear'" class="linear-scale">
            <div class="scale-line">
              <label 
                v-for="value in getScaleRange(answer.intensity)" 
                :key="value" 
                class="scale-option"
              >
                <input
                  type="radio"
                  :name="`question-${index}`"
                  :value="value"
                  v-model="answer.answer"
                  disabled
                />
                {{ value }}
              </label>
            </div>
            <div class="scale-label">Intensidade</div>     
          </div>
          
          <div v-else-if="answer.question_type === 'multiple'" class="multiple-choice">
            <div v-for="(option, optIndex) in answer.multiple_options" :key="optIndex">
              <input
                type="radio"
                :name="`question-${index}`"
                :value="option"
                :checked="option === answer.answer"
                disabled
              />
              <label>{{ option }}</label>
            </div>
          </div>

          <p><strong>Submetido em:</strong> {{ new Date(answer.submitted_at).toLocaleString() }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import ApiService from "@/services/api.js";

export default {
  name: "ListFormAnswers",
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      answers: []
    };
  },
  created() {
    this.loadAnswers();
  },
  methods: {
    async loadAnswers() {
      try {
        const response = await ApiService.getAnswers(this.id);
        this.answers = response.data;
      } catch (error) {
        console.error("Error loading answers:", error);
      }
    },
    getScaleRange(max) {
      // If intensity is not defined, default to 5
      const intensity = max || 5;
      return Array.from({ length: intensity }, (_, i) => i + 1);
    },
    undo() {
      this.$router.go(-1);
    }
  },
  computed: {
    aggregatedInfo() {
      // Group answers by question id
      const groups = {};
      this.answers.forEach(answer => {
        const qId = answer.question;
        if (!groups[qId]) {
          groups[qId] = {
            question_id: qId,
            question_description: answer.question_description,
            question_type: answer.question_type,
            intensity: answer.intensity, // for linear questions
            answers: []
          };
        }
        groups[qId].answers.push(answer.answer);
      });
      // Compute aggregated value per group
      return Object.values(groups).map(group => {
        if (group.question_type === "linear") {
          // Calculate the mean
          const sum = group.answers.reduce((acc, val) => acc + Number(val), 0);
          const mean = sum / group.answers.length;
          return { ...group, mean: mean.toFixed(2) };
        } else if (group.question_type === "multiple") {
          // Count frequency for each option
          const frequency = {};
          group.answers.forEach(ans => {
            frequency[ans] = (frequency[ans] || 0) + 1;
          });
          // Get the most chosen option
          const mostChosen = Object.keys(frequency).reduce((a, b) =>
            frequency[a] >= frequency[b] ? a : b
          );
          return { ...group, mostChosen };
        }
        return group;
      });
    }
  }
};
</script>

<style scoped>
h1 {
  font-size: 24px;
  margin-bottom: 20px;
}
h2 {
  font-size: 20px;
  margin-bottom: 10px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

/* Styles for the linear scale widget */
.linear-scale {
  margin: 10px 0;
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

/* Styles for multiple-choice widget */
.multiple-choice {
  margin: 10px 0;
}
.multiple-choice div {
  margin-bottom: 5px;
}

/* Container and header styles */
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
.header div h1 {
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
.home-button,
.undo-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
}
.home-button img,
.undo-button img {
  width: 24px;
  height: 24px;
}
.undo-button:hover,
.home-button:hover {
  transform: translateY(-3px) scale(1.1);
  background-color: rgba(#DEE7E7, 67, 67, 0.1);
}

/* Aggregated info styles */
.aggregated-info {
  margin: 120px 0 20px; /* space below header */
  text-align: left;
  padding: 0 20px;
}
.aggregate-item {
  margin-bottom: 15px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}
</style>
