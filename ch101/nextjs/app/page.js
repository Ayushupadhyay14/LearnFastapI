'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function Home() {
  const [products, setProducts] = useState([])
  useEffect(() => {
    fetch('http://localhost:8000/products')
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error('Error fetching products:', err))
  }, [])
  return (
    <main style={{ maxWidth: '600px', margin: '40px auto', padding: '1rem' }}>
       <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>Product List</h1>
       <Link href="/create" style={{ color: 'blue', textDecoration: 'underline' }}>
        Add New Product
      </Link>
      <ul style={{ marginTop: '1rem', listStyle: 'none', padding: 0 }}>
        {products.map((product) => (
          <li
            key={product.id}
            style={{
              padding: '1rem',
              background: '#f0f4ff',
              marginBottom: '1rem',
              borderRadius: '8px',
            }}
          >
            <strong>{product.title}</strong>
            <p>{product.description}</p>
          </li>
        ))}
      </ul>

    </main>
  );
}
