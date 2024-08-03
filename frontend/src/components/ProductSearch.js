import React, { useState } from 'react';
import axios from 'axios';

function ProductSearch() {
    const [productName, setProductName] = useState('');
    const [result, setResult] = useState(null);

    const searchProduct = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/search/', {
                params: { product_name: productName }
            });
            setResult(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                placeholder="Enter product name"
            />
            <button onClick={searchProduct}>Search</button>
            {result && (
                <div>
                    <h3>Product URLs:</h3>
                    <p>Product: {result.product}</p>
                    <p>Flipkart: {result.flipkart}</p>
                    <p>Amazon: {result.amazon}</p>
                    <p>Croma: {result.croma}</p>
                </div>
            )}
        </div>
    );
}

export default ProductSearch;
