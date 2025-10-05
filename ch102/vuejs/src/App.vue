<script setup>
import ProductList from './components/ProductList.vue'
</script>

<template>
  <div class="container">
    <ProductList />
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 40px auto;
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: sans-serif;
}
</style>
