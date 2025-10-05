<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const title = ref('')
const description = ref('')
const router = useRouter()
const handleSubmit = async () => {
  const res = await fetch('http://localhost:8000/products', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title: title.value, description: description.value }),
  })

  if (res.ok) {
    await router.push('/')
  } else {
    alert('Error creating product')
  }
}
</script>

<template>
  <div class="container">
    <h1>Add Product</h1>
    <form @submit.prevent="handleSubmit">
      <input v-model="title" type="text" placeholder="Title" required />
      <textarea v-model="description" placeholder="Description" required></textarea>
      <button type="submit">Add</button>
    </form>
    <NuxtLink to="/" class="link">← Back to List</NuxtLink>
  </div>
</template>

<style scoped>
.container {
  max-width: 700px;
  margin: 40px auto;
  padding: 20px;
}
form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
input,
textarea {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
button {
  padding: 10px;
  background-color: #0077ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background-color: #005fd1;
}
.link {
  margin-top: 20px;
  display: inline-block;
  color: blue;
  text-decoration: underline;
}
</style>