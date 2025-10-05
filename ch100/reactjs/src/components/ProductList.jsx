import { useEffect, useState } from 'react';
import ProductForm from './ProductForm';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const fetchProducts = async () => {
    const res = await fetch('http://localhost:8000/products');
    const data = await res.json();
    setProducts(data);
  };
  useEffect(() => {
    fetchProducts();
  }, []);
  return (
    <div>
      <h1>Product List</h1>
      <ProductForm onProductAdded={(product) => setProducts([...products, product])} />
      <hr />
       <ul>
        {products.map((p) => (
          <li key={p.id}>
            <strong>{p.title}</strong>: {p.description}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ProductList