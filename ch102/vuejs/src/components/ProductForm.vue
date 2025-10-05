<script setup>
import { ref } from 'vue'
const emit = defineEmits(['product-added'])
const title = ref('')
const description = ref('')
const submitForm = async () => {
  const res = await fetch('http://localhost:8000/products', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: title.value,
      description: description.value,
    }),
  })

  if (res.ok) {
    const data = await res.json()
    emit('product-added', data)
    title.value = ''
    description.value = ''
  } else {
    alert('Failed to add product')
  }
}
</script>

<template>
  <form @submit.prevent="submitForm">
    <h2>Add Product</h2>
    <input v-model="title" type="text" placeholder="Title" required />
    <textarea v-model="description" placeholder="Description" required></textarea>
    <button type="submit">Add</button>
  </form>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 30px;
}

input, textarea {
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
</style>
