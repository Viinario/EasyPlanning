<template>
    <div>
        <h1>List of Answers</h1>
        <ul>
            <li v-for="answer in answers" :key="answer.id">
                <p>Answer: {{ answer.answer }}</p>
                <p>Submitted At: {{ new Date(answer.submitted_at).toLocaleString() }}</p>
                <p>Question ID: {{ answer.question }}</p>
            </li>
        </ul>
    </div>
</template>

<script>
import ApiService from "@/services/api.js";

export default {
    props: {
        id: {
            type: Number,
            required: true
        }
    },
    name: "ListFormAnswers",
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
                console.error('Error loading answers:', error);
            }
        }
    }
};
</script>

<style scoped>
h1 {
    font-size: 24px;
    margin-bottom: 20px;
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
</style>