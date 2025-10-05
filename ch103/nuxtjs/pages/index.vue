<script setup>
const { data: products, error } = await useFetch('http://localhost:8000/products')

if (error.value) {
  console.error('Error loading products:', error.value)
}
</script>

<template>
 <div class="container">
    <h1>Product List</h1>
    <NuxtLink to="/create" class="link">Add New Product</NuxtLink>
    <ul v-if="products && products.length" class="product-list">
      <li v-for="p in products" :key="p.id">
        <strong>{{ p.title }}</strong>: {{ p.description }}
      </li>
    </ul>
    <p v-else>No products found.</p>
  </div>
</template>

<style scoped>
.container {
  max-width: 700px;
  margin: 40px auto;
  padding: 20px;
  font-family: sans-serif;
}
.product-list {
  list-style: none;
  padding: 0;
}
.product-list li {
  background: #f0f4ff;
  margin-bottom: 10px;
  padding: 12px;
  border-radius: 6px;
}
.link {
  display: inline-block;
  margin-bottom: 20px;
  color: blue;
  text-decoration: underline;
}
</style>