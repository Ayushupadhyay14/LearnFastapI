<script setup>
import { ref, onMounted } from 'vue'
import ProductForm from './ProductForm.vue'

const products = ref([])

const fetchProducts = async () => {
  const res = await fetch('http://localhost:8000/products')
  if (res.ok) {
    const data = await res.json()
    products.value = data
  } else {
    console.error('Failed to load products')
  }
}

onMounted(fetchProducts)

const handleProductAdded = (product) => {
  products.value.push(product)
}

</script>

<template>
  <div>
    <ProductForm @product-added="handleProductAdded" />
    <h2>Product List</h2>
    <ul>
      <li v-for="product in products" :key="product.id">
        <strong>{{ product.title }}</strong>: {{ product.description }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}

li {
  background: #f0f4ff;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 10px;
}

li strong {
  color: #0077ff;
}
</style>
